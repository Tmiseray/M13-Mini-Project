import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from models.order import Order
from models.product import Product
from models.user import User
from services.orderService import save, read, update, delete, find_all
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")


class OrderServiceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('TestingConfig')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()


    # Test Read Order
    @patch('services.orderService.db.session.execute')
    def testReadOrder(self, mock_execute):
        faker = Faker()
        mock_result = MagicMock()
        mock_order = Order(
            id=faker.random_int(),
            customerId=faker.random_int(),
            productId=faker.random_int(),
            quantity=faker.random_int(min=1, max=10)
        )

        mock_result.scalar_one_or_none.return_value = mock_order
        mock_execute.return_value = mock_result

        result = read(mock_order.id)

        self.assertEqual(result.id, mock_order.id)
        self.assertEqual(result.customerId, mock_order.customerId)
        self.assertEqual(result.productId, mock_order.productId)
        self.assertEqual(result.quantity, mock_order.quantity)

    # Test Update Order
    @patch('services.orderService.db.session.execute')
    @patch('services.orderService.db.session.commit')
    def testUpdateOrder(self, mock_commit, mock_execute):
        faker = Faker()
        mock_order = Order(
            id=faker.random_int(),
            customerId=faker.random_int(),
            productId=faker.random_int(),
            quantity=faker.random_int(min=1, max=10)
        )

        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_order
        mock_execute.return_value = mock_scalar_result

        updated_data = {
            'id': mock_order.id,
            'quantity': faker.random_int(min=1, max=10)
        }

        result = update(updated_data)
        self.assertEqual(result.id, mock_order.id)
        self.assertEqual(result.quantity, updated_data['quantity'])
        mock_commit.assert_called_once()

    # Test Delete Order
    @patch('services.orderService.db.session.commit')
    @patch('services.orderService.db.session.delete')
    @patch('services.orderService.db.session.execute')
    def testDeleteOrder(self, mock_execute, mock_delete, mock_commit):
        faker = Faker()
        mock_order = MagicMock(spec=Order)
        mock_order.id = faker.random_int()

        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_order
        mock_execute.return_value = mock_scalar_result

        delete({'id': mock_order.id})
        
        mock_delete.assert_called_once_with(mock_order)
        mock_commit.assert_called_once()

    # Test Find All Orders
    @patch('services.orderService.db.session.execute')
    def testFindAllOrders(self, mock_execute):
        faker = Faker()
        order1 = MagicMock(spec=Order)
        order1.id = faker.random_int()
        order1.customerId = faker.random_int()
        order1.productId = faker.random_int()
        order1.quantity = faker.random_int(min=1, max=10)

        order2 = MagicMock(spec=Order)
        order2.id = faker.random_int()
        order2.customerId = faker.random_int()
        order2.productId = faker.random_int()
        order2.quantity = faker.random_int(min=1, max=10)

        expected_orders = [order1, order2]

        mock_execute.return_value.scalars.return_value.all.return_value = expected_orders

        result = find_all()
        self.assertEqual(result, expected_orders)

if __name__ == '__main__':
    unittest.main()
