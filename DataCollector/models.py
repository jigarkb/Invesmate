import requests
from firebase_admin import db


class USMarket(object):
    def __init__(self):
        self.symbols = ['AAPL', 'AMD', 'FB', 'MU', 'MSFT', 'AMZN', 'GOOGL', 'TWTR', 'NVDA', 'BABA']
        self.filters = ["previousClose", "open", "latestPrice", "close"]
        self.base_api = "https://api.iextrading.com/1.0/stock/market/batch"
        self.firebase_data_structure = {
            "$quote": {
                "previousClose": 0,
                "open": 0,
                "latestPrice": 0,
                "close": 0,
            }
        }

    def update(self):
        json_content = self.batch_fetch()
        us_market = db.reference('/us_market')
        us_market.set(json_content)

    def batch_fetch(self):
        parameters = {
            "filter": ",".join(self.filters),
            "symbols": ",".join(self.symbols),
            "types": "quote"
        }

        r = requests.get(self.base_api, params=parameters)
        return r.json()




