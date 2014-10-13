import spiff.local
import spiff.donations

App = spiff.api.plugins.SpiffApp.new(__name__,
    spiff.local.app.version)

app = App()
