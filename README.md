# Coderr Project - Backend

Coderr is a freelancer platform specifically for software developers.
This API forms the backbone of the application and manages users,
offers, orders, and reviews.

You can find the corresponding frontend here: coderr-frontend

Version: 1.0

## Features

* **User Management**: Registration and login system with distinction between Business and Customer.
* **Offer Management**: Create and manage services by Business users.
* **Order System**: Complete ordering process for customers.
* **Review System**: Customers can submit, edit, and delete reviews.
* **Profiles**: Automatically created and assigned user profiles for all participants.

## Requirements

* **Python**: 3.13.x (Developed and tested with 3.13.7)
* **Database**: SQLite (Default)
* **Minimum Python Version**: 3.10+ (Required due to Django 6.0 features)
* **Framework**: Django & Django REST Framework

### Key Dependencies
- Django == 6.0.1
- djangorestframework == 3.16.1
- django-filter == 25.2
- django-cors-headers == 4.9.0

## Installation

Clone the project:

``` bash
git clone git@github.com:DanielSchn/coderr-backend.git
cd coderr-backend
```

## Create Virtual Environment

### Create

``` bash
python -m venv venv
```

### Activate (Linux/Mac)

``` bash
source venv/bin/activate
```

### Activate (Windows)

``` bash
venv\Scripts\activate
```

## Install Dependencies

``` bash
pip install -r requirements.txt
```

### Initialize Database

``` bash
python manage.py makemigrations
python manage.py migrate
```

### Start Server

``` bash
python manage.py runserver
```

The API is now accessible at http://127.0.0.1:8000.

## Create Superuser (Admin)

The project supports the default Django command for creating
administrators:

``` bash
python manage.py createsuperuser
```

A corresponding UserProfile is created and correctly assigned
automatically.

### Automatic Profile Creation

User profiles are generated automatically using Django signals when a
new user is created (including superusers). This ensures that:

-   Every user always has exactly one profile
-   Profiles are correctly linked to their user
-   No manual shell commands are required
-   The standard Django `createsuperuser` command works as expected
-   The project is clone‑friendly and production‑ready

## Configuration (Core Settings)

The project uses Django REST Framework with the following core settings
in settings.py:

Authentication: TokenAuthentication

Permissions: IsAuthenticatedOrReadOnly (Read for everyone, write only
for logged‑in users).

Filters: DjangoFilterBackend for precise API queries.

## Usage & Commands

``` bash
python manage.py makemigrations   # Create migration files for model changes
python manage.py migrate          # Apply changes to the database
python manage.py runserver        # Start the local development server
python manage.py test             # Run the automated test suite
```

## License

This project was created as a learning project and is currently not
under any specific license.
