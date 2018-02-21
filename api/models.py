from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
