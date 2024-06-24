from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Recipe
from forms import RecipeForm, RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.paginate(page=page, per_page=5)
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            created_by=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('recipe_form.html', form=form)

@app.route('/recipe/<int:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.created_by != current_user.id:
        flash('You are not authorized to edit this recipe.', 'danger')
        return redirect(url_for('index'))
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
    return render_template('recipe_form.html', form=form)

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.created_by != current_user.id:
        flash('You are not authorized to delete this recipe.', 'danger')
        return redirect(url_for('index'))
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        # Use ILIKE for case-insensitive search in PostgreSQL
        search_query = f"%{query}%"
        recipes = Recipe.query.filter(
            (Recipe.title.ilike(search_query)) |
            (Recipe.ingredients.ilike(search_query))
        ).all()
    else:
        recipes = Recipe.query.all()  # Display all recipes if no search query
        
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)