from services import accountService
from flask import jsonify, request
from models.schemas.accountSchema import account_schema, accounts_schema
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required


# Account Login
def login():
    userRequest = request.json
    account = accountService.login(userRequest['username'], userRequest['password'])
    if account:
        return jsonify(account), 200
    else:
        response = {
            'status': 'error',
            'message': 'Account does not exist'
        }
        return jsonify(response), 400
    
# Save/Create New Account
# @token_required
# @role_required('admin')
def save():
    try:
        user_data = account_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    account_save = accountService.save(user_data)
    if account_save is not None:
        return account_schema.jsonify(account_save), 201
    else:
        return jsonify({
            'status': 'error',
            'message': 'Fallback method error activated',
            'body': user_data
            }), 400
    
# Read Account Info
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def read():
    try:
        id = request.args.get('accountId', type=int)
        account_data = accountService.read(id)
        if account_data is not None:
            return account_schema.jsonify(account_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid account information',
                'body': account_data
            }), 400
    except Exception as e:
        return jsonify(e.messages), 404
    
# Update Account Data
@token_required
def update():
    try:
        account_data = request.json
        updated_data = accountService.update(account_data)
        if updated_data is not None:
            return account_schema.jsonify(updated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either invalid account or incomplete data',
                'body': account_data
            }), 400
    except Exception as e:
        return jsonify(e.messages), 404
    
# Delete/Deactivate
@token_required
@role_required('admin')
def deactivate():
    try:
        account_data = request.json
        deactivated_data = accountService.deactivate(account_data)
        if deactivated_data is not None:
            return account_schema.jsonify(deactivated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to deactivate account',
                'body': account_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Get All Accounts
@token_required
@role_required('admin')
def find_all():
    accounts = accountService.find_all()
    return accounts_schema.jsonify(accounts), 201
