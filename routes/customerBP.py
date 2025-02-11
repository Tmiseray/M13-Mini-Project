from flask import Blueprint
from controllers.customerController import save, read, update, deactivate, find_all


customer_blueprint = Blueprint('customer_bp', __name__)

# Save/Create New Customer
customer_blueprint.route('/', methods=['POST'])(save)

# Read Customer
customer_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update Customer
customer_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete/Deactivate Customer
customer_blueprint.route('/<int:id>', methods=['POST'])(deactivate)

# Get All Customers
customer_blueprint.route('/', methods=['GET'])(find_all)