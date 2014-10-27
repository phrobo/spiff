from django.test import TestCase
from django.contrib.auth.models import User, Group
import models
from spiff.api.tests import APITestMixin, withPermission, withLogin, withUser, withAdmin
import datetime
from spiff.subscription.models import SubscriptionPeriod, Subscription
from spiff.subscription import api as subscriptionAPI
import calendar
from spiff.payment.models import Invoice, Payment

class RankTest(TestCase):
  def testGroupCreation(self):
    g = Group.objects.create(name="Test Group")
    self.assertIsNotNone(g.rank)
    self.assertEqual(g.rank.group, g)
    g.delete()


class MembershipPeriodTest(APITestMixin):
  def setUp(self):
    self.setupAPI()

  @withAdmin
  def addOldDues(self):
    rank = self.createGroup('test').rank
    rank.monthlyDues = 15
    rank.save()

    self.postAPI('/v1/invoice/',
      {
        'identity': self.user.identity,
        'dueDate': datetime.date.today()
      }
    )

    self.postAPI('/v1/ranklineitem/',
      {
        'invoice': '/v1/invoice/1/',
        'rank': '/v1/rank/1/',
        'member': '/v1/member/1/',
        'activeFromDate': datetime.date.today(),
        'activeToDate': datetime.date.today(),
        'quantity': 1
      }
    )
    self.postAPI('/v1/payment/',
      {
        'invoice': '/v1/invoice/1/',
        'value': 15,
        'method': 0,
        'identity': '/v1/identity/1/'
      }
    )
    membershipPeriod = self.identity.membershipPeriods.all()[0]
    self.assertEqual(membershipPeriod.activeFromDate.date(),
        datetime.date.today())
    self.assertEqual(membershipPeriod.activeToDate.date(), datetime.date.today())

  @withPermission('identity.read_identity')
  @withPermission('auth.read_group')
  @withPermission('membership.create_membershipperiod')
  @withPermission('membership.read_rank')
  @withPermission('payment.create_invoice')
  @withPermission('payment.create_payment')
  @withPermission('subscription.read_subscriptionplan')
  @withAdmin
  def testSubscribeAndPayDues(self):
    rank = self.createGroup('test').rank
    rank.monthlyDues = 15
    rank.save()

    period = SubscriptionPeriod.objects.create(
      name = 'Monthly',
      dayOfMonth=1
    )

    plan = models.RankSubscriptionPlan.objects.create(
      rank = rank,
      identity = self.user.identity,
      period = period
    )

    self.postAPI('/v1/subscription/',
      {
        'identity': '/v1/identity/1/',
        'plan': '/v1/subscriptionplan/1/',
      }
    )

    self.assertEqual(len(self.user.identity.invoices.all()), 0)
    subscriptionAPI.processSubscriptions()
    self.assertEqual(len(self.user.identity.invoices.all()), 1)

    subscriptionAPI.processSubscriptions()
    self.assertEqual(len(self.user.identity.invoices.all()), 1)

    self.postAPI('/v1/payment/',
      {
        'invoice': '/v1/invoice/1/',
        'value': 15,
        'method': 0,
        'identity': '/v1/identity/1/'
      }
    )

    self.assertTrue(self.user.groups.filter(name='test').exists())

    today = datetime.date.today()
    monthStart = datetime.date(year=today.year, month=today.month, day=1)
    monthEnd = datetime.date(year=today.year, month=today.month,
        day=calendar.monthrange(today.year, today.month)[1])
    monthEnd += datetime.timedelta(days=1)

    membershipPeriod = self.user.identity.membershipPeriods.all()[0]
    self.assertEqual(membershipPeriod.activeFromDate.date(), monthStart)
    self.assertEqual(membershipPeriod.activeToDate.date(), monthEnd)

    subscriptionAPI.processSubscriptions()
    self.assertEqual(len(self.user.identity.invoices.all()), 1)

# Create your tests here.
