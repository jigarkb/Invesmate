import webapp2

import utils


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = utils.authenticate_user(self, self.request.url)
        if not user:
            return
        self.response.write('Hello {}!'.format(user))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
