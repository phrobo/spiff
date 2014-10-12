from django.db import models
import spiff.membership.models

class UnwelcomePerson(models.Model):
  name = models.TextField()
  reason = models.TextField()
  creator = models.ForeignKey(spiff.membership.models.Member)
  timestamp = models.DateTimeField(auto_now_add=True)

class Voucher(models.Model):
  member = models.ForeignKey(spiff.membership.models.Member)
  unwelsomePerson = models.ForeignKey('UnwelcomePerson')
  timestamp = models.DateTimeField(auto_now_add=True)
