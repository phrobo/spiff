from tastypie import fields
import requests
from tastypie.resources import Resource
from spiff.api import SpiffAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
import models
from django.conf.urls import url
from tastypie.utils import trailing_slash
import spiff.api.plugins

class AppResource(Resource):
  id = fields.CharField('id')
  version = fields.CharField('version')

  class Meta:
    resource_name = 'app'
    object_class = spiff.api.plugins.SpiffApp

  def obj_get_list(self, bundle, **kwargs):
    return spiff.api.plugins.find_apps()

  def obj_get(self, bundle, **kwargs):
    return spiff.api.plugins.find_app(kwargs['pk'])
