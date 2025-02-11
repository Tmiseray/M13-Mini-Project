from flask import Blueprint
from controllers.adminController import save, read, update, deactivate, find_all


admin_blueprint = Blueprint('admin_bp', __name__)

# Save/Create New Admin
admin_blueprint.route('/', methods=['POST'])(save)

# Read Admin
admin_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update Admin
admin_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete/Deactivate Admin
admin_blueprint.route('/<int:id>', methods=['POST'])(deactivate)

# Get All Admins
admin_blueprint.route('/', methods=['GET'])(find_all)