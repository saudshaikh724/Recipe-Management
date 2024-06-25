import unittest
from app import app, db
from models import User, Recipe
from flask_testing import TestCase

# Test case for database-related functionalities
class DatabaseTestCase(TestCase):
    # Specify the configuration for the app in testing mode
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    # Setup the test environment
    def setUp(self):
        db.create_all()  # Create all tables
        self.client = self.app.test_client()  # Create a test client
        self.create_test_user()  # Create a test user for database tests

    # Teardown the test environment
    def tearDown(self):
        db.session.remove()  # Remove the session
        db.drop_all()  # Drop all tables

    # Create a test user for database tests
    def create_test_user(self):
        user = User(username='testuser')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id  # Store the user ID for later use

    # Test the recipe creation functionality
    def test_create_recipe(self):
        self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        response = self.client.post('/recipe/new', data=dict(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredients',
            instructions='Test Instructions'
        ), follow_redirects=True)
        self.assertIn(b'Recipe created successfully!', response.data)

    # Test the recipe editing functionality
    def test_edit_recipe(self):
        self.test_create_recipe()
        recipe = Recipe.query.filter_by(title='Test Recipe').first()
        response = self.client.post(f'/recipe/{recipe.id}/edit', data=dict(
            title='Updated Recipe',
            description='Updated Description',
            ingredients='Updated Ingredients',
            instructions='Updated Instructions'
        ), follow_redirects=True)
        self.assertIn(b'Recipe updated successfully!', response.data)

    # Test the recipe deletion functionality
    def test_delete_recipe(self):
        self.test_create_recipe()
        recipe = Recipe.query.filter_by(title='Test Recipe').first()
        response = self.client.post(f'/recipe/{recipe.id}/delete', follow_redirects=True)
        self.assertIn(b'Recipe deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
