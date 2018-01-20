from .handlers import *

app = webapp2.WSGIApplication([
    webapp2.Route(template='/data_collector/us_market/update',
                  handler=USMarketHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/data_collector/coinbase_market/update',
                  handler=CoinbaseMarketHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/data_collector/binance_market/update',
                  handler=BinanceMarketHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),

    webapp2.Route(template='/data_collector/crypto_news/update',
                  handler=CryptoNewsHandler,
                  handler_method='update',
                  methods=['GET', 'POST']),
])
