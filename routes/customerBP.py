from flask import Blueprint
from controllers.customerController import save, find_all


customer_blueprint = Blueprint('customer_bp', __name__)

# Save a New Customer
customer_blueprint.route('/', methods=['POST'])(save)

# Get All Customers
customer_blueprint.route('/', methods=['GET'])(find_all)