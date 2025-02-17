from flask import Blueprint
from controllers.accountController import login, save, read, update, deactivate, find_all


account_blueprint = Blueprint('account_bp', __name__)

# Save/Create New Account
account_blueprint.route('/', methods=['POST'])(save)

# Login
account_blueprint.route('/login', methods=['POST'])(login)

# Read Account
account_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update Account
account_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete/Deactivate Account
account_blueprint.route('/<int:id>', methods=['POST'])(deactivate)

# Get All Accounts
account_blueprint.route('/', methods=['GET'])(find_all)