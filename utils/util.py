from datetime import datetime, timedelta
from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()
SECRETKEY = os.getenv('SECRETKEY')

def encode_token(userId, roleName):
    payload = {
        'exp': datetime.now() + timedelta(days=0, hours=1),
        'iat': datetime.now(),
        'sub': userId,
        'role': roleName
    }
    token = jwt.encode(payload, SECRETKEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
                print("Token:", token)
                payload = jwt.decode(token, SECRETKEY, algorithms="HS256")
                print(payload['sub'])
            except jwt.ExpiredSignatureError:
                return jsonify({ 'message': 'Token has expired', 'error': 'Unauthorized' }), 401
            except jwt.InvalidTokenError:
                return jsonify({ 'message': 'Invalid token', 'error': 'Unauthorized' }), 401
        if not token:
            return jsonify({ 'message': 'Authentication Token is missing', 'error': 'Unauthorized' }), 401
        
        return f(*args, *kwargs)
    
    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return jsonify({ 'message': 'Token is missing' }), 401
            
            try:
                payload = jwt.decode(token, SECRETKEY, algorithms="HS256")
            except jwt.ExpiredSignatureError:
                return jsonify({ 'message': 'Token has expired', 'error': 'Unauthorized' }), 401
            except jwt.InvalidTokenError:
                return jsonify({ 'message': 'Invalid token', 'error': 'Unauthorized' }), 401
            
            payloadRole = payload['role']

            if payloadRole != 'admin':
                return jsonify({ 'message': 'User does not have the required role', "error": "Unauthorized" }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator