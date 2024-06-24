# Recipe-Management

## Overview

The Recipe Management is a web application that allows users to create, view, and manage recipes. Users can register, log in, and perform CRUD operations on recipes. The application is built using Flask, HTML,CSS and PostgreSQL.

## Endpoints

### User Authentication

- **Register**: `/register` (POST)

  - Allows new users to register.
  - Required data: `username`, `password`, `confirm_password`

- **Login**: `/login` (POST)

  - Allows existing users to log in.
  - Required data: `username`, `password`

- **Logout**: `/logout` (GET)
  - Logs out the current user.

### Recipes

- **Create Recipe**: `/recipe/new` (POST)

  - Allows users to create a new recipe.
  - Required data: `title`, `description`, `ingredients`, `instructions`

- **View Recipe**: `/recipe/<int:id>` (GET)

  - Displays a single recipe based on its ID.

- **Update Recipe**: `/recipe/<int:id>/update` (POST)

  - Allows users to update an existing recipe.
  - Required data: `title`, `description`, `ingredients`, `instructions`

- **Delete Recipe**: `/recipe/<int:id>/delete` (POST)

  - Allows users to delete a recipe.

- **List Recipes**: `/` (GET)
  - Displays a list of all recipes.

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/saudshaikh724/Recipe-Management.git
   cd Recipe-Management
   ```

2. **Create a virtual environment and activate it:**
   python -m venv env
   source venv/env/activate # On Windows, use `venv\Scripts\activate`

3. **Install the dependencies:**
   pip install -r requirements.txt

4. **Initialize the database:**
   flask db upgrade

5. **Run the application:**
   flask run
