"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User, Group
import models
from spiff.api.tests import APITestMixin, withPermission, withLogin, withUser


class AnonymousUserMiddlewareTest(APITestMixin):
  def setUp(self):
    self.setupClient()

  def testFetchAnon(self):
    user = self.getAPI('/v1/identity/self/')
    self.assertNotEqual(user, None)

class IdentityTest(TestCase):
  def testUserCreation(self):
    u = User.objects.create_user('test', 'test@example.com', 'test')
    self.assertIsNotNone(u.identity)
    self.assertEqual(u.identity.user, u)
    u.delete()

  def testCreateAnonUser(self):
    userCount = len(User.objects.all())
    identityCount = len(models.Identity.objects.all())
    anonUser = models.get_anonymous_user()
    newUserCount = len(User.objects.all())
    newIdentityCount = len(models.Identity.objects.all())
    self.assertEqual(userCount, newUserCount)
    self.assertEqual(identityCount, newIdentityCount)
    self.assertEqual(models.get_anonymous_user().pk, anonUser.pk)

  def testRecreateAnonIdentity(self):
    user = models.get_anonymous_user()
    user.identity.delete()
    identity = None
    with self.assertRaises(models.Identity.DoesNotExist):
      identity = User.objects.get(id=user.pk).identity
    user = models.get_anonymous_user()
    self.assertEqual(user.identity.user_id, user.id)
    self.assertEqual(identity, None)

class IdentityAPITest(APITestMixin):
  def setUp(self):
    self.setupAPI()

  @withUser
  def testLogin(self):
    response = self.postAPI('/v1/identity/login/', {'username': 'test',
      'password': 'test'}, status=200)
    self.assertTrue('token' in response)

  @withUser
  def testBadLogin(self):
    response = self.postAPI('/v1/identity/login/', {'username': 'test',
      'password': 'nottest'}, status=401)
    self.assertIsNone(response)

  @withUser
  def testDisabledLogin(self):
    self.user.is_active = False
    self.user.save()
    response = self.postAPI('/v1/identity/login/', {'username': 'test',
      'password': 'test'}, status=403)
    self.assertIsNone(response)

  def testMissingPermission(self):
    response = self.postAPIRaw('/v1/identity/self/has_permission/not.a_permission/')
    self.assertEqual(response.status_code, 403)

  @withPermission('identity.add_identity')
  @withLogin
  def testHasPermission(self):
    response = self.postAPIRaw('/v1/identity/self/has_permission/identity.add_identity/')
    self.assertEqual(response.status_code, 204)
