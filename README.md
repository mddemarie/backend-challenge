# Vimcar Coding Challenge: Backend

Building a web app using Python, Flask. It follows typical RESTful API design pattern.

## SETUP

I assume you already installed Python 3.4 or higher and pip.

### Virtual Environment

Install virtualenv via pip:

```
$ pip3 install virtualenv
```

Create a virtual environment for a project:

```
$ cd backend-challenge
$ python3 -m venv vimcar
```

To begin using the virtual environment, it needs to be activated:

```
$ source vimcar/bin/activate
```

Install the same packages using the same versions:

```
(venv) $ pip3 install -r requirements.txt
```

### Database

Before you run the server, you will have to create a database.
First, go to the Python shell (while you are in your virtualenv) and import the database from `app.py`:

```
from app import db
```

Secord, create the database with this command:

```
db.create_all()
```

### Run server

With this command:

```
(venv) $ export FLASK_APP=app.py
(venv) $ export PYTHONPATH=/Path/to/the/app
(venv) $ flask run
```

### In Browser

Paste this url and hit enter:

```
http://localhost:5000/login
```

### Tests

You can run the tests with this command:

```
(venv) $ python3 api/test_views.py
```

### How I decided what tests to write

I decided for the API integration tests because they test the overall functionality of the API endpoint (error messages, response codes, headers...). This is very important aspect for RESTful design architecture.

**Integration tests**:

I write the integration tests in this order:

**POST - GET - GET:id - PUT - DELETE.**

For each HTTP method, I start with as little functionality as possible.
I write the integration tests for each HTTP method in this order:

- test for creating a user without authentication
- test for creating a user with authentication
- other edge cases

What response code the test returns does not influence my decision in which order I write an integration test. This way, I make sure that all test cases are covered.

### REST API Architecture

- **GET user/** – Retrieves list of users
(authentication necessary)
- **GET user/<public_id>** – Retrieves the one users details of the <public_id>
(authentication necessary)
- **POST user/** – Create a new user without authentication
- **DELETE user/<public_id>** – Delete the user of the <public_id>
(authentication necessary)
- **PUT tasks/<public_id>** – Update the user of the <public_id>
(authentication necessary)

### What is not working?

- integration tests are not running properly:
	1. `test_create_user_works_unauthenticated` should work and return the POST method should return the response code 201.
	2. `test_create_user_fails_authenticated` is not able to login, this does not work because of the request context in Flask (<http://flask.pocoo.org/docs/0.12/reqcontext/>), I would have to look it up in more detail.

- the user has to log in with username and password and according to the authentication task description, this is not correct. _The user should log in into the system with email and password instead!_ I was not able to change it because `auth.email` does not exist.

### Suggestions for Improvement

- the usage of the module `bcrypt` is safer
- it is better to hash and check the password in the models.py than in the views.py
- the functionality for sign up should be improved - **email confirmation** is totally **missing**. The sign up enables only the token generation that grants an authorized access to a protected source (GET, GET:id, PUT, DELETE). Anonymous access to POST method is possible due to necessary sign up (= creating of new user).
- the sign up could implement `EmailPasswordForm` in forms.py that could be displayed on the home page for creating a new account (not obligatory for the task). 
- it would be great to have **migrations** for changes that happen in the database fields/tables - possible to do with Alembic that is installed with requirements.txt.
- **more integration tests** in `test_views.py` are needed for checking RESTful architechture: very important for catching errors that could return the response code 500, overwriting wrong success response codes and giving appropriate error messages if the HTTP request is not successful
- **unit tests** for the `models.py` and `forms.py` are missing
- the RESTful API documentation is missing (not obligatory). I usually write it with Swagger UI.

**Please note:**
I am going to work on this app during the following weeks and will use the branch "experiment" for this purpose. Check that out for more details.