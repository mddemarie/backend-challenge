from flask import Flask
from flask_restful import Api
from api.resources.users import User

app = Flask(__name__)
api = Api(app)

# api.add_resource(User, '/User', '/User/<str:id>') would be better
api.add_resource(User, '/')

if __name__ == '__main__':
    app.run(debug=True)