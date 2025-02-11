from flask import Blueprint
from controllers.productController import save, read, update, deactivate, find_all


product_blueprint = Blueprint('product_bp', __name__)

# Save/Create New Product
product_blueprint.route('/', methods=['POST'])(save)

# Read Product
product_blueprint.route('/<int:id>', methods=['GET'])(read)

# Update Product
product_blueprint.route('/<int:id>', methods=['PUT'])(update)

# Delete/Deactivate Product
product_blueprint.route('/<int:id>', methods=['POST'])(deactivate)

# Get All Products
product_blueprint.route('/', methods=['GET'])(find_all)