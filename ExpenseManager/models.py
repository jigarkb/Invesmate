import model


class ExpenseTransaction(object):
    def __init__(self):
        pass

    def add(self, **data):
        self.check_validity(method='add', data=data)

        tracker, tracker_exists = self.get_datastore_entity(data)
        if tracker_exists:
            raise Exception("Transaction already present. Try updating it instead!")

        ExpenseAccount().transact(
            user_email=tracker.user_email,
            account_id=tracker.account_id,
            transaction_id=tracker.transaction_id,
            transaction_type=tracker.type,
            amount=tracker.amount,
        )

        tracker.put()

    @staticmethod
    def get_datastore_entity(json_object):
        transaction_exists = True
        datastore_entity = model.ExpenseTransaction.get_by_key_name(json_object["transaction_id"])
        if not datastore_entity:
            transaction_exists = False
            datastore_entity = model.ExpenseTransaction(key_name=json_object["transaction_id"])

        datastore_entity.account_id = json_object["account_id"]
        datastore_entity.user_email = json_object["user_email"]
        datastore_entity.transaction_id = json_object["transaction_id"]
        datastore_entity.type = json_object["type"]
        datastore_entity.title = json_object["title"]
        datastore_entity.amount = json_object["amount"]
        datastore_entity.tag = json_object["tag"]

        return datastore_entity, transaction_exists

    @staticmethod
    def check_validity(method, data):
        error = []

        valid_transaction_type = ['credit', 'debit']

        if method == "add":
            if not data.get('user_email', None):
                error.append({"attribute_name": "user_email", "err_msg": "'user_email' cannot be blank"})

            if not data.get('account_id', None):
                error.append({"attribute_name": "account_id", "err_msg": "'account_id' cannot be blank"})

            if not data.get('title', None):
                error.append({"attribute_name": "title", "err_msg": "'title' cannot be blank"})

            if not data.get('tag', None):
                error.append({"attribute_name": "tag", "err_msg": "'tag' cannot be blank"})

            if type(data.get("amount")) != float:
                error.append({"attribute_name": "amount", "err_msg": "'amount' should be float"})

            if data.get("type", None) not in valid_transaction_type:
                error.append({"attribute_name": "type", "err_msg": "'type' should be one of: {}".format(valid_transaction_type)})

        if error:
            raise Exception(error)


class ExpenseAccount(object):
    def __init__(self):
        pass

    def add(self, **data):
        self.check_validity(method='add', data=data)

        expense_account, expense_account_exists = self.get_datastore_entity(data)
        if expense_account_exists:
            raise Exception("Expense account already present. Try updating it instead!")

        expense_account.put()

    def transact(self, **data):
        self.check_validity("transact", data)
        key_name = "{}/{}".format(data["user_email"], data["account_id"])

        expense_account = model.ExpenseAccount.get_by_key_name(key_name)
        if not expense_account:
            raise Exception("Expense account {} for {} does not exist".format(data["account_id"], data["user_email"]))

        if data["transaction_type"] == "credit":
            expense_account.balance += data["amount"]
        else:
            expense_account.balance -= data["amount"]

        expense_account.put()

    @staticmethod
    def get_datastore_entity(json_object):
        transaction_exists = True
        key_name = "{}/{}".format(json_object["user_email"], json_object["account_id"])
        datastore_entity = model.ExpenseAccount.get_by_key_name(key_name)
        if not datastore_entity:
            transaction_exists = False
            datastore_entity = model.ExpenseAccount(key_name=key_name)

        datastore_entity.account_id = json_object["account_id"]
        datastore_entity.user_email = json_object["user_email"]
        datastore_entity.title = json_object["title"]
        datastore_entity.balance = json_object["balance"]
        datastore_entity.type = json_object["type"]

        return datastore_entity, transaction_exists

    @staticmethod
    def check_validity(method, data):
        error = []

        valid_transaction_type = ['credit', 'debit']
        valid_account_type = ["credit_card", "debit_card", "checking", "savings", "cash", "prepaid_card", "wallet"]

        if method == "add":
            if not data.get('account_id', None):
                error.append({"attribute_name": "account_id", "err_msg": "'account_id' cannot be blank"})

            if not data.get('user_email', None):
                error.append({"attribute_name": "user_email", "err_msg": "'user_email' cannot be blank"})

            if type(data.get('balance', None)) != float:
                error.append({"attribute_name": "balance", "err_msg": "'balance' should be float"})

            if not data.get('title', None):
                error.append({"attribute_name": "title", "err_msg": "'title' cannot be blank"})

            if data.get("type", None) not in valid_account_type:
                error.append({"attribute_name": "type", "err_msg": "'type' should be one of: {}".format(valid_account_type)})

        elif method == "transact":
            if not data.get('account_id', None):
                error.append({"attribute_name": "account_id", "err_msg": "'account_id' cannot be blank"})

            if not data.get('user_email', None):
                error.append({"attribute_name": "user_email", "err_msg": "'user_email' cannot be blank"})

            if type(data.get("amount")) != float:
                error.append({"attribute_name": "amount", "err_msg": "'amount' should be float"})

            if data.get("transaction_type", None) not in valid_transaction_type:
                error.append({"attribute_name": "transaction_type", "err_msg": "'transaction_type' should be one of: {}".format(valid_transaction_type)})

        if error:
            raise Exception(error)
