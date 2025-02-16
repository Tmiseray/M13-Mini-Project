from services import userService
from flask import jsonify, request
from models.schemas.userSchema import user_schema, users_schema
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

    
# Save/Create New User
def save():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    user_save = userService.save(user_data)
    if user_save is not None:
        return user_schema.jsonify(user_save), 201
    else:
        return jsonify({
            'status': 'error',
            'message': 'Fallback method error activated',
            'body': user_data
            }), 400
    
# Read User Info
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def read():
    try:
        id = request.args.get('id', type=int)
        user_data = userService.read(id)
        if user_data is not None:
            return user_schema.jsonify(user_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid admin information',
                'body': user_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Update User Data
@token_required
@role_required('admin')
def update():
    try:
        user_data = request.json
        updated_data = userService.update(user_data)
        if updated_data is not None:
            return user_schema.jsonify(updated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either invalid admin or incomplete data',
                'body': user_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Delete/Deactivate
@token_required
@role_required('admin')
def deactivate():
    try:
        user_data = request.json
        deactivated_data = userService.deactivate(user_data)
        if deactivated_data is not None:
            return user_schema.jsonify(deactivated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to deactivate user',
                'body': user_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Get All Users
@token_required
@role_required('admin')
def find_all():
    users = userService.find_all()
    return users_schema.jsonify(users), 201

# Get All Admin Users
@token_required
@role_required('admin')
def find_all_admins():
    admins = userService.find_all_admins()
    return users_schema.jsonify(admins), 201

# Get All Customer Users
@token_required
@role_required('admin')
def find_all_customers():
    customers = userService.find_all_customers()
    return users_schema.jsonify(customers), 201
