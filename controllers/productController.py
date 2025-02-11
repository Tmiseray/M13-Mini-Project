from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required


# Save New Product Data
@token_required
@role_required('admin')
def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    product_save = productService.save(product_data)
    if product_save is not None:
        return product_schema.jsonify(product_save), 201
    else:
        return jsonify({
            'status': 'error',
            'message': 'Fallback method error activated',
            'body': product_data
            }), 400
    
# Read Product Info
@token_required
# @role_required('admin')
@cache.cached(timeout=60)
def read():
    try:
        id = request.args.get('productId', type=int)
        product_data = productService.read(id)
        if product_data is not None:
            return product_schema.jsonify(product_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid product information',
                'body': product_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404
    
# Update Product Data
@token_required
@role_required('admin')
def update():
    try:
        product_data = request.json
        updated_data = productService.update(product_data)
        if updated_data is not None:
            return product_schema.jsonify(updated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either invalid product or incomplete data',
                'body': product_data
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
        product_data = request.json
        deactivated_data = productService.deactivate(product_data)
        if deactivated_data is not None:
            return product_schema.jsonify(deactivated_data), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to deactivate product',
                'body': product_data
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'exception error',
            'message': e
        }), 404

# Get All products
@token_required
# @role_required('admin')
@cache.cached(timeout=60)
def find_all():
    products = productService.find_all()
    return products_schema.jsonify(products), 200