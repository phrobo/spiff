import spiff.api.plugins
import models
import spiff.local
from django.conf import settings

class App(spiff.api.plugins.SpiffApp):
  def __init__(self):
    super(App, self).__init__(__name__, 
      spiff.local.app.version)

  def filterSpaceAPI(self, api):
    if settings.SPACEAPI_OPEN_SENSOR_ID is not None:
      sensor = models.Sensor.objects.get(id=settings.SPACEAPI_OPEN_SENSOR_ID)
      if sensor.value() is not None:
        api['open'] = bool(sensor.value())
      api['x-spiff-open-sensor'] = sensor.id

    sensors = {}
    for t in models.SENSOR_TYPES:
      sensors[t[1]] = []
      for s in models.Sensor.objects.filter(type=t[0]):
        v = s.value()
        sensors[t[1]].append({s.name: v})
    if 'sensors' not in api:
      api['sensors'] = {}
    api['sensors'].update(sensors)
    return api

app = App()
