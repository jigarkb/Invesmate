import logging

import requests
from firebase_admin import db


class USMarket(object):
    def __init__(self):
        self.symbols = ['AAPL', 'AMD', 'FB', 'MU', 'MSFT', 'AMZN', 'GOOGL', 'TWTR', 'NVDA', 'BABA', 'INTC', 'INFY']
        self.filters = ["previousClose", "open", "latestPrice", "close"]
        self.base_api = "https://api.iextrading.com/1.0/stock/market/batch"

    def update(self):
        json_content = self.batch_fetch()
        us_market = db.reference('/market/us')
        us_market.set(json_content)

    def batch_fetch(self):
        parameters = {
            "last": 5,
            "symbols": ",".join(self.symbols),
            "types": "quote,news"
        }

        r = requests.get(self.base_api, params=parameters)
        return r.json()


class CoinbaseMarket(object):
    def __init__(self):
        self.symbols = ['BTC', 'LTC', 'ETH', 'BCH']
        self.currency = ['USD']
        self.base_api = "https://min-api.cryptocompare.com/data/pricemultifull"

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
        r = requests.get(self.base_api, params=parameters).json()['RAW']
        for symbol in r:
            for currency in r[symbol]:
                result["{}-{}".format(symbol, currency)] = {
                    "quote": {
                        "latestPrice": r[symbol][currency]['PRICE'],
                        "open": r[symbol][currency]['OPEN24HOUR'],
                        "previousClose": r[symbol][currency]['OPEN24HOUR'],
                        "close": r[symbol][currency]['PRICE'],
                    }
                }
        return result


class BinanceMarket(object):
    def __init__(self):
        self.symbols = ['IOT', 'ADA']
        self.currency = ['BTC']
        self.base_api = "https://min-api.cryptocompare.com/data/pricemultifull"

    def update(self):
        json_content = self.batch_fetch()
        binance_market = db.reference('/market/binance')
        binance_market.set(json_content)

    def batch_fetch(self):
        parameters = {
            "fsyms": ",".join(self.symbols),
            "e": "binance",
            "tsyms": ",".join(self.currency)
        }

        result = {}
        r = requests.get(self.base_api, params=parameters).json()['RAW']
        for symbol in r:
            for currency in r[symbol]:
                result["{}-{}".format(symbol, currency)] = {
                    "quote": {
                        "latestPrice": r[symbol][currency]['PRICE'],
                        "open": r[symbol][currency]['OPEN24HOUR'],
                        "previousClose": r[symbol][currency]['OPEN24HOUR'],
                        "close": r[symbol][currency]['PRICE'],
                    }
                }
        return result


class CryptoNews(object):
    def __init__(self):
        self.base_api = "https://min-api.cryptocompare.com/data/news/"

    def update(self):
        json_content = self.batch_fetch()
        crypto_news = db.reference('/crypto/news')
        crypto_news.set(json_content)

    def batch_fetch(self):
        parameters = {}

        r = requests.get(self.base_api, params=parameters).json()
        logging.error(r)
        result = r[:10]
        return result
