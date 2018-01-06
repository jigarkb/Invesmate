import requests
from firebase_admin import db


class USMarket(object):
    def __init__(self):
        self.symbols = ['AAPL', 'AMD', 'FB', 'MU', 'MSFT', 'AMZN', 'GOOGL', 'TWTR', 'NVDA', 'BABA']
        self.filters = ["previousClose", "open", "latestPrice", "close"]
        self.base_api = "https://api.iextrading.com/1.0/stock/market/batch"

    def update(self):
        json_content = self.batch_fetch()
        us_market = db.reference('/market/us')
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
        self.symbols = ['BTC', 'LTC', 'ETH', 'BCH']
        self.currency = ['USD']
        self.base_api = "https://min-api.cryptocompare.com/data/pricemulti"

    def update(self):
        json_content = self.batch_fetch()
        coinbase_market = db.reference('/market/coinbase')
        coinbase_market.set(json_content)

    def batch_fetch(self):
        parameters = {
            "fsyms": ",".join(self.symbols),
            "e": "coinbase",
            "tsyms": ",".join(self.currency)
        }

        result = {}
        r = requests.get(self.base_api, params=parameters).json()
        for symbol in r:
            for currency in r[symbol]:
                result["{}-{}".format(symbol, currency)] = {
                    "quote": {
                        "latestPrice": r[symbol][currency]
                    }
                }
        return result

