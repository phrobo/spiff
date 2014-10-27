from django.db import models
import spiff.payment.models
from spiff.identity.models import Identity, AuthenticatedUserGroup
from django.contrib.auth.models import Group
from spiff.membership.utils import monthRange
from django.db.models.signals import post_save, post_syncdb
import datetime
from spiff.subscription.models import SubscriptionPlan
from spiff import funcLog

class Rank(models.Model):
  description = models.TextField(blank=True)
  monthlyDues = models.FloatField(default=0)
  group = models.OneToOneField(Group)
  isActiveMembership = models.BooleanField(default=False)
  isKeyholder = models.BooleanField(default=False)

  class Meta:
    permissions = (
      ('can_change_identity_rank', 'Can change identity ranks'),
      ('can_view_identity_rank', 'Can view identity ranks'),
      ('can_deactivate_identity', 'Can deactivate an identity'),
    )

  def __unicode__(self):
    return self.group.name

def create_rank(sender, instance, created, **kwargs):
  if created:
    Rank.objects.get_or_create(group=instance)

class RankLineItem(spiff.payment.models.LineItem):
    rank = models.ForeignKey(Rank)
    identity = models.ForeignKey(Identity, related_name='rankLineItems')
    activeFromDate = models.DateTimeField(default=datetime.datetime.utcnow())
    activeToDate = models.DateTimeField(default=datetime.datetime.utcnow())

    def process(self):
      period, created = MembershipPeriod.objects.get_or_create(
        rank = self.rank,
        identity = self.identity,
        activeFromDate = self.activeFromDate,
        activeToDate = self.activeToDate,
        lineItem = self
      )
      if created:
        u = self.identity.user
        u.groups.add(self.rank.group)
        u.save()
        funcLog().info("Processed %s - added %s to group %s", self,
            self.identity,
            self.rank.group)

    def save(self, *args, **kwargs):
        self.unitPrice = self.rank.monthlyDues
        self.name = "%s membership dues for %s, %s to %s"%(self.rank,
            self.identity, self.activeFromDate, self.activeToDate)
        super(RankLineItem, self).save(*args, **kwargs)

class MembershipPeriod(models.Model):
    rank = models.ForeignKey(Rank)
    identity = models.ForeignKey(Identity, related_name='membershipPeriods')
    activeFromDate = models.DateTimeField(default=datetime.datetime.utcnow())
    activeToDate = models.DateTimeField(default=datetime.datetime.utcnow())
    lineItem = models.ForeignKey(RankLineItem, default=None, null=True, blank=True)

    class Meta:
      index_together = [
        ['activeFromDate', 'activeToDate']
      ]


    @property
    def contiguousPeriods(self):
      dates = self.contiguousDates
      range = MembershipPeriod.objects.filter(
        rank = self.rank,
        identity = self.identity,
        activeFromDate__gte=dates[0],
        activeToDate__lte=dates[1]
      )
      funcLog().debug("Found %s!", range)
      return range

    @property
    def contiguousDates(self):
      start = self
      end = self
      seen = []
      overlapQueue = [self]
      cursor = connection.cursor()
      cursor.execute("\
        SELECT MIN(a.activeFromDate), MAX(b.activeToDate) \
        FROM membership_membershipperiod AS a \
        LEFT JOIN membership_membershipperiod AS b \
        ON \
          ( a.activeToDate >= b.activeFromDate OR \
          a.activeFromDate <= b.activeToDate) AND \
          a.identity_id = b.identity_id \
          WHERE a.identity_id = %s AND \
          a.activeFromDate <= %s AND \
          b.activeToDate >= %s", [self.identity.id, self.activeFromDate,
            self.activeToDate])
      row = cursor.fetchone()
      return (row[0], row[1])

    @property
    def siblings(self):
      return self.overlapping.filter(Q(activeFromDate=self.activeToDate) | Q(activeToDate=self.activeFromDate))

    @property
    def overlapping(self):
      return MembershipPeriod.objects.filter(
        Q(activeFromDate__gte=self.activeFromDate, activeFromDate__lte=self.activeToDate) | 
        Q(activeToDate__gte=self.activeFromDate, activeToDate__lte=self.activeToDate)
      ).filter(rank=self.rank, identitiy=self.identity).exclude(pk=self.pk)

    def __unicode__(self):
      return "%s, %s: %s to %s"%(self.identity, self.rank, self.activeFromDate,
          self.activeToDate)

class RankSubscriptionPlan(SubscriptionPlan):
    rank = models.ForeignKey(Rank, related_name='subscriptions')
    identity = models.ForeignKey(Identity, related_name='rankSubscriptions',
        blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def calculatePeriodCost(self):
      return self.rank.monthlyDues * self.quantity

    def createLineItems(self, subscription, processDate):
      targetIdentity = self.identity
      if targetIdentity is None:
        targetIdentity = subscription.identity
      planOwner = subscription.identity
      startOfMonth, endOfMonth = monthRange(processDate)

      funcLog().info("Processing subscription of %s dues for %s, billing to %s",
          self.rank, self.identity, planOwner)
      endOfMonth += datetime.timedelta(days=1)

      #FIXME: membershipRanges was removed
      #for range in targetIdentity.membershipRanges:
      #  if range['start'] <= startOfMonth and range['end'] >= endOfMonth:
      #    return []
      #  if RankLineItem.objects.filter(rank=self.rank, identity=targetIdentitiy,
      #      activeFromDate=startOfMonth, activeToDate=endOfMonth).exists():
      #    return []

      return [RankLineItem(
        rank = self.rank,
        identity = targetIdentity,
        activeFromDate = startOfMonth,
        activeToDate = endOfMonth
      ),]

    def __unicode__(self):
      return "%sx%s for %s, %s"%(self.rank, self.quantity, self.identity, self.period)

post_save.connect(create_rank, sender=Group)
post_save.connect(create_rank, sender=AuthenticatedUserGroup)

# Create your models here.
