import unittest
from unittest.mock import patch, MagicMock
from modules.db.database import get_user, verify_user, register_user


class TestUserFunctions(unittest.TestCase):

    def setUp(self):
        # Setup any prerequisites for testing
        pass

    @patch('db.database.UserAccount.query')
    def test_get_user(self, mock_query):
        # Mocking the query filter_by method
        mock_query.filter_by.return_value.first.return_value = MagicMock()

        # Test for an existing user
        existing_user = get_user('testuser')
        self.assertIsNotNone(existing_user)

        # Test for a non-existing user
        non_existing_user = get_user('non_existing_user')
        self.assertIsNone(non_existing_user)

    @patch('db.database.get_user')
    @patch('db.database.bcrypt')
    def test_verify_user(self, mock_bcrypt, mock_get_user):
        # Mocking the return value of get_user
        mock_get_user.return_value = MagicMock(password='hashed_password')
        mock_bcrypt.checkpw.return_value = True

        # Test for correct username and password
        self.assertTrue(verify_user('testuser', 'password'))

        # Test for incorrect username or password
        self.assertFalse(verify_user('non_user1', 'incorrect_password'))
        self.assertFalse(verify_user('non_existing_user', 'password'))

    def test_register_user(self, mock_bcrypt, mock_session, mock_user_account):
        # You can mock dependencies and set up expectations as needed for testing this function
        # Mocking dependencies and setting up expectations

        # Mocking the bcrypt hash function
        mock_bcrypt.hashpw.return_value = b'hashed_password'

        # Mocking the new user object
        new_user_mock = MagicMock()
        mock_user_account.return_value = new_user_mock

        # Test successful registration
        new_user = register_user(
            'John', 'Doe', 'john_doe', 'john@example.com', 'password')
        self.assertIsNotNone(new_user)

        # Test registration with existing username or email
        mock_session.add.side_effect = MagicMock(side_effect=IntegrityError)
        result = register_user(
            'Jane', 'Doe', 'existing_user', 'jane@example.com', 'password')
        self.assertEqual(result['error'], 'IntegrityError')

        # Test handling of SQLAlchemy errors
        mock_session.add.side_effect = MagicMock(side_effect=SQLAlchemyError)
        result = register_user('Jane', 'Doe', 'new_user',
                               'jane@example.com', 'password')
        self.assertEqual(result['error'], 'SQLAlchemyError')

    def tearDown(self):
        # Clean up any resources created during the test
        pass


if __name__ == '__main__':
    unittest.main()
