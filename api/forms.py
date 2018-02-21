from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class EmailPasswordForm(Form):
    email = StringField('Email', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
