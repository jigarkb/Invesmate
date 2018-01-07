import json
import logging
import traceback
import uuid

import datetime
import webapp2
from google.appengine.ext.webapp import template

from .models import Holding
import utils


class PortfolioHandler(webapp2.RedirectHandler):
    def dashboard(self):
        user_info = utils.authenticate_user_account(self)
        if not user_info:
            return

        template_values = {
            "user": user_info["full_name"],
            "config": {
                "apiKey": "AIzaSyDjLVEBgIWBZvN15eqhppSpV2zJEMGGPPo",
                "authDomain": "brainstorm-cloud.firebaseapp.com",
                "databaseURL": "https://brainstorm-cloud.firebaseio.com",
                "projectId": "brainstorm-cloud",
                "storageBucket": "brainstorm-cloud.appspot.com",
                "messagingSenderId": "244652867281"
            },
            "date_str": datetime.datetime.now().strftime('%Y-%m-%d'),
        }
        page = utils.template("dashboard.html", "Portfolio/html")
        self.response.out.write(template.render(page, template_values))


class HoldingHandler(webapp2.RequestHandler):
    def add(self):
        user_info = utils.authenticate_user_account(self)
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
        user_info = utils.authenticate_user_account(self)
        if not user_info:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            user_holdings = Holding.get(user_email=user_info["user_id"])
            position_index = {}
            positions = []
            i = -1
            cost_price = 0
            for holding in user_holdings:
                cost_price += holding.cost_price
                key_name = "market/{}/{}".format(holding.market.lower(), holding.symbol)
                if key_name not in position_index:
                    i += 1
                    position_index[key_name] = i
                    positions.append({
                        "symbol": holding.symbol,
                        "market": holding.market,
                        "shares": holding.shares,
                        "cost_price": holding.cost_price,
                        "cost_price_ps": holding.cost_price/float(holding.shares),
                        "market_price": -1,
                        "market_price_ps": -1,
                        "overall_change": -1,
                        "24hr_change": -1,
                        "overall_change_%": -1,
                        "24hr_change_%": -1,
                        "lots": [{
                            "uuid": holding.uuid,
                            "purchased_at": holding.purchased_at,
                            "shares": holding.shares,
                            "cost_price": holding.cost_price,
                            "cost_price_ps": holding.cost_price/float(holding.shares),
                            "market_price": -1,
                            "market_price_ps": -1,
                            "overall_change": -1,
                            "24hr_change": -1,
                            "overall_change_%": -1,
                            "24hr_change_%": -1,
                            "portfolio_name": holding.portfolio_name,
                            "note": holding.note,
                        }],
                    })
                else:
                    position = positions[position_index[key_name]]
                    position["shares"] += holding.shares
                    position["cost_price"] += holding.cost_price
                    position["cost_price_ps"] = position["cost_price"]/float(position["shares"])
                    position["lots"].append({
                        "uuid": holding.uuid,
                        "purchased_at": holding.purchased_at,
                        "shares": holding.shares,
                        "cost_price": holding.cost_price,
                        "cost_price_ps": holding.cost_price/float(holding.shares),
                        "market_price": -1,
                        "market_price_ps": -1,
                        "overall_change": -1,
                        "24hr_change": -1,
                        "overall_change_%": -1,
                        "24hr_change_%": -1,
                        "portfolio_name": holding.portfolio_name,
                        "note": holding.note,
                    })
            response = {
                "cost_price": cost_price,
                "market_price": -1,
                "overall_change": -1,
                "24hr_change": -1,
                "overall_change_%": -1,
                "24hr_change_%": -1,
                "positions": positions,
                "position_index": position_index,
            }
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': response}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())