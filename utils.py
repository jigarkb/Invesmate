from google.appengine.api import taskqueue, users
from google.appengine.ext import db

import os


def insert_in_pull_queue(queue_name, payload):
    q = taskqueue.Queue(queue_name)
    q.add((taskqueue.Task(payload=payload, method='PULL')))


def fetch_gql(query_string, fetchsize=50):
    q = db.GqlQuery(query_string)
    cursor = None
    results = []
    while True:
        q.with_cursor(cursor)
        intermediate_result = q.fetch(fetchsize)
        if len(intermediate_result) == 0:
            break
        cursor = q.cursor()
        results += intermediate_result

    return results


def authenticate_user(self, target_url, email_list=None):
    if 'http://localhost' in self.request.url:
        return 'local-user'

    user = users.get_current_user()
    if user:
        if not email_list or user.email().lower() in [email.lower() for email in email_list]:
            return user.email()
        else:
            self.response.out.write(
                "{user_email} is not authorized.  Please <a href={logout_url}>Logout</a> and re-login.".format(
                    user_email=user.email(),
                    logout_url=users.create_login_url(target_url)))
            return False

    else:
        self.response.out.write("Please <a href='{login_url}'>Login...</a>".format(
            login_url=users.create_login_url(target_url)
        ))
        return False


def authenticate_user_account(self):
    try:
        from UserAccount import UserAccount
        auth_token = self.request.cookies.get('auth_token', '')
        user_info = UserAccount.verify(auth_token=auth_token)
        return user_info
    except:
        self.redirect("/user_account/login?redirect="+self.request.url)


def template(file_name, directory="templates"):
    return os.path.join(os.path.dirname(__file__), directory, file_name)