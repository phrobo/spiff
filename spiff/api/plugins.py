from django.conf import settings
import importlib
import inspect

class SpiffApp(object):
  def __init__(self, id=None, version=None):
    self.id = id;
    self.version = version

  @classmethod
  def new(cls, id, version):
    class AppClass(SpiffApp):
      def __init__(self):
        super(AppClass, self).__init__(id, version)
    return AppClass

def find_api_classes(*args, **kwargs):
  for app, cls in find_api_implementations(*args, **kwargs):
    yield cls

def find_api_implementations(module, superclass, test=lambda x: True):
  for app in map(lambda x:'%s.%s'%(x, module), settings.INSTALLED_APPS):
    try:
      appAPI = importlib.import_module(app)
    except ImportError:
      continue
    for name, cls in inspect.getmembers(appAPI):
      if inspect.isclass(cls) and issubclass(cls, superclass) and not cls is superclass and test(cls):
        yield (app, cls)

def find_apps():
  return [x[1]() for x in find_api_implementations('app', SpiffApp)]

def find_app(id):
  ret = list(find_api_classes('app', SpiffApp, lambda x:x().id==id))
  if len(ret):
    return ret[0]()
  raise KeyError("Unknown app "+repr(id))
