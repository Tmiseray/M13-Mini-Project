from marshmallow import fields
from schema import ma


class UserSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    role = fields.String(required=False, default='user')
    isActive = fields.Boolean(dump_only=True, default=True)

    class Meta:
        fields = ('id', 'name', 'email', 'phone', 'role', 'isActive')


user_schema = UserSchema()
users_schema = UserSchema(many=True)