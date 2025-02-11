from flask import Flask, current_app
from database import db
from schema import ma
from limiter import limiter, init_limiter
from caching import cache
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'E-Commerce Management System API'
    }
)

from models.user import Admin
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.account import Account

from routes.adminBP import admin_blueprint
from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.accountBP import account_blueprint


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    init_limiter(app)

    return app


def blueprint_config(app):
    app.register_blueprint(admin_blueprint, url_prefix='/api/admins')
    app.register_blueprint(customer_blueprint, url_prefix='/api/customers')
    app.register_blueprint(product_blueprint, url_prefix='/api/products')
    app.register_blueprint(order_blueprint, url_prefix='/api/orders')
    app.register_blueprint(account_blueprint, url_prefix='/api/accounts')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


def configure_rate_limit():
    if current_app.config.get('TESTING'):
        return
    
    limiter.limit('21/day')(admin_blueprint)
    limiter.limit('13/hour')(customer_blueprint)
    limiter.limit('13/minute')(product_blueprint)
    limiter.limit('7/minute')(order_blueprint)
    limiter.limit('21/hour')(account_blueprint)


if __name__ == '__main__':
    app = create_app('DevelopmentConfig')

    blueprint_config(app)
    configure_rate_limit()

    with app.app_context():
        # db.drop_all()
        db.create_all()

    app.run(debug=True)