import tastypie.resources
import tastypie.api
import spiff.api.plugins

v1_api = tastypie.api.Api(api_name='v1')
for api in spiff.api.plugins.find_api_classes('v1_api', tastypie.resources.Resource, lambda x:hasattr(x, 'Meta')):
  v1_api.register(api())

