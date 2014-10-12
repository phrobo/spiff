import spiff.api.plugins

SubscriptionApp = spiff.api.plugins.SpiffApp.new("spiff.inventory",
    spiff.api.plugins.find_app('spiff').version)
