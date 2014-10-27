from tastypie import fields
from spiff.api import SpiffAuthorization
from tastypie.resources import ModelResource
import models

class TrainingResource(ModelResource):
  identity = fields.ToOneField('spiff.identity.v1_api.IdentityResource', 'identity', full=True)
  resource = fields.ToOneField('spiff.inventory.v1_api.ResourceResource', 'resource')
  rank = fields.CharField('comment', blank=True)

  class Meta:
    authorization = SpiffAuthorization()
    always_return_data = True
    queryset = models.Certification.objects.all()
    filtering = {
      'resource': 'exact'
    }

class ResourceMetadataResource(ModelResource):
  name = fields.CharField('name')
  value = fields.CharField('value')
  resource = fields.ToOneField('spiff.inventory.v1_api.ResourceResource', 'resource')

  class Meta:
    authorization = SpiffAuthorization()
    queryset = models.Metadata.objects.all()
    always_return_data = True
    filtering = {
      'resource': 'exact'
    }

  def obj_create(self, bundle, **kwargs):
    bundle = super(ResourceMetadataResource, self).obj_create(
      bundle, **kwargs)
    bundle.obj.resource.logChange(
      identity=bundle.request.identity,
      property=bundle.obj.name,
      new=bundle.obj.value)
    return bundle

  def obj_update(self, bundle, **kwargs):
    oldVal = bundle.obj.value
    bundle = super(ResourceMetadataResource, self).obj_update(
      bundle, **kwargs)
    bundle.obj.resource.logChange(
      identity=bundle.request.identity,
      property=bundle.obj.name,
      new=bundle.obj.value,
      old=oldVal)
    return bundle

  def obj_delete(self, bundle, **kwargs):
    oldMeta = models.Metadata.objects.get(pk=kwargs['pk'])
    oldName = oldMeta.name
    oldValue = oldMeta.value
    oldIdentity = bundle.request.identity
    bundle = super(ResourceMetadataResource, self).obj_delete(
      bundle, **kwargs)
    oldMeta.resource.logChange(
      identity=oldIdentity,
      property=oldName,
      old=oldValue,
      new=None)
    return bundle

class ChangelogResource(ModelResource):
  identity = fields.ToOneField('spiff.identity.v1_api.IdentityResource', 'identity', full=True)
  old = fields.CharField('old', null=True)
  new = fields.CharField('new', null=True)
  property = fields.CharField('property', null=True)
  stamp = fields.DateTimeField('stamp')

  class Meta:
    queryset = models.Change.objects.all()
    authorization = SpiffAuthorization()
    always_return_data = True
    filtering = {
      'resource': 'exact'
    }

class ResourceResource(ModelResource):
  name = fields.CharField('name')
  metadata = fields.ToManyField(ResourceMetadataResource, 'metadata', full=True,
      null=True)

  class Meta:
    queryset = models.Resource.objects.all()
    resource_name = 'resource'
    always_return_data = True
    authorization = SpiffAuthorization()
