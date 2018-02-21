from Flask import jsonify
from flask_testing import TestCase
import unittest
from app import app, db

from api.models import User


class UserAPITest(TestCase):

    def create_app(self):
        DEBUG = True
        app.config['TESTING'] = True
        return app

    def setUp(self):
        '''
        Configurations for Testing, with a separate test database.
        '''
        TESTING = True
        WTF_CSRF_ENABLED = False
        SQLALCHEMY_DATABASE_URI = 'sqlite://'
        HASH_ROUNDS = 1

        self.app = app
        self.client = self.app.test_client
        self.user = {
            'username': 'Marie',
            'email': 'marie@gmail.com',
            'password': '12345'
        }
        with self.app.app_context():
            db.create_all()

    '''
    Here I wanted to set the logged user but it did not work.
    I would have to know much more about request context in Flask.

    def test_adduser(self):
        user = User(username="test", email="test@test.com")
        user2 = User(username="lucas", email="lucas@test.com")

        db.session.add(user)
        db.session.commit()

        assert user in db.session
        assert user2 not in db.session

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=user.username,
            password=user.password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login(self):
        rv = self.login('lucas', 'test')
        assert 'You were logged in' in rv.data
    '''

    def test_create_user_works_unauthenticated(self):
        '''
        Unauthenticated user is allowed to create an account
        '''
        response = self.client().post('/user', data=self.user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.first, jsonify({
            'message': 'A new user was created.'
        }))

    def test_create_user_fails_authenticated(self):
        '''
        Authenticated user is not allowed to create another account
        '''
        user = User(username="Joe", email="joe@joes.com", password="12345")
        db.session.add(user)
        db.session.commit()
        with self.client:
            self.client().get('/login', data=user)
            response = self.client().post('/user', data=user)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, jsonify({
                'message': 'You already have an account and are logged in.'
            }))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
