from flask import Flask, request, jsonify
from database import get_db_connection
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
from auth import *
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv("APP_SECRET")
app.config['JWT_SUBJECT_CLAIM'] = 'sub'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy'}), 200
    except:
        return jsonify({'status': 'unhealthy'}), 500


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # Hash the password
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = execute_signup(password_hash, data['email'], data['username'], data['role'])
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'email': new_user['email'],
            'username': new_user['username'],
            'role': new_user['role']
        }
    }), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user('email', data['email'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not bcrypt.check_password_hash(user['password_hash'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = create_access_token(identity={'id': str(user['id']), 'role': user['role']})
    return jsonify({
        'message': 'Login successful',
        'access_token': token,
        'user': {
            'username': user['username'],
            'role': user['role']
        }
    }), 200

@app.route('/protected', methods=['POST'])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    user = get_user('id', identity['id'])
    return jsonify({
        'message': f"Hello {user['username']}, you have access!",
        'received': request.get_json()
        }), 200

@app.route('/admin/users', methods=['GET'])
@jwt_required()
def admin_users():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'message': 'Admins only!'}), 403
    users = get_user()
    return jsonify({'users': users})

def check_role(identity, role):
    if identity['role'] != role:
        return jsonify({'message': f'{role} only!'}), 403
    return None

if __name__ == '__main__':
    app.run(debug=True)
