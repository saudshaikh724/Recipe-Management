from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

# Form for creating and editing recipes
class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  # Title field with a required validator
    description = TextAreaField('Description')  # Optional description field
    ingredients = TextAreaField('Ingredients')  # Optional ingredients field
    instructions = TextAreaField('Instructions')  # Optional instructions field
    submit = SubmitField('Submit')  # Submit button

# Form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])  # Username field with required and length validators
    password = PasswordField('Password', validators=[DataRequired()])  # Password field with required validator
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  # Confirm password field with required and equality validators
    submit = SubmitField('Sign Up')  # Submit button

# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])  # Username field with required and length validators
    password = PasswordField('Password', validators=[DataRequired()])  # Password field with required validator
    submit = SubmitField('Login')  # Submit button
