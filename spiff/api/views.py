from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from spiff.local.models import SpaceConfig, SpaceContact, SpaceFeed
from spiff.identity.models import Rank
from spiff.api.plugins import find_apps
import json
import random

def spaceapi(request):
  meta = {}
  meta['api'] = '0.12'
  meta['x-spiff-version'] = '0.1'
  site = get_current_site(request)
  base = "%s://%s"%(request.META['wsgi.url_scheme'], site.domain)
  if (request.META['wsgi.url_scheme'] == 'http' and request.META['SERVER_PORT'] != '80') or (request.META['wsgi.url_scheme'] == 'https' and request.META['SERVER_PORT'] != '443'):
    base = "%s:%s"%(base, request.META['SERVER_PORT'])
  meta['x-spiff-url'] = "%s%s"%(base, reverse('root'))

  spaceConfig,created = SpaceConfig.objects.get_or_create(site=site)

  meta['space'] = site.name
  meta['logo'] = spaceConfig.logo
  meta['icon'] = {'open': spaceConfig.closedIcon, 'closed': spaceConfig.openIcon}
  meta['url'] = site.domain
  meta['open'] = spaceConfig.isOpen()

  meta['address'] = spaceConfig.address
  meta['lat'] = spaceConfig.lat
  meta['lon'] = spaceConfig.lon
  meta['status'] = spaceConfig.status
  meta['lastchange'] = str(spaceConfig.lastChange)
  meta['motd'] = spaceConfig.motd
  meta['x-spiff-welcome'] = settings.WELCOME_MESSAGE
  meta['x-spiff-greeting'] = random.choice(settings.GREETINGS)

  contacts = {}
  for c in SpaceContact.objects.filter(space=spaceConfig):
    contacts[c.name] = c.value
  meta['contact'] = contacts

  feeds = []
  for f in SpaceFeed.objects.filter(space=spaceConfig):
    feeds.append({'name': f.name, 'url': f.url})
  meta['feeds'] = feeds

  for app in find_apps():
    meta = app.filterSpaceAPI(meta)

  data = json.dumps(meta, indent=True)
  resp = HttpResponse(data)
  resp['Content-Type'] = 'text/plain'
  return resp

