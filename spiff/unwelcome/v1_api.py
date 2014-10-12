from tastypie import fields
from tastypie.resources import ModelResource
from spiff.api import SpiffAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import models

class UnwelcomePersonResource(ModelResource):
  name = fields.CharField('name')
  reason = fields.CharField('reason')
  timestamp = fields.DateTimeField('timestamp', blank=True, default=None)
  creator = fields.ToOneField('spiff.membership.v1_api.MemberResource',
      'creator')

  class Meta:
    queryset = models.UnwelcomePerson.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'name': ALL_WITH_RELATIONS,
      'reason': ALL_WITH_RELATIONS,
      'timestamp': ALL_WITH_RELATIONS
    }

  def obj_create(self, bundle, **kwargs):
    if 'creator' not in bundle.data:
      bundle.data['creator'] = bundle.request.user.member
    return super(UnwelcomePersonResource, self).obj_create(bundle, **kwargs)
