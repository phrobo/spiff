import spiff.api.plugins
import spiff.local

App = spiff.api.plugins.SpiffApp.new(__name__,
    spiff.local.app.version)

app = App()
