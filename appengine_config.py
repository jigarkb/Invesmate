from google.appengine.ext import vendor
vendor.add('Library')
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

import os
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "Keys", "firebase-adminsdk.json"))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://brainstorm-cloud.firebaseio.com'
})
