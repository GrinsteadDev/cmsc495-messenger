from flask import Flask
from unittest.mock import patch, MagicMock
from os.path import dirname, realpath
from sys import path
import unittest


# Needed to set path before accessing the  module at parent dir
path.append(f"{dirname(realpath(__file__))}/../")
from modules.db.database import get_user, verify_user, register_user  # isort: skip
from modules.settings import config  # isort: skip


class TestUserFunctions(unittest.TestCase):
    """A test case class for user-related functions"""

    def setUp(self):
        """Set up a Flask application context before each test"""
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = config["SQLALCHEMY_DATABASE_URI"]
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after each test by poppin the Flask application context"""
        self.app_context.pop()

    @patch('modules.db.database.UserAccount.query')
    def test_get_user(self, mock_query):
        """Test the get_user function"""

        # Mocking the query filter_by method
        mock_query.filter_by.return_value.first.side_effect = [MagicMock(), None]

        # Test for an existing user
        existing_user = get_user('testuser')
        self.assertIsNotNone(existing_user)

        # Test for a non-existing user
        non_existing_user = get_user('non_existing_user')
        self.assertIsNone(non_existing_user)

    @patch('modules.db.database.get_user')
    @patch('modules.db.database.bcrypt')
    def test_verify_user(self, mock_bcrypt, mock_get_user):
        """Test the verify_user function"""

        mock_user = MagicMock()
        mock_user.password = b'hashed_password'
        mock_get_user.side_effect = [mock_user, None, None]

        mock_bcrypt.checkpw.return_value = True

        # Test for correct username and password
        self.assertTrue(verify_user('testuser', 'password'))

        # Test for incorrect username or password
        self.assertFalse(verify_user('non_user1', 'incorrect_password'))

        self.assertFalse(verify_user('non_existing_user', 'password'))

    @patch('modules.db.database.bcrypt')
    @patch('modules.db.database.db.session')
    @patch('modules.db.database.UserAccount')
    def test_register_user(self, mock_user_account, mock_session, mock_bcrypt):
        """Test the register_user function"""

        # Mocking the bcrypt hash function
        mock_bcrypt.hashpw.return_value = b'hashed_password'

        # Mocking the new user object
        new_user_mock = MagicMock()
        mock_user_account.return_value = new_user_mock

        # Test successful registration
        new_user = register_user(
            'John', 'Doe', 'john_doe', 'john@example.com', 'password')

        # Test registration with existing username or email
        mock_session.add.assert_called_once_with(new_user_mock)
        mock_session.commit.assert_called_once()
        self.assertIsNone(new_user)

    


if __name__ == '__main__':
    unittest.main()
