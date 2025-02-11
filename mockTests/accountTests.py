import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
import bcrypt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from models.account import Account
from models.user import Admin
from services.accountService import login, save, read, update, deactivate, activate, find_all
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")

class AccountServiceTests(unittest.TestCase):

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

    @patch('services.accountService.db.session.execute')
    def testLoginSuccess(self, mock_execute):
        faker = Faker()
        password = faker.password()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mock_account = Account(
            id = faker.random_int(),
            username = faker.user_name(),
            password = hashed_password,
            role = 'admin'
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_execute.return_value = mock_result

        with patch('services.accountService.encode_token', return_value='fake_token'):
            response = login(mock_account.username, password)
            
            self.assertEqual(response['status'], 'success')
            self.assertEqual(response['message'], 'Successfully logged in')
            self.assertEqual(response['authToken'], 'fake_token')


    @patch('services.accountService.db.session.execute')
    def testLoginFailure(self, mock_execute):
        faker = Faker()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_execute.return_value = mock_result

        response = login(faker.user_name(), faker.password())
        self.assertIsNone(response)


    @patch('services.accountService.db.session.add')
    @patch('services.accountService.db.session.commit')
    @patch('services.accountService.db.session.refresh')
    def testSave(self, mock_refresh, mock_commit, mock_add):
        # Arrange
        faker = Faker()
        mock_account = Account(

        )

    @patch('services.accountService.db.session.execute')
    @patch('services.accountService.db.session.commit')
    def testUpdateAccount(self, mock_commit, mock_execute):
        faker = Faker()
        mock_account = Account(
            id=faker.random_int(),
            username=faker.user_name(),
            password=bcrypt.hashpw(faker.password().encode('utf-8'), bcrypt.gensalt()),
            role='admin'
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_execute.return_value = mock_result
        
        new_data = {
            'id': mock_account.id,
            'username': faker.user_name(),
            'password': faker.password()
        }
        
        result = update(new_data)
        
        self.assertEqual(result.id, mock_account.id)
        self.assertEqual(result.username, new_data['username'])
        mock_commit.assert_called_once()


    @patch('services.accountService.db.session.execute')
    def testUpdateAccountFailure(self, mock_execute):
        faker = Faker()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_execute.return_value = mock_result
        
        with self.assertRaises(Exception) as context:
            update({'id': faker.random_int(), 'password': faker.password()})
        
        self.assertEqual(str(context.exception), 'No account found with that ID')

    @patch('services.accountService.db.session.execute')
    def testFindAllAccounts(self, mock_execute):
        faker = Faker()
        account1 = MagicMock(spec=Account)
        account1.id = faker.random_int()
        account1.username = faker.user_name()
        account1.role = 'user'

        account2 = MagicMock(spec=Account)
        account2.id = faker.random_int()
        account2.username = faker.user_name()
        account2.role = 'admin'

        expected_accounts = [account1, account2]
        mock_execute.return_value.scalars.return_value.all.return_value = expected_accounts

        result = find_all()
        self.assertEqual(result, expected_accounts)

if __name__ == '__main__':
    unittest.main()
