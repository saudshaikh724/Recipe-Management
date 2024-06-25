from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model class, representing a user in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(64), unique=True, nullable=False)  # Username field, must be unique and not nullable
    password = db.Column(db.String(256), nullable=False)  # Password field, hashed and not nullable

    # Method to set password, storing the hashed version
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    # Method to check password, comparing the provided password with the stored hashed password
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Recipe model class, representing a recipe in the database
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(100), nullable=False)  # Title field, not nullable
    description = db.Column(db.Text)  # Description field, optional
    ingredients = db.Column(db.Text)  # Ingredients field, optional (could be JSON)
    instructions = db.Column(db.Text)  # Instructions field, optional
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to the User model, not nullable
