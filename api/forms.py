from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField

class LoginForm(FlaskForm):
    email = TextField('email')
    password = PasswordField('password')