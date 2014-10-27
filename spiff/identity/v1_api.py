from django.db.models import Q
from django.utils.timezone import utc
import datetime
from django.contrib.sites.models import get_current_site
import string
import random
from django.conf.urls import url
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import models
from spiff.api import SpiffAuthorization
import json
from spiff import funcLog
import jwt
from django.conf import settings
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from django.core.mail import send_mail

class FieldValueAuthorization(SpiffAuthorization):
  def conditions(self):
    return (
      ('public', 'field is public'),
      ('protected', 'field is protected'),
      ('private', 'field is private'),
    ) + super(FieldValueAuthorization, self).conditions()

  def check_perm(self, bundle, model, permName):
    if model.field.public:
      return super(FieldValueAuthorization, self).check_perm(bundle, model,
      '%s_public'%(permName))
    if model.field.protected:
      return super(FieldValueAuthorization, self).check_perm(bundle, model,
      '%s_protected'%(permName))
    return super(FieldValueAuthorization, self).check_perm(bundle, model,
    '%s_private'%(permName))

class FieldResource(ModelResource):
  name = fields.CharField('name')
  description = fields.CharField('description')
  required = fields.BooleanField('required')
  public = fields.BooleanField('public')
  protected = fields.BooleanField('protected')

  class Meta:
    queryset = models.Field.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True

class FieldValueResource(ModelResource):
  field = fields.ToOneField(FieldResource, 'field', full=True)
  value = fields.CharField('value')
  identity = fields.ToOneField('spiff.identity.v1_api.IdentityResource', 'identity')

  class Meta:
    queryset = models.FieldValue.objects.all()
    authorization = FieldValueAuthorization()
    always_return_data = True


class PermissionResource(ModelResource):
  name = fields.CharField('name', readonly=True)
  app = fields.CharField('content_type__app_label', readonly=True)
  codename = fields.CharField('codename', readonly=True)
  id = fields.IntegerField('id', readonly=True)

  class Meta:
    queryset = Permission.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'id': ALL_WITH_RELATIONS,
      'name': ALL_WITH_RELATIONS,
      'app': ALL_WITH_RELATIONS,
      'codename': ALL_WITH_RELATIONS
    }

class GroupResource(ModelResource):
  permissions = fields.ToManyField(PermissionResource, 'permissions',
      full=False, blank=True)

  class Meta:
    queryset = Group.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'rank': ALL_WITH_RELATIONS,
      'name': ALL_WITH_RELATIONS,
      'permissions': ALL_WITH_RELATIONS
    }

class SelfIdentityAuthorization(SpiffAuthorization):
  def check_perm(self, bundle, model, name):
    if bundle.request.identity.pk == model.pk:
      return True
    return super(SelfIdentityAuthorization, self).check_perm(bundle, model, name)

class IdentityResource(ModelResource):
  username = fields.CharField(attribute='user__username', help_text="Login Username")
  displayName = fields.CharField(attribute='displayName', null=True,
      help_text="Display name")
  isAnonymous = fields.BooleanField(attribute='isAnonymous')
  email = fields.CharField(attribute='user__email')
  groups = fields.ToManyField(GroupResource, 'user__groups', null=True,
      full=True)
  userid = fields.IntegerField('user_id', readonly=True)
  fields = fields.ToManyField('spiff.identity.v1_api.FieldValueResource', 'attributes', full=False, null=True)

  class Meta:
    queryset = models.Identity.objects.all()
    authorization = SelfIdentityAuthorization()
    always_return_data = True
    filtering = {
      'groups': ALL_WITH_RELATIONS,
      'displayName': ALL_WITH_RELATIONS,
    }

  def obj_update(self, bundle, **kwargs):
    data = bundle.data
    if 'currentPassword' in data and 'password' in data:
      u = bundle.obj.user
      valid = False
      if u.check_password(data['currentPassword']):
        valid = True
      else:
        tokens = models.UserResetToken.objects.filter(user=u,
            token=data['currentPassword'])
        if tokens.exists():
          valid = True
      u.set_password(data['password'])
      u.save()
    return bundle

  def obj_create(self, bundle, **kwargs):
    data = bundle.data
    funcLog().debug("Creating user from %r", data)
    u = User.objects.create(
      username = data['username'],
      email = data['email'],
      displayName = data['displayName']
    )
    u.set_password(data['password'])
    u.save()
    if 'fields' in data:
      for f in data['fields']:
        field = models.Field.objects.get(id=f['id'])
        models.FieldValue.objects.create(
          field = field,
          value = f['value'],
          identity = u.identity
        )
    bundle.obj = u.identity
    return bundle

  def self(self, request, **kwargs):
    self.method_check(request, allowed=['get'])
    self.throttle_check(request)
    return self.get_detail(request, pk=request.identity.id)

  def has_permission(self, request, permission_name, **kwargs):
    if permission_name == 'is_superuser' and request.user.is_superuser:
      return HttpResponse(status=204)
    if request.user.has_perm(permission_name):
      return HttpResponse(status=204)
    return HttpResponse(status=403)

  def prepend_urls(self):
    return [
      url(r'^(?P<resource_name>%s)/login%s$' %
        (self._meta.resource_name, trailing_slash()),
        self.wrap_view('login'), name='login'),
      url(r'^(?P<resource_name>%s)/requestPasswordReset%s$' %
        (self._meta.resource_name, trailing_slash()),
        self.wrap_view('requestPasswordReset'), name='requestPasswordReset'),
      url(r'^(?P<resource_name>%s)/self%s$' %
        (self._meta.resource_name, trailing_slash()),
        self.wrap_view('self'), name='self'),
      url(r'^(?P<resource_name>%s)/self/has_permission/(?P<permission_name>.*)%s$' %
        (self._meta.resource_name, trailing_slash()),
        self.wrap_view('has_permission'), name='self_has_permission')
    ]

  def requestPasswordReset(self, request, **kwargs):
    self.method_check(request, allowed=['post'])
    data = self.deserialize(request, request.body,
        format=request.META.get('CONTENT_TYPE', 'application/json'))

    users = User.objects.filter(Q(username=data['userid']) |
      Q(email=data['userid']))

    site = get_current_site(request)

    for u in users:
      token = models.UserResetToken.objects.create(user=u)
      funcLog().info("Resetting password for %s, mailing %s to %s", u.username,
          token.token, u.email)
      message = [
        random.choice(settings.GREETINGS),
        '',
        'This is Spaceman Spiff for %s'%(site.name),
        '',
        'Someone from the IP %s has requested that your password be reset.',
        '',
        'To reset your password, visit %s and use this temporary password to login:'%(settings.WEBUI_URL),
        '',
        '%s'%(token.token),
        '',
        'It will expire after 5 minutes. If you did not request to have your password reset, feel free to ignore this message!'
        '',
        'Thanks!'
      ]

      send_mail('Spiff Password Reset', "\n".join(message), settings.DEFAULT_FROM_EMAIL,
          [u.email])
    return self.create_response(request, {'success': True})

  def login(self, request, **kwargs):
    self.method_check(request, allowed=['post'])
    data = self.deserialize(request, request.body,
        format=request.META.get('CONTENT_TYPE', 'application/json'))

    if 'username' in data and 'password' in data:
      username = data['username']
      password = data['password']
    else:
      username = None
      password = None

    user = authenticate(username=username, password=password)
    if user:
      if user.is_active:
        funcLog().info("Successful login for %s", username)
        token = {}
        token['id'] = user.id
        return self.create_response(request, {
          'success': True,
          'token': jwt.encode(token, settings.SECRET_KEY),
          'passwordReset': False
        })
      else:
        funcLog().warning("Good login, but %s is disabled.", username)
        raise ImmediateHttpResponse(response=HttpForbidden())
    else:
      tokens = models.UserResetToken.objects.filter(user__username=username, token=password)
      for t in tokens:
        if t.created >= datetime.datetime.utcnow().replace(tzinfo=utc)-datetime.timedelta(minutes=5):
          user = t.user
          funcLog().info("Successful password reset for %s", user.username)
          token = {}
          token['id'] = user.id
          return self.create_response(request, {
            'success': True,
            'token': jwt.encode(token, settings.SECRET_KEY),
            'passwordReset': True,
          })
        else:
          t.delete()
      funcLog().warning("Invalid login for %s", username)
      raise ImmediateHttpResponse(response=HttpUnauthorized())
