from tastypie import fields
import requests
from tastypie.resources import ModelResource
from spiff.api import SpiffAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import models
from django.conf.urls import url
from tastypie.utils import trailing_slash

class FederationResource(ModelResource):
  url = fields.CharField('url')
  alias = fields.CharField('alias')
  ttl = fields.IntegerField('ttl')
  enabled = fields.BooleanField('enabled')
  lastContact = fields.DateTimeField('lastContact', readonly=True)

  class Meta:
    queryset = models.Federation.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'alias': ALL_WITH_RELATIONS,
      'enabled': ALL_WITH_RELATIONS,
      'lastContact': ALL_WITH_RELATIONS,
      'url': ALL_WITH_RELATIONS,
      'ttl': ALL_WITH_RELATIONS
    }

  def prepend_urls(self):
    return [
      url(r'^(?P<resource_name>%s)/(?P<id>.*)/query/(?P<query>.*)$' %
        (self._meta.resource_name),
        self.wrap_view('federatedSearch'), name='search')
    ]

  def federatedSearch(self, request, **kwargs):
    self.method_check(request, allowed=['get'])
    self.is_authenticated(request)
    self.throttle_check(request)
    federation = models.Federation.objects.get(pk=kwargs['id'])
    return self.create_response(request,
        requests.get(federation.url+'v1/'+kwargs['query']).json())
