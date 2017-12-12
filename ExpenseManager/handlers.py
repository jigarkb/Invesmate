import json
import logging
import traceback
import uuid

import datetime
import webapp2

from .models import ExpenseAccount, ExpenseTransaction
import utils


class ExpenseTransactionHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url)
        if not user_email:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            expense_trx = ExpenseTransaction()
            response = expense_trx.add(
                user_email=user_email,
                account_id=self.request.get("account_id", None),
                transaction_id=str(uuid.uuid4()),
                type=self.request.get("type", None),
                title=self.request.get("title", None),
                amount=float(self.request.get("amount", None)),
                tag=self.request.get("tag", None),
                month=int(self.request.get("month", datetime.datetime.now().month)),
                year=int(self.request.get("year", datetime.datetime.now().year)),
            )
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def fetch_all(self):
        user_email = utils.authenticate_user(self, self.request.url)
        if not user_email:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_transactions = ExpenseTransaction.get(user_email=user_email)
            response = []
            for transaction in user_transactions:
                response.append(ExpenseTransaction.get_json_object(transaction))

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def update(self):
        pass

    def remove(self):
        pass


class ExpenseAccountHandler(webapp2.RequestHandler):
    def add(self):
        user_email = utils.authenticate_user(self, self.request.url)
        if not user_email:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            expense_acc = ExpenseAccount()
            response = expense_acc.add(
                user_email=user_email,
                account_id=str(uuid.uuid4()),
                type=self.request.get("type", None),
                title=self.request.get("title", None),
                balance=float(self.request.get("balance", None)),
            )
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def fetch_all(self):
        user_email = utils.authenticate_user(self, self.request.url)
        if not user_email:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_accounts = ExpenseAccount.get(user_email=user_email)
            response = []
            for account in user_accounts:
                response.append(ExpenseAccount.get_json_object(account))

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def update(self):
        pass

    def remove(self):
        pass
