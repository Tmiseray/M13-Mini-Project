from services import orderService
from flask import jsonify, request
from models.schemas.orderSchema import order_schema, orders_schema
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

    
# Save/Create New Order
@token_required
# @role_required('admin')
def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    order_save = orderService.save(order_data)
    if order_save is not None:
        return order_schema.jsonify(order_save), 201
    else:
        return jsonify({
            'status': 'error',
            'message': 'Fallback method error leted',
            'body': order_data
            }), 400
    
# Read Order Info
@token_required
# @role_required('admin')
@cache.cached(timeout=60)
def read():
    try:
        id = request.args.get('id', type=int)
        order_data = orderService.read(id)
        if order_data is not None:
            return order_schema.jsonify(order_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid order information',
                'body': order_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Update Order Data
@token_required
# @role_required('admin')
def update():
    try:
        order_data = request.json
        updated_data = orderService.update(order_data)
        if updated_data is not None:
            return order_schema.jsonify(updated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either invalid order or incomplete data',
                'body': order_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Delete Order
@token_required
@role_required('admin')
def delete():
    try:
        order_data = request.json
        deleted_data = orderService.delete(order_data)
        if deleted_data is not None:
            return order_schema.jsonify(deleted_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to delete order',
                'body': order_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Get All Orders
@token_required
@role_required('admin')
def find_all():
    orders = orderService.find_all()
    return orders_schema.jsonify(orders), 201