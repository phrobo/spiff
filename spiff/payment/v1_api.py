from tastypie.resources import ModelResource
from tastypie.exceptions import ImmediateHttpResponse
from spiff.notification_loader import notification
notification = None
import stripe
import models
from django.conf import settings
from tastypie import fields
from spiff.api import SpiffAuthorization, OwnedObjectAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class CreditResource(ModelResource):
  identity = fields.ToOneField('spiff.identity.v1_api.IentityResource', 'identity')
  value = fields.FloatField('value')
  description = fields.CharField('description')
  created = fields.DateTimeField('created')

  class Meta:
    queryset = models.Credit.objects.all()
    authorization = OwnedObjectAuthorization('identity')
    always_return_data = True
    filtering = {
      'identity': ALL_WITH_RELATIONS,
      'value': ALL_WITH_RELATIONS,
      'description': ALL_WITH_RELATIONS,
      'created': ALL_WITH_RELATIONS
    }

class PaymentResource(ModelResource):
  invoice = fields.ToOneField('spiff.payment.v1_api.InvoiceResource', 'invoice')
  value = fields.FloatField('value')
  identity = fields.ToOneField('spiff.identity.v1_api.IdentityResource', 'identity')
  method = fields.IntegerField('method')

  class Meta:
    queryset = models.Payment.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
        'identity': ALL_WITH_RELATIONS,
        'value': ALL_WITH_RELATIONS,
        'method': ALL_WITH_RELATIONS,
        'invoice': ALL_WITH_RELATIONS,
    }

  def obj_create(self, bundle, **kwargs):
    bundle = self.full_hydrate(bundle)
    m2m = self.hydrate_m2m(bundle)
    invoice = m2m.obj.invoice
    if bundle.data['method'] == models.Payment.METHOD_STRIPE:
      stripe.api_key = settings.STRIPE_KEY
      cardData = {}
      stripeData = bundle.data['stripe']
      cardData['number'] = stripeData['card']
      cardData['exp_month'] = stripeData['exp_month']
      cardData['exp_year'] = stripeData['exp_year']
      cardData['cvc'] = stripeData['cvc']
      balance = float(bundle.data['value'])
      if balance > invoice.unpaidBalance:
        raise ImmediateHttpResponse(response=self.error_response("You can't pay more than $%s!"%(invoice.unpaidBalance)))
      charge = stripe.Charge.create(
        amount = int(balance*100),
        currency = 'usd',
        card = cardData,
        description = 'Payment from %s for invoice %s'%(bundle.request.identity.displayName, invoice.id)
      )
      payment = models.Payment.objects.create(
        identity = bundle.request.identity,
        value = balance,
        status = models.Payment.STATUS_PAID,
        transactionID = charge.id,
        method = models.Payment.METHOD_STRIPE,
        invoice = invoice
      )
      if notification:
        notification.send(
          [bundle.request.identity],
          'payment_received',
          {'identity': bundle.request.identity, 'payment': payment}
        )
      bundle.obj = payment
      return bundle
    else:
      return super(PaymentResource, self).obj_create(bundle, **kwargs)

class LineItemResource(ModelResource):
  name = fields.CharField(attribute='name')
  unitPrice = fields.FloatField('unitPrice')
  quantity = fields.FloatField('quantity')
  totalPrice = fields.FloatField('totalPrice')
  invoice = fields.ToOneField('spiff.payment.v1_api.InvoiceResource',
      attribute='invoice', full=False)

  class Meta:
    queryset = models.LineItem.objects.all()
    authorization = SpiffAuthorization()
    filtering = {
      'name': ALL_WITH_RELATIONS,
      'unitPrice': ALL_WITH_RELATIONS,
      'quantity': ALL_WITH_RELATIONS,
      'invoice': ALL_WITH_RELATIONS
    }
    always_return_data = True

class InvoiceResource(ModelResource):
  identity = fields.ToOneField('spiff.identity.v1_api.IdentityResource',
      attribute='identity',
      null=True, full=False)
  unpaidBalance = fields.FloatField('unpaidBalance', readonly=True)
  paidBalance = fields.FloatField('paidBalance', readonly=True)
  total = fields.FloatField('total', readonly=True)
  items = fields.ToManyField(LineItemResource, 'items', null=True, full=True);
  payments = fields.ToManyField(PaymentResource, 'payments', null=True, full=True);

  class Meta:
    queryset = models.Invoice.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
        'identity': ALL_WITH_RELATIONS
    }
