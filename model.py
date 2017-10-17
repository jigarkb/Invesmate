from google.appengine.ext import db


class ExpenseTransaction(db.Model):
    user_email = db.StringProperty()
    transaction_id = db.StringProperty()

    type = db.StringProperty(choices=["credit", "debit"])
    account_id = db.StringProperty()
    title = db.StringProperty()
    amount = db.FloatProperty()
    tag = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class ExpenseAccount(db.Model):
    user_email = db.StringProperty()
    account_id = db.StringProperty()

    title = db.StringProperty()
    type = db.StringProperty(choices=["credit_card", "debit_card", "checking", "savings", "cash", "prepaid_card", "wallet"])
    balance = db.FloatProperty(default=0.0)
