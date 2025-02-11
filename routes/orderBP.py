from flask import Blueprint
from controllers.orderController import save, read, update, delete, find_all


order_blueprint = Blueprint('order_bp', __name__)

# Save/Create New Order
order_blueprint.route('/', methods=['POST'])(save)

# Read Order
order_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update Order
order_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete Order
order_blueprint.route('/<int:id>', methods=['POST'])(delete)

# Get All Orders
order_blueprint.route('/', methods=['GET'])(find_all)