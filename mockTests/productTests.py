import unittest
from unittest.mock import MagicMock, patch
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from models.product import Product
from services.productService import save, read, update, deactivate, activate, find_all
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")


class ProductServiceTests(unittest.TestCase):

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


    # Test Save Product
    @patch('services.productService.db.session.add')
    @patch('services.productService.db.session.commit')
    @patch('services.productService.db.session.refresh')
    def testSaveProduct(self, mock_refresh, mock_commit, mock_add):
        # Arrange
        faker = Faker()
        mock_product = Product(
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int()
        )

        # Mocking Database
        mock_add.return_value = None
        mock_commit.return_value = None
        mock_refresh.return_value = None

        # Mock Save
        with patch('services.productService.Product', return_value = mock_product):
            # Act
            response = save({
                'name': mock_product.name,
                'price': mock_product.price,
                'createdBy': mock_product.createdBy
            })

            # Assert
            self.assertEqual(response.name, mock_product.name)
            self.assertEqual(response.price, mock_product.price)
            self.assertEqual(response.createdBy, mock_product.createdBy)

    # Test Read Product
    @patch('services.productService.db.session.execute')
    def testRead(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_result = MagicMock()
        mock_product = Product(
            id = faker.random_int(),
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int()
        )

        # Mock Response
        mock_result.scalar_one_or_none.return_value = mock_product
        mock_execute.return_value = mock_result

        # Act
        result = read(mock_product.id)

        # Assert
        self.assertEqual(result.id, mock_product.id)
        self.assertEqual(result.name, mock_product.name)
        self.assertEqual(result.price, mock_product.price)
        self.assertEqual(result.createdBy, mock_product.createdBy)
        self.assertEqual(result.createdAt, mock_product.createdAt)


    @patch('services.productService.db.session.execute')
    def testReadFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # Simulate no result
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            read(faker.random_int())

        self.assertEqual(str(context.exception), 'No product found with that ID')


    # Test Update Product
    @patch('services.productService.db.session.execute')
    @patch('services.productService.db.session.commit')
    def testUpdateProduct(self, mock_commit, mock_execute):
        # Arrange
        faker = Faker()
        mock_product = Product(
            id = faker.random_int(),
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int()
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_product
        mock_execute.return_value = mock_scalar_result

        # New Data for Update
        updated_data = {
            'id': mock_product.id,
            'name': faker.name(),
            'price': faker.random_number(),
            'updatedBy': faker.random_int()
        }

        # Act
        result = update(updated_data)

        # Assert
        self.assertEqual(result.id, mock_product.id)
        self.assertEqual(result.name, updated_data['name'])
        self.assertEqual(result.price, updated_data['price'])
        self.assertEqual(result.updatedBy, updated_data['updatedBy'])
        mock_commit.assert_called_once()


    @patch('services.productService.db.session.execute')
    @patch.object(Product, 'deactivate')
    def testDeactivate(self, mock_deactivate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_product = Product(
            id = faker.random_int(),
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int(),
            isActive = True
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_product
        mock_execute.return_value = mock_scalar_result

        # Mock Deactivate Function
        def mock_deactivate():
            mock_product.isActive = False

        mock_deactivate_method.side_effect = mock_deactivate

        # Act
        result = deactivate({'id': mock_product.id})

        # Assert
        mock_deactivate_method.assert_called_once()
        self.assertFalse(result.isActive)


    @patch('services.productService.db.session.execute')
    def testDeactivateProductNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No product found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No product found with that ID')


    @patch('services.productService.db.session.execute')
    def testDeactivateProductFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_product = Product(
            id = faker.random_int(),
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int(),
            isActive = False
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_product
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            deactivate({'id': mock_product.id})

        self.assertEqual(str(context.exception), 'Product is already deactivated')


    @patch('services.productService.db.session.execute')
    @patch.object(Product, 'activate')
    def testActivateProduct(self, mock_activate_method, mock_execute):
        # Arrange
        faker = Faker()
        mock_product = Product(
            id = faker.random_int(),
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int(),
            isActive = False
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_product
        mock_execute.return_value = mock_scalar_result

        # Mock Activate Function
        def mock_activate():
            mock_product.isActive = True

        mock_activate_method.side_effect = mock_activate

        # Act
        result = activate({'id': mock_product.id})

        # Assert
        mock_activate_method.assert_called_once()
        self.assertTrue(result.isActive)


    @patch('services.productService.db.session.execute')
    def testActivateProductNotFound(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = None  # No product found
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': faker.random_int()})  # Random ID

        self.assertEqual(str(context.exception), 'No product found with that ID')


    @patch('services.productService.db.session.execute')
    def testActivateProductFailure(self, mock_execute):
        # Arrange
        faker = Faker()
        mock_product = Product(
            id = faker.random_int(),
            name = faker.name(),
            price = faker.random_number(),
            createdBy = faker.random_int(),
            isActive = True
        )

        # Mock Database Response
        mock_scalar_result = MagicMock()
        mock_scalar_result.scalar_one_or_none.return_value = mock_product
        mock_execute.return_value = mock_scalar_result

        # Act & Assert
        with self.assertRaises(Exception) as context:
            activate({'id': mock_product.id})

        self.assertEqual(str(context.exception), 'Product is already activated')


    @patch('services.productService.db.session.execute')
    def testFindAll(self, mock_execute):
        # Arrange
        faker = Faker()
        product = MagicMock(spec=Product)
        product.id = faker.random_int()
        product.name = faker.name()
        product.price = faker.random_number()
        product.createdBy = faker.random_int()
        product.isActive = True

        product2 = MagicMock(spec=Product)
        product2.id = faker.random_int()
        product2.name = faker.name()
        product2.price = faker.random_number()
        product2.createdBy = faker.random_int()
        product2.isActive = True
        expected_products = [product, product2]

        # Mock Query
        mock_execute.return_value.scalars.return_value.all.return_value = expected_products

        # Act
        result = find_all()

        # Assert
        self.assertEqual(result, expected_products)


if __name__ == '__main__':
    unittest.main()