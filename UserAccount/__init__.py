from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/user_account/register',
                  handler=UserAccountHandler,
                  handler_method='register',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/user_account/login',
                  handler=UserAccountHandler,
                  handler_method='login',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/user_account/verify',
                  handler=UserAccountHandler,
                  handler_method='verify',
                  methods=['GET', 'POST']),
])
