from django.core.management import BaseCommand
from spiff.identity.models import Identity

class Command(BaseCommand):
  help = 'Lists active member email addresses'

  def handle(self, *args, **options):
    identities = Identity.objects.all()
    for i in identity:
      print i.user.email
