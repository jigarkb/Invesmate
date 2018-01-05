import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import utils

cred = credentials.Certificate(utils.template("firebase-adminsdk.json", "Keys"))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://brainstorm-cloud.firebaseio.com'
})

