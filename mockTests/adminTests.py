import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from models.user import Admin
from services.adminService import save, read, update, deactivate, activate, find_all
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")


class AdminServiceTests(unittest.TestCase):

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


    @patch('services.adminService.db.session.add')
    @patch('services.adminService.db.session.commit')
    @patch('services.adminService.db.session.refresh')
    def testSave(self, mock_refresh, mock_commit, mock_add):
        # Arrange
        faker = Faker()
        mock_admin = Admin(
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'admin'
        )

        # Mocking Database
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None

        # Mock Save
        with patch('services.adminService.Admin', return_value = mock_admin):
            # Act
            response = save({
                'name': mock_admin.name,
                'email': mock_admin.email,
                'phone': mock_admin.phone
            })

            # Assert
            self.assertEqual(response.name, mock_admin.name)
            self.assertEqual(response.email, mock_admin.email)
            self.assertEqual(response.phone, mock_admin.phone)
            self.assertEqual(response.role, 'admin')


    @patch('services.adminService.db.session.execute')
    def testRead(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_result = MagicMock()
        mock_admin = Admin(
            id = faker.random_int(),
            name = faker.name(),
            email = faker.email(),
            phone = faker.phone_number(),
            role = 'admin'
        )

        # Mock Response
        mock_result.scalar_one_or_none.return_value = mock_admin
        mock_execute.return_value = mock_result

        # Act
        result = read(mock_admin.id)

        # Assert
        self.assertEqual(result.id, mock_admin.id)
        self.assertEqual(result.name, mock_admin.name)
        self.assertEqual(result.email, mock_admin.email)
        self.assertEqual(result.phone, mock_admin.phone)


    @patch('services.adminService.db.session.execute')
    def testReadFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # Simulate no result
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            read(faker.random_int())

        self.assertEqual(str(context.exception), 'No admin found with that ID')


    @patch('services.adminService.db.session.execute')
    @patch('services.adminService.db.session.commit')
    def testUpdateAdmin(self, mock_commit, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = Admin(
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
            'phone': faker.phone_number()
        }

        # Act
        result = update(updated_data)

        # Assert
        self.assertEqual(result.id, mock_admin.id)
        self.assertEqual(result.name, updated_data['name'])
        self.assertEqual(result.email, updated_data['email'])
        self.assertEqual(result.phone, updated_data['phone'])
        mock_commit.assert_called_once()


    @patch('services.adminService.db.session.execute')
    def testUpdateAdminFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No admin found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            update({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No admin found with that ID')


    @patch('services.adminService.db.session.execute')
    @patch.object(Admin, 'deactivate')
    def testDeactivateAdmin(self, mock_deactivate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = Admin(
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

        # Mock Deactivate Function
        def mock_deactivate():
            mock_admin.isActive = False

        mock_deactivate_method.side_effect = mock_deactivate

        # Act
        result = deactivate({'id': mock_admin.id})

        # Assert
        mock_deactivate_method.assert_called_once()
        self.assertFalse(result.isActive)


    @patch('services.adminService.db.session.execute')
    # @patch.object(Admin, 'deactivate')
    def testDeactivateAdminNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No admin found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No admin found with that ID')


    @patch('services.adminService.db.session.execute')
    # @patch.object(Admin, 'deactivate')
    def testDeactivateAdminFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = Admin(
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

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': mock_admin.id})

        self.assertEqual(str(context.exception), 'Admin is already deactivated')


    @patch('services.adminService.db.session.execute')
    @patch.object(Admin, 'activate')
    def testActivateAdmin(self, mock_activate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = Admin(
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


    @patch('services.adminService.db.session.execute')
    # @patch.object(Admin, 'activate')
    def testActivateAdminNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No admin found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No admin found with that ID')


    @patch('services.adminService.db.session.execute')
    # @patch.object(Admin, 'activate')
    def testActivateAdminFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_admin = Admin(
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

        self.assertEqual(str(context.exception), 'Admin is already activated')


    @patch('services.adminService.db.session.execute')
    def testFindAll(self, mock_execute):
        # Arrange
        faker = Faker()
        admin1 = MagicMock(spec=Admin)
        admin1.id = faker.random_int()
        admin1.name = faker.name()
        admin1.email = faker.email()
        admin1.phone = faker.phone_number()
        admin1.role = 'admin'
        admin1.isActive = True

        admin2 = MagicMock(spec=Admin)
        admin2.id = faker.random_int()
        admin2.name = faker.name()
        admin2.email = faker.email()
        admin2.phone = faker.phone_number()
        admin2.role = 'admin'
        admin2.isActive = True
        expected_admins = [admin1, admin2]

        # Mock Query
        mock_execute.return_value.scalars.return_value.all.return_value = expected_admins

        # Act
        result = find_all()

        # Assert
        self.assertEqual(result, expected_admins)


if __name__ == '__main__':
    unittest.main()