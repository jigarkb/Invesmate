import traceback

import webapp2
from google.appengine.ext.webapp import template
from passlib.hash import pbkdf2_sha256

from .models import *


class UserAccountHandler(webapp2.RequestHandler):
    def login(self):
        page = utils.template("login.html", "UserAccount/html")
        template_values = {}
        if self.request.method == 'GET':
            self.response.set_cookie("redirect", self.request.get("redirect", ""))
            self.response.out.write(template.render(page, template_values))
        else:
            try:
                user_id = self.request.get("user_id", None)
                password = self.request.get("password", None)

                user_account = UserAccount()
                response = user_account.login(
                    user_id=user_id,
                    password=password,
                )

                if not response:
                    raise Exception('Email or Password is invalid!')

                self.response.set_cookie('auth_token', response['auth_token'])
                redirect = str(self.request.cookies.get("redirect"))
                if not redirect:
                    redirect = "/"
                self.redirect(redirect)
            except Exception as e:
                template_values.update({"error": e.message})
                self.response.out.write(template.render(page, template_values))
                logging.error(traceback.format_exc())

    def register(self):
        page = utils.template("register.html", "UserAccount/html")
        template_values = {}
        if self.request.method == 'GET':
            self.response.set_cookie("redirect", self.request.get("redirect", ""))
            self.response.out.write(template.render(page, template_values))
        else:
            try:
                user_id = self.request.get("user_id", None)
                password = self.request.get("password", None)
                full_name = self.request.get("full_name", None)

                user_account = UserAccount()
                response = user_account.register(
                    user_id=user_id,
                    password=password,
                    full_name=full_name,
                )
                self.response.set_cookie('auth_token', response['auth_token'])
                redirect = str(self.request.cookies.get("redirect"))
                if not redirect:
                    redirect = "/"
                self.redirect(redirect)
            except Exception as e:
                template_values.update({"error": e.message})
                self.response.out.write(template.render(page, template_values))
                logging.error(traceback.format_exc())

    def verify(self):
        user_info = utils.authenticate_user_account(self.request)
        if not user_info:
            return

        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Access-Control-Allow-Origin'] = '*'

        try:
            self.response.out.write(json.dumps({'success': True, 'error': [], 'response': user_info}))
        except Exception as e:
            self.response.out.write(json.dumps({'success': False, 'error': e.message, 'response': None}))
            logging.error(traceback.format_exc())
