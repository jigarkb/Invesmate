import datetime
from google.appengine.ext import db


class ExpenseTransaction(db.Model):
    user_email = db.StringProperty()
    transaction_id = db.StringProperty()
    type = db.StringProperty(choices=["credit", "debit"])
    account_id = db.StringProperty()
    title = db.StringProperty()
    amount = db.FloatProperty()
    tag = db.StringProperty()
    month = db.IntegerProperty(default=datetime.datetime.now().month, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    year = db.IntegerProperty(default=datetime.datetime.now().year)
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class ExpenseAccount(db.Model):
    user_email = db.StringProperty()
    account_id = db.StringProperty()
    title = db.StringProperty()
    type = db.StringProperty(
        choices=["credit_card", "debit_card", "checking", "savings", "cash", "prepaid_card", "wallet", "recover"])
    balance = db.FloatProperty(default=0.0)
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class UserAccount(db.Model):
    user_id = db.StringProperty()
    password_hash = db.TextProperty()
    full_name = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)


class Holding(db.Model):
    uuid = db.StringProperty()
    user_email = db.StringProperty()
    portfolio_name = db.StringProperty()
    market = db.StringProperty()
    symbol = db.StringProperty()
    shares = db.FloatProperty()
    cost_price = db.FloatProperty()
    note = db.TextProperty()
    purchased_at = db.StringProperty()

    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now=True)
