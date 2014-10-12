import spiff.api.plugins

SubscriptionApp = spiff.api.plugins.SpiffApp.new("spiff.unwelcome",
    spiff.api.plugins.find_app('spiff').version)

