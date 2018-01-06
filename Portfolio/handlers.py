import json
import logging
import traceback
import uuid

import datetime
import webapp2

from .models import Holding
import utils


class HoldingHandler(webapp2.RequestHandler):
    def add(self):
        user_info = utils.authenticate_user_account(self.request)
        if not user_info:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            holding = Holding()
            response = holding.add(
                uuid=uuid.uuid4().hex,
                user_email=user_info["user_id"],
                portfolio_name=self.request.get("portfolio_name", "default"),
                market=self.request.get("market", ""),
                symbol=self.request.get("symbol", None),
                shares=float(self.request.get("shares", None)),
                cost_price=float(self.request.get("cost_price", None)),
                note=self.request.get("note", None),
                purchased_at=self.request.get("purchased_at", datetime.datetime.now().strftime("%Y-%m-%d")),
            )
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())

    def fetch_all(self):
        user_info = utils.authenticate_user_account(self.request)
        if not user_info:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_holdings = Holding.get(user_email=user_info["user_id"])
            response = {}
            for holding in user_holdings:
                obj = Holding.get_json_object(holding)
                response[obj["portfolio_name"]] = response.get(obj["portfolio_name"], [])
                response[obj["portfolio_name"]].append(obj)

            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())