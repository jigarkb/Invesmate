from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/portfolio',
                  handler=PortfolioHandler,
                  handler_method='dashboard',
                  methods=['GET']),

    webapp2.Route(template='/portfolio/add',
                  handler=HoldingHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/portfolio/fetch_all',
                  handler=HoldingHandler,
                  handler_method='fetch_all',
                  methods=['GET', 'POST']),
])
