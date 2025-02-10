import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from services.customerService import save, read, update, deactivate, find_all


class CustomerServiceTests(unittest.TestCase):

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


    # @patch('services.customerService.db.session.execute')
    # def testSaveCustomer(self):
    #     # Arrange
    #     faker = Faker()
    #     mock_customer = MagicMock()
    #     mock_customer.name = faker.name()
    #     mock_customer.email = faker.email()
    #     mock_customer.phone = faker.phone_number()

    #     # Act
    #     response = save(mock_customer)

    #     # Assert
    #     self.assertEqual(response['name'], mock_customer.name)
    #     self.assertEqual(response['email'], mock_customer.email)
    #     self.assertEqual(response['phone'], mock_customer.phone)
    #     self.assertEqual(response['role'], 'customer')

    # @patch('services.customerService.db.session.')

    @patch('services.customerService.db.session.execute')
    def test_find_all(self, mock_customers):
        # Arrange
        faker = Faker()
        customer1 = MagicMock()
        customer1.id = faker.random_int()
        customer1.name = faker.name()
        customer1.email = faker.email()
        customer1.phone = faker.phone_number()
        customer1.role = [MagicMock(role='customer')]
        customer1.isActive = [MagicMock(isActive=True)]

        customer2 = MagicMock()
        customer2.id = faker.random_int()
        customer2.name = faker.name()
        customer2.email = faker.email()
        customer2.phone = faker.phone_number()
        customer2.role = [MagicMock(role='customer')]
        customer2.isActive = [MagicMock(isActive=True)]
        expected_customers = [customer1, customer2]

        # Mock query chain
        mock_customers.return_value.scalars.return_value.all.return_value = expected_customers

        # Act
        result = find_all()

        # Assert
        self.assertEqual(result, expected_customers)


if __name__ == '__main__':
    unittest.main()