from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/expense_tracker/transaction/add',
                  handler=ExpenseTransactionHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/transaction/fetch_all',
                  handler=ExpenseTransactionHandler,
                  handler_method='fetch_all',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/transaction/update',
                  handler=ExpenseTransactionHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/transaction/remove',
                  handler=ExpenseTransactionHandler,
                  handler_method='remove',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/account/add',
                  handler=ExpenseAccountHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/account/fetch_all',
                  handler=ExpenseAccountHandler,
                  handler_method='fetch_all',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/account/update',
                  handler=ExpenseAccountHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_tracker/account/remove',
                  handler=ExpenseAccountHandler,
                  handler_method='remove',
                  methods=['GET', 'POST']),
])
