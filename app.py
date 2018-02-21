from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
mail = Mail(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

from api.models import User

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()

from api.views import *

if __name__ == '__main__':
    app.run()
