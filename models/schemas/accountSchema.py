from marshmallow import fields
from schema import ma

class AccountSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=False)
    accountId = fields.Integer(required=True)

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)