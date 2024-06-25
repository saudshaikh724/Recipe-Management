import unittest
from flask import current_app
from app import app, db
from models import User
from flask_testing import TestCase

# Test case for authentication-related functionalities
class AuthenticationTestCase(TestCase):
    # Specify the configuration for the app in testing mode
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    # Setup the test environment
    def setUp(self):
        db.create_all()  # Create all tables
        self.client = self.app.test_client()  # Create a test client
        self.create_test_user()  # Create a test user for authentication tests

    # Teardown the test environment
    def tearDown(self):
        db.session.remove()  # Remove the session
        db.drop_all()  # Drop all tables

    # Create a test user for authentication tests
    def create_test_user(self):
        user = User(username='testuser')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    # Test the user registration functionality
    def test_register(self):
        response = self.client.post('/register', data=dict(
            username='newuser',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertIn(b'Account created successfully!', response.data)

    # Test the user login functionality
    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'Login successful!', response.data)

    # Test the user logout functionality
    def test_logout(self):
        self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'index', response.data)

    # Test the invalid login attempt functionality
    def test_invalid_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertIn(b'Login Unsuccessful. Please check username and password', response.data)

if __name__ == '__main__':
    unittest.main()
