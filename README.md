# Recipe Repository

A simple Django web application for managing and sharing recipes.

This project was created as part of the **Cyber Security Base MOOC** course project at the **University of Helsinki**. The purpose of the project is to build a small web application and later demonstrate and fix multiple security vulnerabilities based on the OWASP Top 10.

## Features

- User registration and login
- Public recipe listing
- Personal "My Recipes" page for users to manage their own recipes
- Create, edit, and delete recipes
- Search recipes by title
- Public and private recipes

## Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/mkekola/recipe-repository.git
    cd recipe-repository
    ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Open your web browser and navigate to `http://127.0.0.1:8000/` to access the application.