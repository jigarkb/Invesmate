from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/expense_manager/transaction/add',
                  handler=ExpenseTransactionHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_manager/transaction/update',
                  handler=ExpenseTransactionHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_manager/transaction/remove',
                  handler=ExpenseTransactionHandler,
                  handler_method='remove',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_manager/account/add',
                  handler=ExpenseAccountHandler,
                  handler_method='add',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_manager/account/update',
                  handler=ExpenseAccountHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/expense_manager/account/remove',
                  handler=ExpenseAccountHandler,
                  handler_method='remove',
                  methods=['GET', 'POST']),
])
