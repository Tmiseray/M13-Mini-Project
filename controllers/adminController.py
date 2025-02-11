from services import adminService
from flask import jsonify, request
from models.schemas.adminSchema import admin_schema, admins_schema
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

    
# Save/Create New Admin
# @token_required
# @role_required('admin')
def save():
    try:
        user_data = admin_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    admin_save = adminService.save(user_data)
    if admin_save is not None:
        return admin_schema.jsonify(admin_save), 201
    else:
        return jsonify({
            'status': 'error',
            'message': 'Fallback method error activated',
            'body': user_data
            }), 400
    
# Read Admin Info
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def read():
    try:
        id = request.args.get('id', type=int)
        admin_data = adminService.read(id)
        if admin_data is not None:
            return admin_schema.jsonify(admin_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid admin information',
                'body': admin_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Update admin Data
@token_required
@role_required('admin')
def update():
    try:
        admin_data = request.json
        updated_data = adminService.update(admin_data)
        if updated_data is not None:
            return admin_schema.jsonify(updated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either invalid admin or incomplete data',
                'body': admin_data
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
        admin_data = request.json
        deactivated_data = adminService.deactivate(admin_data)
        if deactivated_data is not None:
            return admin_schema.jsonify(deactivated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to deactivate admin',
                'body': admin_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Get All admins
@token_required
@role_required('admin')
def find_all():
    admins = adminService.find_all()
    return admins_schema.jsonify(admins), 201
