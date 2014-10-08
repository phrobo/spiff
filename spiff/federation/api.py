from models import Federation
import requests
import tastypie.resources

class FederatedModelResource(tastypie.resources.ModelResource):
  def getFederatedResources(self, query={}):
    results = {}
    for f in Federation.objects.all():
      results[f.url] = requests.get(f.url+'/v1/'+self.resource_name+'/').json()
    return results

  def get_list(self, request, **kwargs):
    l = super(FederatedModelResource, self).get_list(request, **kwargs)
    print type(l)
    return l
