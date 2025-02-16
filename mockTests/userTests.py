import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from models.user import User
from services.userService import save, read, update, deactivate, activate, find_all, find_all_admins, find_all_customers
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")


class userServiceTests(unittest.TestCase):

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


    # Test Save Admin User
    @patch('services.userService.db.session.add')
    @patch('services.userService.db.session.commit')
    @patch('services.userService.db.session.refresh')
    def testSaveAdmin(self, mock_refresh, mock_commit, mock_add):
        # Arrange
        faker = Faker()
        mock_admin = User(
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = '@Dm!n1$+rAT0R'
        )

        # Mocking Database
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None

        # Mock Save
        with patch('services.userService.User', return_value = mock_admin):
            # Act
            response = save({
                'name': mock_admin.name,
                'email': mock_admin.email,
                'phone': mock_admin.phone,
                'role': mock_admin.role
            })

            # Assert
            self.assertEqual(response.name, mock_admin.name)
            self.assertEqual(response.email, mock_admin.email)
            self.assertEqual(response.phone, mock_admin.phone)
            self.assertEqual(response.role, mock_admin.role)

    # Test Save Customer User
    @patch('services.userService.db.session.add')
    @patch('services.userService.db.session.commit')
    @patch('services.userService.db.session.refresh')
    def testSaveCustomer(self, mock_refresh, mock_commit, mock_add):
        # Arrange
        faker = Faker()
        mock_customer = User(
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'user'
        )

        # Mocking Database
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None

        # Mock Save
        with patch('services.userService.User', return_value = mock_customer):
            # Act
            response = save({
                'name': mock_customer.name,
                'email': mock_customer.email,
                'phone': mock_customer.phone,
                'role': mock_customer.role
            })

            # Assert
            self.assertEqual(response.name, mock_customer.name)
            self.assertEqual(response.email, mock_customer.email)
            self.assertEqual(response.phone, mock_customer.phone)
            self.assertEqual(response.role, mock_customer.role)


    # Test Read User
    @patch('services.userService.db.session.execute')
    def testRead(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_result = MagicMock()
        mock_user = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = faker.word()
        )

        # Mock Response
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_execute.return_value = mock_result

        # Act
        result = read(mock_user.id)

        # Assert
        self.assertEqual(result.id, mock_user.id)
        self.assertEqual(result.name, mock_user.name)
        self.assertEqual(result.email, mock_user.email)
        self.assertEqual(result.phone, mock_user.phone)
        self.assertEqual(result.role, mock_user.role)


    @patch('services.userService.db.session.execute')
    def testReadFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # Simulate no result
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            read(faker.random_int())

        self.assertEqual(str(context.exception), 'No user found with that ID')


    # Test Update Admin User
    @patch('services.userService.db.session.execute')
    @patch('services.userService.db.session.commit')
    def testUpdateAdmin(self, mock_commit, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'admin'
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_admin
        mock_execute.return_value = mock_scalar_result

        # New Data for Update
        updated_data = {
            'id': mock_admin.id,
            'name': faker.name(),
            'email': faker.email(),
            'phone': faker.phone_number(),
            'role': '@Dm!n1$+rAT0R'
        }

        # Act
        result = update(updated_data)

        # Assert
        self.assertEqual(result.id, mock_admin.id)
        self.assertEqual(result.name, updated_data['name'])
        self.assertEqual(result.email, updated_data['email'])
        self.assertEqual(result.phone, updated_data['phone'])
        self.assertEqual(result.role, updated_data['role'])
        mock_commit.assert_called_once()


    # Test Update Customer User
    @patch('services.userService.db.session.execute')
    @patch('services.userService.db.session.commit')
    def testUpdateCustomer(self, mock_commit, mock_execute):
        # Arrange
        faker = Faker()
        mock_customer = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'user'
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
            'phone': faker.phone_number(),
            'role': 'user'
        }

        # Act
        result = update(updated_data)

        # Assert
        self.assertEqual(result.id, mock_customer.id)
        self.assertEqual(result.name, updated_data['name'])
        self.assertEqual(result.email, updated_data['email'])
        self.assertEqual(result.phone, updated_data['phone'])
        self.assertEqual(result.role, updated_data['role'])
        mock_commit.assert_called_once()


    @patch('services.userService.db.session.execute')
    def testUpdateUserFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No user found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            update({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No user found with that ID')


    @patch('services.userService.db.session.execute')
    @patch.object(User, 'deactivate')
    def testDeactivate(self, mock_deactivate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_user = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'user',
            isActive = True
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_user
        mock_execute.return_value = mock_scalar_result

        # Mock Deactivate Function
        def mock_deactivate():
            mock_user.isActive = False

        mock_deactivate_method.side_effect = mock_deactivate

        # Act
        result = deactivate({'id': mock_user.id})

        # Assert
        mock_deactivate_method.assert_called_once()
        self.assertFalse(result.isActive)


    @patch('services.userService.db.session.execute')
    # @patch.object(Admin, 'deactivate')
    def testDeactivateUserNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No user found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No user found with that ID')


    @patch('services.userService.db.session.execute')
    # @patch.object(Admin, 'deactivate')
    def testDeactivateUserFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_user = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'user',
            isActive = False
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_user
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': mock_user.id})

        self.assertEqual(str(context.exception), 'User is already deactivated')


    @patch('services.userService.db.session.execute')
    @patch.object(User, 'activate')
    def testActivateUser(self, mock_activate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'admin',
            isActive = False
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_admin
        mock_execute.return_value = mock_scalar_result

        # Mock Activate Function
        def mock_activate():
            mock_admin.isActive = True

        mock_activate_method.side_effect = mock_activate

        # Act
        result = activate({'id': mock_admin.id})

        # Assert
        mock_activate_method.assert_called_once()
        self.assertTrue(result.isActive)


    @patch('services.userService.db.session.execute')
    # @patch.object(Admin, 'activate')
    def testActivateUserNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No user found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No user found with that ID')


    @patch('services.userService.db.session.execute')
    # @patch.object(Admin, 'activate')
    def testActivateUserFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = User(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'admin',
            isActive = True
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_admin
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': mock_admin.id})

        self.assertEqual(str(context.exception), 'User is already activated')


    @patch('services.userService.db.session.execute')
    def testFindAll(self, mock_execute):
        # Arrange
        faker = Faker()
        admin = MagicMock(spec=User)
        admin.id = faker.random_int()
        admin.name = faker.name()
        admin.email = faker.email()
        admin.phone = faker.phone_number()
        admin.role = 'admin'
        admin.isActive = True

        customer = MagicMock(spec=User)
        customer.id = faker.random_int()
        customer.name = faker.name()
        customer.email = faker.email()
        customer.phone = faker.phone_number()
        customer.role = 'user'
        customer.isActive = True
        expected_users = [admin, customer]

        # Mock Query
        mock_execute.return_value.scalars.return_value.all.return_value = expected_users

        # Act
        result = find_all()

        # Assert
        self.assertEqual(result, expected_users)


    @patch('services.userService.db.session.execute')
    def testFindAllAdmins(self, mock_execute):
        # Arrange
        faker = Faker()
        admin = MagicMock(spec=User)
        admin.id = faker.random_int()
        admin.name = faker.name()
        admin.email = faker.email()
        admin.phone = faker.phone_number()
        admin.role = 'admin'
        admin.isActive = True

        admin2 = MagicMock(spec=User)
        admin2.id = faker.random_int()
        admin2.name = faker.name()
        admin2.email = faker.email()
        admin2.phone = faker.phone_number()
        admin2.role = 'admin'
        admin2.isActive = True
        expected_admins = [admin, admin2]

        # Mock Query
        mock_execute.return_value.scalars.return_value.all.return_value = expected_admins

        # Act
        result = find_all_admins()

        # Assert
        self.assertEqual(result, expected_admins)

    
    @patch('services.userService.db.session.execute')
    def testFindAllCustomers(self, mock_execute):
        # Arrange
        faker = Faker()
        customer = MagicMock(spec=User)
        customer.id = faker.random_int()
        customer.name = faker.name()
        customer.email = faker.email()
        customer.phone = faker.phone_number()
        customer.role = 'user'
        customer.isActive = True

        customer2 = MagicMock(spec=User)
        customer2.id = faker.random_int()
        customer2.name = faker.name()
        customer2.email = faker.email()
        customer2.phone = faker.phone_number()
        customer2.role = 'user'
        customer2.isActive = True
        expected_customers = [customer, customer2]

        # Mock Query
        mock_execute.return_value.scalars.return_value.all.return_value = expected_customers

        # Act
        result = find_all()

        # Assert
        self.assertEqual(result, expected_customers)


if __name__ == '__main__':
    unittest.main()