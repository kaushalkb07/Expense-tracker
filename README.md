# Django Expense Tracking System

This project is a simple Expense Tracking System built with Django. It allows users to manage and track their daily expenses, visualize expenses through graphs, search through expenses, and export data in various formats like CSV and Excel.

## Features

- User authentication (login, signup, logout).
- Create, read, update, and delete (CRUD) expenses.
- Search expenses by title, amount, description, and date.
- View expenses as graphs on a dashboard.
- Export expense data as CSV and Excel.
- Pagination for expense list.
- Currency conversion using an API.

## Requirements

- Python 3.x
- Django 4.x
- Other dependencies listed in `requirements.txt`.

## Installation

1. Clone the repository:

```bash
git https://github.com/kaushalkb07/Expense-tracker.git
cd your-repository
```

2. Create a virtual environment and activate it: 
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Setup the database
```bash
python manage.py makemigration
python manage.py migrate
```

5. Create a superuser to access the admin dashboard:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Visit http://127.0.0.1:8000 in your browser to access the application.

## Usage
- Sign Up: Create an account to start adding expenses.
- Login: Log in to view, add, and manage your expenses.
- Add Expense: Click the "Add Expense" button to record a new expense.
- Search: Use the search bar to find specific expenses.
- Export: Click on "Export to CSV" to download a CSV file of your expenses.

## API Integration
- Currency Conversion: The project uses a third-party API to convert currency for expenses.
- Graphing: Data visualization is done using Chart.js or another charting library to display expense trends.
