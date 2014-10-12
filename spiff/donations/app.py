import spiff.api.plugins
import spiff.local.app
import spiff.donations

DonationsApp = spiff.api.plugins.SpiffApp.new("spiff.donations",
    spiff.api.plugins.find_app('spiff').version)
