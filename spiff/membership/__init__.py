import spiff.api.plugins
from spiff.membership.models import Rank
import spiff.local

class App(spiff.api.plugins.SpiffApp):
  def __init__(self):
    super(App, self).__init__(__name__,
      spiff.local.app.version)

  def filterSpaceAPI(self, api):

    keyholders = []
    for r in Rank.objects.filter(isKeyholder=True):
      for u in r.group.user_set.all():
        keyholders.append(str(u.member))

    api['contact']['keymaster'] = keyholders
    return api;

app = App()

