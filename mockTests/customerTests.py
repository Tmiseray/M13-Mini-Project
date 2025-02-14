import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from models.customer import Customer
from services.customerService import save, read, update, deactivate, activate, find_all
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")


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


    @patch('services.customerService.db.session.add')
    @patch('services.customerService.db.session.commit')
    @patch('services.customerService.db.session.refresh')
    def testSave(self, mock_refresh, mock_commit, mock_add):
        # Arrange
        faker = Faker()
        mock_customer = Customer(
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer'
        )

        # Mocking Database
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None

        # Mock Save
        with patch('services.customerService.Customer', return_value = mock_customer):
            # Act
            response = save({
                'name': mock_customer.name,
                'email': mock_customer.email,
                'phone': mock_customer.phone
            })

            # Assert
            self.assertEqual(response.name, mock_customer.name)
            self.assertEqual(response.email, mock_customer.email)
            self.assertEqual(response.phone, mock_customer.phone)
            self.assertEqual(response.role, 'customer')


    @patch('services.customerService.db.session.execute')
    def testRead(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_result = MagicMock()
        mock_customer = Customer(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer'
        )

        # Mock Response
        mock_result.scalar_one_or_none.return_value = mock_customer
        mock_execute.return_value = mock_result

        # Act
        result = read(mock_customer.id)

        # Assert
        self.assertEqual(result.id, mock_customer.id)
        self.assertEqual(result.name, mock_customer.name)
        self.assertEqual(result.email, mock_customer.email)
        self.assertEqual(result.phone, mock_customer.phone)


    @patch('services.customerService.db.session.execute')
    def testReadFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # Simulate no result
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            read(faker.random_int())

        self.assertEqual(str(context.exception), 'No customer found with that ID')


    @patch('services.customerService.db.session.execute')
    @patch('services.customerService.db.session.commit')
    def testUpdateCustomer(self, mock_commit, mock_execute):
        # Arrange
        faker = Faker()
        mock_customer = Customer(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer'
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_customer
        mock_execute.return_value = mock_scalar_result

        # New Data for Update
        updated_data = {
            'id': mock_customer.id,
            'name': faker.name(),
            'email': faker.email(),
            'phone': faker.phone_number()
        }

        # Act
        result = update(updated_data)

        # Assert
        self.assertEqual(result.id, mock_customer.id)
        self.assertEqual(result.name, updated_data['name'])
        self.assertEqual(result.email, updated_data['email'])
        self.assertEqual(result.phone, updated_data['phone'])
        mock_commit.assert_called_once()


    @patch('services.customerService.db.session.execute')
    def testUpdateCustomerFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No customer found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            update({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No customer found with that ID')


    @patch('services.customerService.db.session.execute')
    @patch.object(Customer, 'deactivate')
    def testDeactivateCustomer(self, mock_deactivate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_customer = Customer(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer',
            isActive = True
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_customer
        mock_execute.return_value = mock_scalar_result

        # Mock Deactivate Function
        def mock_deactivate():
            mock_customer.isActive = False

        mock_deactivate_method.side_effect = mock_deactivate

        # Act
        result = deactivate({'id': mock_customer.id})

        # Assert
        mock_deactivate_method.assert_called_once()
        self.assertFalse(result.isActive)


    @patch('services.customerService.db.session.execute')
    # @patch.object(Customer, 'deactivate')
    def testDeactivateCustomerNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No customer found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No customer found with that ID')


    @patch('services.customerService.db.session.execute')
    # @patch.object(Customer, 'deactivate')
    def testDeactivateCustomerFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_customer = Customer(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer',
            isActive = False
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_customer
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': mock_customer.id})

        self.assertEqual(str(context.exception), 'Customer is already deactivated')


    @patch('services.customerService.db.session.execute')
    @patch.object(Customer, 'activate')
    def testActivateCustomer(self, mock_activate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_customer = Customer(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer',
            isActive = False
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_customer
        mock_execute.return_value = mock_scalar_result

        # Mock Activate Function
        def mock_activate():
            mock_customer.isActive = True

        mock_activate_method.side_effect = mock_activate

        # Act
        result = activate({'id': mock_customer.id})

        # Assert
        mock_activate_method.assert_called_once()
        self.assertTrue(result.isActive)


    @patch('services.customerService.db.session.execute')
    # @patch.object(Customer, 'activate')
    def testActivateCustomerNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No customer found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No customer found with that ID')


    @patch('services.customerService.db.session.execute')
    # @patch.object(Customer, 'activate')
    def testActivateCustomerFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_customer = Customer(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'customer',
            isActive = True
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_customer
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': mock_customer.id})

        self.assertEqual(str(context.exception), 'Customer is already activated')


    @patch('services.customerService.db.session.execute')
    def testFindAll(self, mock_execute):
        # Arrange
        faker = Faker()
        customer1 = MagicMock(spec=Customer)
        customer1.id = faker.random_int()
        customer1.name = faker.name()
        customer1.email = faker.email()
        customer1.phone = faker.phone_number()
        customer1.role = 'customer'
        customer1.isActive = True

        customer2 = MagicMock(spec=Customer)
        customer2.id = faker.random_int()
        customer2.name = faker.name()
        customer2.email = faker.email()
        customer2.phone = faker.phone_number()
        customer2.role = 'customer'
        customer2.isActive = True
        expected_customers = [customer1, customer2]

        # Mock Query
        mock_execute.return_value.scalars.return_value.all.return_value = expected_customers

        # Act
        result = find_all()

        # Assert
        self.assertEqual(result, expected_customers)


if __name__ == '__main__':
    unittest.main()