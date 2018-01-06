from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/data_collector/us_market/update',
                  handler=USMarketHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),
])
