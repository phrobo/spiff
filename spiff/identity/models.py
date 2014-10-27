from django.db import models, connection
import random
import string
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_syncdb
from south.signals import post_migrate
from openid_provider.models import OpenID
import datetime
from django.conf import settings
from spiff import funcLog
from django.core.exceptions import ValidationError
from django.db.models import Q

if not hasattr(settings, 'ANONYMOUS_USER_ID'):
  settings.ANONYMOUS_USER_ID = 0

if not hasattr(settings, 'AUTHENTICATED_GROUP_ID'):
  settings.AUTHENTICATED_GROUP_ID = 0

class UserResetToken(models.Model):
  user = models.ForeignKey(User, related_name='resetTokens')
  token = models.CharField(max_length=10)
  created = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    if not self.token:
      self.token = ''.join(random.choice(string.ascii_uppercase +
        string.digits) for _ in range(10))
    return super(UserResetToken, self).save(*args, **kwargs)

class Identity(models.Model):
  tagline = models.CharField(max_length=255)
  user = models.OneToOneField(User, related_name='identity')
  created = models.DateTimeField(editable=False, auto_now_add=True)
  lastSeen = models.DateTimeField(editable=False, auto_now_add=True)
  fields = models.ManyToManyField('Field', through='FieldValue')
  hidden = models.BooleanField(default=False)
  displayName = models.TextField()

  def isAnonymous(self):
    return self.user_id == get_anonymous_user().id

  class Meta:
    permissions = (
      ('can_view_hidden_identities', 'Can view hidden identities'),
      ('list_identities', 'Can list identities'),
    )

  @property
  def fullName(self):
    if self.hidden:
      return "Anonymous"
    else:
      return self.displayName

  @property
  def outstandingBalance(self):
    sum = 0
    invoices = self.user.invoices.unpaid()
    for i in invoices:
        sum += i.unpaidBalance
    return sum

  @property
  def overdue(self):
    return len(self.user.invoices.pastDue()) > 0

  @property
  def keyholder(self):
    groups = self.user.groups.filter(rank__isKeyholder=True)
    return len(groups) > 0

  def __unicode__(self):
    if self.hidden:
      return "Anonymous"
    return self.displayName

class Field(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  required = models.BooleanField(default=False)
  public = models.BooleanField(default=False)
  protected = models.BooleanField(default=False)

  class Meta:
    permissions = (
      ('can_view_private_fields', 'Can view private fields'),
      ('can_edit_protected_fields', 'Can edit protected fields'),
    )

  def __unicode__(self):
    return self.name

class FieldValue(models.Model):
  field = models.ForeignKey(Field)
  identity = models.ForeignKey(Identity, related_name='attributes')
  value = models.TextField()

  def __unicode__(self):
    return "%s: %s = %s"%(self.identity.displayName, self.field.name, self.value)

def create_identity(sender, instance, created, **kwargs):
  if created:
    Identity.objects.get_or_create(user=instance)
    OpenID.objects.get_or_create(user=instance, default=True)

post_save.connect(create_identity, sender=User)

class AuthenticatedUser(User):
  class Meta:
    proxy = True

  def has_perm(self, perm, obj=None):
    funcLog().debug("Checking %s for permission %s on %r",self, perm, obj)
    if super(AuthenticatedUser, self).has_perm(perm, obj):
      funcLog().debug("Found django permission %s", perm)
      return True
    anon = get_anonymous_user()
    if anon.has_perm(perm, obj):
      funcLog().debug("Found anonymous permission %s", perm)
      return True
    app, perm = perm.split('.', 1)
    ret = get_authenticated_user_group().permissions.filter(
      content_type__app_label = app,
      codename=perm).exists()
    if ret:
      funcLog().debug("Found authenticated group permission %s", perm)
    else:
      funcLog().debug("Denied")
    return ret


class AuthenticatedUserGroup(Group):
  class Meta:
    proxy = True

class AnonymousUser(User):
  def is_anonymous(self):
    return True

  def has_perm(self, *args, **kwargs):
    u = User.objects.get(pk=self.pk)
    return u.has_perm(*args, **kwargs)

  class Meta:
    proxy = True

def get_authenticated_user_group():
  if settings.AUTHENTICATED_GROUP_ID == 0:
    try:
      group = AuthenticatedUserGroup.objects.get(
        name='Authenticated Users'
      )
    except AuthenticatedUserGroup.DoesNotExist:
      group = AuthenticatedUserGroup.objects.create(
        name='Authenticated Users'
      )
  else:
    group = AuthenticatedUserGroup.objects.get(id=settings.AUTHENTICATED_GROUP_ID)
  return group

def get_anonymous_user():
  if settings.ANONYMOUS_USER_ID == 0:
    try:
      user = AnonymousUser.objects.get(
        username='anonymous'
      )
    except AnonymousUser.DoesNotExist:
      user = AnonymousUser.objects.create(
        username='anonymous',
        email='anonymous@example.com',
        password='',
      )
      user.set_unusable_password()
      user.save()
      identity = Identity.objects.get(
        user=user,
        displayName='Guest McGuesterson'
      )
      identity.hidden = True
      identity.save()
  else:
    user = User.objects.get(id=settings.ANONYMOUS_USER_ID)
  try:
    identity = user.identity
  except Identity.DoesNotExist:
    user.identity, created = Identity.objects.get_or_create(user=user)
    user.save()
  return user

post_save.connect(create_identity, sender=AnonymousUser)

def ensure_auth_objects(*args, **kwargs):
  try:
    get_anonymous_user()
    get_authenticated_user_group()
  except:
    pass

post_migrate.connect(ensure_auth_objects)
post_syncdb.connect(ensure_auth_objects)
