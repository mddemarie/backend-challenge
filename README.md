# Vimcar Coding Challenge: Backend

Building a web app using Python, Flask RESTful. It follows typical RESTful API design pattern.

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

