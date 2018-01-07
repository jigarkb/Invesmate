import webapp2

import utils


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/portfolio")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
