import logging
import time
import datetime
import traceback

import webapp2
from google.appengine.api import taskqueue

from .models import USMarket, CoinbaseMarket, BinanceMarket, CryptoNews
import utils


class USMarketHandler(webapp2.RequestHandler):
    def update(self):
        try:
            if datetime.datetime.now().weekday() > 4:
                return
            if self.request.method == 'GET' and "X-AppEngine-Cron" in self.request.headers:
                    taskqueue.add(
                        method='POST',
                        queue_name='default',
                        url='/data_collector/us_market/update',
                    )

            else:
                update = False
                if self.request.method == 'POST' and "X-AppEngine-QueueName" in self.request.headers:
                    update = True
                else:
                    user = utils.authenticate_user(self, self.request.url, ['jigarbhatt93@gmail.com'])
                    if user:
                        update = True

                if update:
                    start_time = time.time()
                    while True:
                        if time.time() - start_time > 9 * 60:
                            break
                        try:
                            USMarket().update()
                        except:
                            logging.error(traceback.format_exc())
                            time.sleep(2)
                        time.sleep(1)
        except:
            logging.error(traceback.format_exc())


class CoinbaseMarketHandler(webapp2.RequestHandler):
    def update(self):
        try:
            if self.request.method == 'GET' and "X-AppEngine-Cron" in self.request.headers:
                taskqueue.add(
                    method='POST',
                    queue_name='default',
                    url='/data_collector/coinbase_market/update',
                )

            else:
                update = False
                if self.request.method == 'POST' and "X-AppEngine-QueueName" in self.request.headers:
                    update = True
                else:
                    user = utils.authenticate_user(self, self.request.url, ['jigarbhatt93@gmail.com'])
                    if user:
                        update = True

                if update:
                    start_time = time.time()
                    while True:
                        if time.time() - start_time > 9 * 60:
                            break
                        try:
                            CoinbaseMarket().update()
                        except:
                            logging.error(traceback.format_exc())
                            time.sleep(2)
                        time.sleep(5)
        except:
            logging.error(traceback.format_exc())


class BinanceMarketHandler(webapp2.RequestHandler):
    def update(self):
        try:
            if self.request.method == 'GET' and "X-AppEngine-Cron" in self.request.headers:
                taskqueue.add(
                    method='POST',
                    queue_name='default',
                    url='/data_collector/binance_market/update',
                )

            else:
                update = False
                if self.request.method == 'POST' and "X-AppEngine-QueueName" in self.request.headers:
                    update = True
                else:
                    user = utils.authenticate_user(self, self.request.url, ['jigarbhatt93@gmail.com'])
                    if user:
                        update = True

                if update:
                    start_time = time.time()
                    while True:
                        if time.time() - start_time > 9 * 60:
                            break
                        try:
                            BinanceMarket().update()
                        except:
                            logging.error(traceback.format_exc())
                            time.sleep(2)
                        time.sleep(5)
        except:
            logging.error(traceback.format_exc())


class CryptoNewsHandler(webapp2.RequestHandler):
    def update(self):
        try:
            if self.request.method == 'GET' and "X-AppEngine-Cron" in self.request.headers:
                taskqueue.add(
                    method='POST',
                    queue_name='default',
                    url='/data_collector/crypto_news/update',
                )

            else:
                update = False
                if self.request.method == 'POST' and "X-AppEngine-QueueName" in self.request.headers:
                    update = True
                else:
                    user = utils.authenticate_user(self, self.request.url, ['jigarbhatt93@gmail.com'])
                    if user:
                        update = True

                if update:
                    start_time = time.time()
                    while True:
                        if time.time() - start_time > 9 * 60:
                            break
                        try:
                            CryptoNews().update()
                        except:
                            logging.error(traceback.format_exc())
                            time.sleep(60)
                        time.sleep(120)
        except:
            logging.error(traceback.format_exc())
