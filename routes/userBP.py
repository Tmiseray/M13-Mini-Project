from flask import Blueprint
from controllers.userController import save, read, update, deactivate, find_all, find_all_admins, find_all_customers


user_blueprint = Blueprint('user_bp', __name__)

# Save/Create New User
user_blueprint.route('/', methods=['POST'])(save)

# Read User
user_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update User
user_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete/Deactivate User
user_blueprint.route('/<int:id>', methods=['POST'])(deactivate)

# Get All Users
user_blueprint.route('/', methods=['GET'])(find_all)

# Get All Admins
user_blueprint.route('/admins', methods=['GET'])(find_all_admins)

# Get All Customers
user_blueprint.route('/customers', methods=['GET'])(find_all_customers)