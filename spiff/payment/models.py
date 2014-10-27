from django.db import models
from spiff.identity.models import Identity
from django.utils.timezone import utc
import datetime
import stripe
from spiff import funcLog

from spiff.notification_loader import notification
notification = None
from spiff.api.plugins import find_api_classes
from django.conf import settings

if not hasattr(settings, 'STRIPE_KEY'):
  settings.STRIPE_KEY = None

stripe.api_key = settings.STRIPE_KEY

class StripeProxy(models.Model):
  identity = models.ForeignKey(Identity, related_name='stripe')
  stripeID = models.TextField()

  @property
  def customer(self):
    try:
      customer = stripe.Customer.retrieve(self.stripeID)
    except stripe.InvalidRequestError:
      customer = stripe.Customer.create(
        description = self.fullName,
        email = self.identity.email
      )
      self.stripeID = customer.id
      self.save()
      return self.stripeCustomer()
    if customer.get('deleted') == True:
      self.stripeID = ""
      self.save()
      return self.stripeCustomer()
    return customer

  @property
  def stripeCards(self):
    customer = self.stripeCustomer()
    if customer.get('cards'):
      return customer.cards.data
    return []

  def addStripeCard(self, cardData):
    customer = self.stripeCustomer()
    return customer.cards.create(
      card = cardData
    )

  def setDefaultStripeCard(self, cardID):
    customer = self.stripeCustomer()
    customer.default_card = cardID
    customer.save()

  def removeStripeCard(self, cardID):
    customer = self.stripeCustomer()
    customer.cards.retrieve(cardID).delete()

class InvoiceManager(models.Manager):

    def allOpen(self):
        return self.filter(open=True, draft=False)

    def unpaid(self):
        ids = []
        for i in self.allOpen():
            if i.unpaidBalance > 0:
                ids.append(i.id)
        return self.filter(id__in=ids, draft=False)

    def pastDue(self):
        return self.unpaid().filter(dueDate__lt=datetime.date.utcnow().replace(tzinfo=utc), draft=False)

class Invoice(models.Model):
    identity = models.ForeignKey(Identity, related_name='invoices')
    created = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateField()
    open = models.BooleanField(default=True)
    draft = models.BooleanField(default=True)

    @classmethod
    def bundleLineItems(cls, identity, dueDate, items):
      if len(items) == 0:
        return None

      invoice = Invoice.objects.create(
        identity = identity,
        dueDate = dueDate,
      )
      for item in items:
        item.invoice = invoice
        item.save()
      return invoice

    class Meta:
      permissions = (
        ('view_other_invoices', 'Can view invoices assigned to other identities'),
      )

    def chargeStripe(self):
      stripeCustomer = self.identity.stripe.customer()
      charge = stripe.Charge.create(
        amount = int(self.unpaidBalance*100),
        currency = 'usd',
        description = 'Payment from %s for invoice %s'%(self.identity.displayName, self.id),
        customer = stripeCustomer.id
      )
      Payment.objects.create(
        identity = self.identity,
        value = self.unpaidBalance,
        status = Payment.STATUS_PAID,
        transactionID = charge.id,
        method = Payment.METHOD_STRIPE,
        invoice = self
      )

    def save(self, *args, **kwargs):
      if self.pk and notification:
        current = Invoice.objects.get(pk=self.pk)
        if current.draft == True or current.open == False:
          if self.draft == False and self.open == True and self.unpaidBalance > 0:
            try:
              self.chargeStripe()
            except stripe.error.CardError, e:
              funcLog().error("Failed to charge stripe")
              funcLog().exception(e)
              notification.send(
                [self.identity],
                "card_failed",
                {'identity': self.identity, 'invoice': self})
      super(Invoice, self).save(*args, **kwargs)

    @property
    def unpaidBalance(self):
        return self.total - self.paidBalance

    @property
    def paidBalance(self):
        sum = 0
        for p in self.payments.all():
            sum += p.value
        return sum

    objects = InvoiceManager()

    @property
    def total(self):
        sum = 0
        for s in self.items.all():
            sum += s.totalPrice
        for d in self.discounts.all():
            sum -= d.value
        return sum

    def __unicode__(self):
        return "Invoice %d"%(self.id)

    @property
    def isOverdue(self):
      return self.dueDate < datetime.date.utcnow().replace(tzinfo=utc) and self.draft is False 

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items')
    name = models.TextField()
    unitPrice = models.FloatField(default=0)
    quantity = models.FloatField(default=1)

    def isOpen(self):
        return self.invoice.open

    def process(self):
      pass

    @property
    def totalPrice(self):
        return self.unitPrice * self.quantity

    def __unicode__(self):
        return "%d %s @%d ea, %s"%(self.quantity, self.name, self.unitPrice, self.invoice)

class LineDiscountItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='discounts')
    description = models.TextField()
    flatRate = models.FloatField(default=0)
    percent = models.FloatField(default=0)
    lineItem = models.ForeignKey(LineItem, related_name='discounts')

    @property
    def value(self):
      """Returns the positive value to subtract from the total."""
      originalPrice = self.lineItem.totalPrice
      if self.flatRate == 0:
        return originalPrice * self.percent
      return self.flatRate

class CreditManager(models.Manager):
    def forIdentity(self, identity):
        return self.filter(identity=identity)

    def identityTotal(self, identity):
        totalCredit = self.forIdentity(identity).aggregate(models.Sum('value'))
        totalUsedCredit = Payment.objects.filter(identity=identity,
            method=Payment.METHOD_CREDIT).aggregate(models.Sum('value'))
        if totalUsedCredit['value__sum'] is None:
          totalUsedCredit['value__sum'] = 0
        if totalCredit['value__sum'] is None:
          totalCredit['value__sum'] = 0
        return totalCredit['value__sum'] - totalUsedCredit['value__sum']

class Credit(models.Model):
    objects = CreditManager()

    identity = models.ForeignKey(Identity, related_name='credits')
    value = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

class Payment(models.Model):
    METHOD_CASH = 0
    METHOD_CHECK = 1
    METHOD_STRIPE = 2
    METHOD_OTHER = 3
    METHOD_CREDIT = 4
    METHODS = (
        (METHOD_CASH, 'Cash'),
        (METHOD_CHECK, 'Check'),
        (METHOD_STRIPE, 'Stripe'),
        (METHOD_OTHER, 'Other'),
        (METHOD_CREDIT, 'Credit'),
    )
    STATUS_PENDING = 0
    STATUS_PAID = 1
    STATUS = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
    )
    identity = models.ForeignKey(Identity, related_name='payments')
    value = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=STATUS_PENDING, choices=STATUS)
    transactionID = models.TextField(blank=True, null=True)
    method = models.IntegerField(choices=METHODS)
    invoice = models.ForeignKey(Invoice, related_name='payments')

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = datetime.datetime.utcnow().replace(tzinfo=utc)
            if notification:
              notification.send(
                [self.identity],
                "payment_received",
                {'identity': self.identity, 'payment': self})
        super(Payment, self).save(*args, **kwargs)
        if self.invoice.unpaidBalance == 0:
            self.invoice.open = False
            self.invoice.save()
            for lineItemType in find_api_classes('models', LineItem):
              for item in lineItemType.objects.filter(invoice=self.invoice):
                item.process()

    def __unicode__(self):
        return "%d %s by %s for %s"%(self.value, self.get_method_display(),
            self.identity, self.invoice)

