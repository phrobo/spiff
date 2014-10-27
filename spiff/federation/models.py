from django.db import models
from django.contrib.auth.models import Permission, User

class Federation(models.Model):
  url = models.TextField()
  lastContact = models.DateTimeField()
  permissions = models.ManyToManyField(Permission)
  ttl = models.IntegerField()
  enabled = models.BooleanField(default=True)
  alias = models.TextField()
