import logging

import model
import utils


class Holding(object):
    def __init__(self):
        pass

    def add(self, **data):
        self.check_validity(method='add', data=data)

        holding, holding_exists = self.get_datastore_entity(data)
        if holding_exists:
            raise Exception("Holding already present. Try updating it instead!")

        holding.put()

    @staticmethod
    def get(debug=False, **filters):
        query_string = "select * from Holding"

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

    @staticmethod
    def get_json_object(datastore_entity):
        json_object = {
            "uuid": datastore_entity.uuid,
            "user_email": datastore_entity.user_email,
            "portfolio_name": datastore_entity.portfolio_name,
            "market": datastore_entity.market,
            "symbol": datastore_entity.symbol,
            "shares": datastore_entity.shares,
            "cost_price": datastore_entity.cost_price,
            "purchased_at": datastore_entity.purchased_at,
            "note": datastore_entity.note,
            "modified_at": datastore_entity.modified_at.strftime('%Y-%m-%d %H:%M'),
            "created_at": datastore_entity.created_at.strftime('%Y-%m-%d %H:%M'),
        }

        return json_object

    @staticmethod
    def get_datastore_entity(json_object):
        holding_exists = True
        datastore_entity = model.Holding.get_by_key_name(json_object["uuid"])
        if not datastore_entity:
            holding_exists = False
            datastore_entity = model.Holding(key_name=json_object["uuid"])

        datastore_entity.uuid = json_object["uuid"]
        datastore_entity.user_email = json_object["user_email"]
        datastore_entity.portfolio_name = json_object["portfolio_name"]
        datastore_entity.market = json_object["market"]
        datastore_entity.symbol = json_object["symbol"]
        datastore_entity.shares = json_object["shares"]
        datastore_entity.cost_price = json_object["cost_price"]
        datastore_entity.purchased_at = json_object["purchased_at"]
        datastore_entity.note = json_object["note"]

        return datastore_entity, holding_exists

    @staticmethod
    def check_validity(method, data):
        error = []

        if error:
            raise Exception(error)
