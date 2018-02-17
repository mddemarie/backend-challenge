from flask_testing import TestCase
import unittest
from app import app, db

from api.models import User

class UserAPITest(TestCase):

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
    # TESTING = True

    def create_app(self):
        DEBUG = True
        app.config['TESTING'] = True
        return app

    def setUp(self):
        #self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {
            'username': 'Marie',
            'email': 'marie@gmail.com',
            'password': '12345'
        }
        with self.app.app_context():
            db.create_all()
    
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=user.username,
            password=user.password
        ))
    
    def test_create_user_works_as_non_user(self):
        '''
        Unauthenticated user is allowed to create an account
        '''
        response = self.client().post('/user', data=self.user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.first, jsonify({'message': 'A new user was created.'}))

    def test_create_user_fails_as_user(self):
        '''
        Authenticated user is not allowed to create another account
        '''
        self.login('Jane', 'einewelt')
        response = self.client().post('/user', data=self.user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, jsonify({'message': 'You already have an account and are logged in.'}))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
