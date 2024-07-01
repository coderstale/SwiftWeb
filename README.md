SwiftWeb is a light and customizable web framework which allows you to develop dynamic web applications. It ships with routing, template rendering, session management, authentication, and database integration.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Routing](#routing)
- [Template Rendering](#template-rendering)
- [Database Integration](#database-integration)
- [Authentication and Authorization](#authentication-and-authorization)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- Lightweight and easy to use
- Customizable routing system
- Template rendering with Jinja2
- Session management
- Authentication and authorization
- Database integration with SQLAlchemy
- Middleware support
- Static file serving
- Command-line interface (CLI) for managing tasks

## Installation

To get started with SwiftWeb, clone the repository and install the dependencies:

```bash
git clone https://github.com/coderstale/SwiftWeb.git
cd SwiftWeb
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

You can start the development server using the CLI:

```bash
python cli.py runserver --port 8000
```

To create a new user and test the authentication features:

```bash
python cli.py create_user --username testuser --password testpassword --email test@example.com
```

## Project Structure

```plaintext
SwiftWeb/
├── .github/
│   └── workflows/
│       └── python-app.yml
├── my_framework/
│   ├── __init__.py
│   ├── auth.py
│   ├── crud.py
│   ├── db.py
│   ├── handlers.py
│   ├── middleware.py
│   ├── models.py
│   ├── request.py
│   ├── response.py
│   ├── routing.py
│   ├── server.py
│   ├── session.py
│   └── template_engine.py
├── static/
│   ├── image.png
│   ├── script.js
│   └── styles.css
├── templates/
│   ├── index.html
│   └── login.html
├── tests/
│   ├── test_auth.py
│   ├── test_crud.py
│   ├── test_handlers.py
│   └── test_routing.py
├── .flake8
├── .gitignore
├── app.db
├── app.py
├── basic_http_server.py
├── cli.py
├── config.py
├── framework.log
├── logging_config.py
├── requirements.txt
└── README.md
```

## Configuration

Configuration settings are managed in the `config.py` file. You can configure anything you want: database connection, levels of logging, and secret keys.

## Routing

Routes are configured in `my_framework/routing.py`. You can define routes and their handlers using decorators:

```python
from my_framework.routing import route
from my_framework.response import Response

@route('/')
def index(request):
    return Response(body='Hello, this is the home page!')
```

## Template Rendering

Templates should be stored in `templates` directory. Use the `render_template` function to render templates with context:

```python
from my_framework.template_engine import render_template

@route('/welcome')
def welcome(request):
    return render_template('welcome.html', {'name': 'User'})
```

## Database Integration

Database integration is taken care of by SQLAlchemy. Define your models in `my_framework/models.py` and database sessions in `my_framework/db.py`.

## Authentication and Authorization

Authentication and authorization have been implemented in the file `my_framework/auth.py`. Use decorators to guard routes:

```python
from my_framework.auth import login_required, role_required

@route('/dashboard')
@login_required
def dashboard(request):
    return Response(body=f'Welcome {request.user.username} to your dashboard!')

@route('/admin')
@role_required('admin')
def admin_dashboard(request):
    return Response(body=f'Welcome {request.user.username} to the admin dashboard!')
```

## Testing

Tests are located in the `tests` directory. Use `pytest` to run the tests:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. Test things properly against the coding style and with new features included for testing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
