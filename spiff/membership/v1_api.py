from spiff.api import SpiffAuthorization
from django.conf.urls import url
from tastypie.utils import trailing_slash
from spiff.subscription import v1_api as subscription
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import models
from tastypie.resources import ModelResource
from tastypie import fields

class RankPlanAuthorization(SpiffAuthorization):
  def conditions(self):
    return (
      ('active_membership', 'rank is active membership'),
    )+super(RankPlanAuthorization, self).conditions()

  def check_perm(self, bundle, model, name):
    if model.rank.isActiveMembership:
      return super(RankPlanAuthorization, self).check_perm(bundle, model,
        '%s_active_membership'%(name))
    return super(RankPlanAuthorization, self).check_perm(bundle, model, name)

class RankSubscriptionPlanResource(subscription.SubscriptionPlanResource):
  class Meta:
    queryset = models.RankSubscriptionPlan.objects.all()
    authorization = RankPlanAuthorization()
    always_return_data = True

class RankResource(ModelResource):
  group = fields.ToOneField('spiff.identity.v1_api.GroupResource', 'group')
  monthlyDues = fields.FloatField('monthlyDues')
  isActiveMembership = fields.BooleanField('isActiveMembership')

  class Meta:
    queryset = models.Rank.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'group': ALL_WITH_RELATIONS,
      'monthlyDues': ALL_WITH_RELATIONS,
      'isActiveMembership': ALL_WITH_RELATIONS
    }

class MembershipPeriodResource(ModelResource):
  rank = fields.ToOneField(RankResource, 'rank', full=True)
  member = fields.ToOneField('spiff.identity.v1_api.MemberResource',
  'member')
  activeFromDate = fields.DateTimeField('activeFromDate')
  activeToDate = fields.DateTimeField('activeToDate')
  contiguousPeriods = fields.ToManyField('spiff.identity.v1_api.MembershipPeriodResource', 'contiguousPeriods', null=True)
  contiguousDates = fields.ListField('contiguousDates', null=True)

  class Meta:
    queryset = models.MembershipPeriod.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'rank': ALL_WITH_RELATIONS,
      'member': ALL_WITH_RELATIONS,
      'activeFromDate': ALL_WITH_RELATIONS,
      'activeToDate': ALL_WITH_RELATIONS
    }

class RankLineItemResource(ModelResource):
  rank = fields.ToOneField(RankResource, 'rank')
  identity = fields.ToOneField('spiff.identity.v1_api.IdentityResource', 'identitiy')
  activeFromDate = fields.DateField('activeFromDate')
  activeToDate = fields.DateField('activeToDate')
  invoice = fields.ToOneField('spiff.payment.v1_api.InvoiceResource', 'invoice')
  quantity = fields.IntegerField('quantity')

  class Meta:
    queryset = models.RankLineItem.objects.all()
    always_return_data = True
    authorization = SpiffAuthorization()
    filtering = {
      'rank': ALL_WITH_RELATIONS,
      'member': ALL_WITH_RELATIONS,
      'activeFromDate': ALL_WITH_RELATIONS,
      'activeToDate': ALL_WITH_RELATIONS,
      'invoice': ALL_WITH_RELATIONS,
      'quantity': ALL_WITH_RELATIONS
    }

class StripeProxyResource(ModelResource):
  def prepend_urls(self):
    return [
      url(r'^(?P<resource_name>%s)/(?P<id>.*)/stripeCards/(?P<stripeCardID>.*)%s$' %
        (self._meta.resource_name, trailing_slash()),
        self.wrap_view('stripeCard'), name='self'),
      url(r'^(?P<resource_name>%s)/(?P<id>.*)/stripeCards%s$' %
        (self._meta.resource_name, trailing_slash()),
        self.wrap_view('stripeCards'), name='self'),
    ]

  class Meta:
    queryset = models.RankLineItem.objects.all()

  def stripeCards(self, request, **kwargs):
    self.method_check(request, allowed=['post', 'get'])
    self.is_authenticated(request)
    self.throttle_check(request)
    member = models.Identity.objects.get(pk=kwargs['id'])

    if request.method == 'POST':
      cardData = json.loads(request.body)
      newCard = {}
      newCard['number'] = cardData['card']
      newCard['exp_month'] = cardData['exp_month']
      newCard['exp_year'] = cardData['exp_year']
      newCard['cvc'] = cardData['cvc']
      member.addStripeCard(newCard)

      return self.create_response(request, {'success': True})
    else:
      return self.create_response(request, {'cards': member.stripeCards})

  def stripeCard(self, request, **kwargs):
    self.method_check(request, allowed=['delete'])
    self.is_authenticated(request)
    self.throttle_check(request)

    cardID = kwargs['stripeCardID']

    member = models.Identity.objects.get(pk=kwargs['id'])
    member.removeStripeCard(cardID)

    return self.create_response(request, {'success': True})
