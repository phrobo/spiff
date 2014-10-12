import spiff.api.plugins

SubscriptionApp = spiff.api.plugins.SpiffApp.new("spiff.subscription",
    spiff.api.plugins.find_app('spiff').version)
