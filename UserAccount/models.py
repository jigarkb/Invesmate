import datetime
import json

import logging

import model
import utils
from passlib.hash import pbkdf2_sha256
from jose import jws


class UserAccount(object):
    def __init__(self):
        pass

    def get(self, debug=False, **filters):
        query_string = "select * from UserAccount"

        filters = {key: val for key, val in filters.iteritems() if val != None}

        i = 0
        for field in filters:
            if i == 0:
                query_string += " where "

            if i < len(filters) - 1:
                query_string += "%s='%s' and " % (field, filters[field])
            else:
                query_string += "%s='%s'" % (field, filters[field])
            i += 1

        response = utils.fetch_gql(query_string)
        if debug:
            logging.error("Query String: %s\n\n Response Length: %s" % (query_string, len(response)))

        return response

    def fetch_all(self):
        all_entries = self.get()

        response = []
        for entry in all_entries:
            response.append(self.get_json_object(entry))

        return response

    def register(self, **data):
        password_hash = pbkdf2_sha256.hash(data["password"])
        datastore_entity, entity_exists = self.get_datastore_entity({
            "user_id": data["user_id"],
            "password_hash": password_hash,
            "full_name": data["full_name"],
        })
        if entity_exists:
            raise Exception("User ID already exists!")

        datastore_entity.put()
        auth_token = jws.sign(
            json.dumps({"user_id": datastore_entity.user_id, "full_name": datastore_entity.full_name}),
            'insecure secret', algorithm='HS256')
        return {"auth_token": auth_token, "full_name": datastore_entity.full_name}

    @staticmethod
    def login(**data):
        datastore_entity = model.UserAccount.get_by_key_name(data["user_id"])
        if not datastore_entity:
            raise Exception("User ID does not exists!")

        if pbkdf2_sha256.verify(data["password"], datastore_entity.password_hash):
            auth_token = jws.sign(
                json.dumps({"user_id": datastore_entity.user_id, "full_name": datastore_entity.full_name}),
                'insecure secret', algorithm='HS256')
            return {"auth_token": auth_token, "full_name": datastore_entity.full_name}

        return None

    @staticmethod
    def verify(**data):
        return json.loads(jws.verify(data['auth_token'], 'insecure secret', algorithms=['HS256']))

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "user_id": datastore_entity.user_id,
            "password_hash": datastore_entity.password_hash,
            "full_name": datastore_entity.full_name,
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        entity_exists = True
        datastore_entity = model.UserAccount.get_by_key_name(json_object["user_id"])
        if not datastore_entity:
            entity_exists = False
            datastore_entity = model.UserAccount(key_name=json_object["user_id"])

        datastore_entity.user_id = json_object["user_id"]
        datastore_entity.full_name = json_object["full_name"]
        datastore_entity.password_hash = json_object["password_hash"]

        return datastore_entity, entity_exists
