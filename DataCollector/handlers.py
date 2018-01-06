import time
import webapp2
from google.appengine.api import taskqueue

from .models import USMarket, CoinbaseMarket
import utils


class USMarketHandler(webapp2.RequestHandler):
    def update(self):
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
                    USMarket().update()
                    time.sleep(0.5)


class CoinbaseMarketHandler(webapp2.RequestHandler):
    def update(self):
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
                    CoinbaseMarket().update()
                    time.sleep(0.5)
