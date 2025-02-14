from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required


# Save New Customer Data
# @token_required
# @role_required('admin')
def save():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    customer_save = customerService.save(customer_data)
    if customer_save is not None:
        return customer_schema.jsonify(customer_save), 201
    else:
        return jsonify({
            'status': 'error',
            'message': 'Fallback method error activated',
            'body': customer_data
            }), 400
    
# Read Customer Info
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def read():
    try:
        id = request.args.get('customerId', type=int)
        customer_data = customerService.read(id)
        if customer_data is not None:
            return customer_schema.jsonify(customer_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid customer information',
                'body': customer_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Update Customer Data
@token_required
def update():
    try:
        customer_data = request.json
        updated_data = customerService.update(customer_data)
        if updated_data is not None:
            return customer_schema.jsonify(updated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either invalid customer or incomplete data',
                'body': customer_data
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
        customer_data = request.json
        deactivated_data = customerService.deactivate(customer_data)
        if deactivated_data is not None:
            return customer_schema.jsonify(deactivated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to deactivate customer',
                'body': customer_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404

# Get All Customers
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200