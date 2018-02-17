from flask import render_template, request, jsonify, make_response
from app import app, db
import uuid, jwt, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from api.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.username:
        jsonify({'message': 'You are not logged in.'})
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    if not current_user.username:
        jsonify({'message': 'You are not logged in.'})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user was found.'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], email= data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'A new user was created.'})

@app.route('/user/<public_id>', methods = ['PUT'])
@token_required
def update_user(current_user, public_id):
    if not current_user.username:
        jsonify({'message': 'You are not logged in.'})
    data = request.get_json(force=True)
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user was found.'})
    update_username = User.query.filter_by(public_id=public_id).update(dict(username=data['username']))
    db.session.commit()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    update_password = User.query.filter_by(public_id=public_id).update(dict(password=hashed_password))
    db.session.commit()
    return jsonify({'message': 'The user was modified.'})

@app.route('/user/<public_id>', methods = ['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.username:
        jsonify({'message': 'You are not logged in.'})
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user was found.'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted.'})

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    