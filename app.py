from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
mail = Mail(app)

from api.views import *

if __name__ == '__main__':
    app.run()
