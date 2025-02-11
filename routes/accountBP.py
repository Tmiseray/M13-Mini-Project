from flask import Blueprint
from controllers.accountController import save, read, update, deactivate, find_all


account_blueprint = Blueprint('account_bp', __name__)

# Save/Create New Account
account_blueprint.route('/', methods=['POST'])(save)

# Read Account
account_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update Account
account_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete/Deactivate Account
account_blueprint.route('/<int:id>', methods=['POST'])(deactivate)

# Get All Accounts
account_blueprint.route('/', methods=['GET'])(find_all)