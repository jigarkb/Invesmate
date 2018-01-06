import requests
from firebase_admin import db


class USMarket(object):
    def __init__(self):
        self.symbols = ['AAPL', 'AMD', 'FB', 'MU', 'MSFT', 'AMZN', 'GOOGL', 'TWTR', 'NVDA', 'BABA']
        self.filters = ["previousClose", "open", "latestPrice", "close"]
        self.base_api = "https://api.iextrading.com/1.0/stock/market/batch"

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


class CoinbaseMarket(object):
    def __init__(self):
        self.symbols = ['BTC-USD', 'LTC-USD', 'ETH-USD', 'BCH-USD']
        self.filters = ["previousClose", "open", "latestPrice", "close"]
        self.base_api = "https://api.coinbase.com/v2/prices/{currency_pair}/spot"

    def update(self):
        json_content = self.batch_fetch()
        coinbase_market = db.reference('/coinbase_market')
        coinbase_market.set(json_content)

    def batch_fetch(self):
        result = {}
        for currency_pair in self.symbols:
            r = requests.get(self.base_api.format(currency_pair=currency_pair))
            r = r.json()
            result[currency_pair] = {
                "quote": {
                    "latestPrice": r['data']['amount']
                }
            }
        return result

