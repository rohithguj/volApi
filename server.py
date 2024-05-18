from flask import Flask, jsonify, request
from database import create_user_table, add_user, get_user_by_id, get_user_by_username
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/signin', methods=['POST'])
def login():
    # Retrieve JSON data from the request
    data = request.json

    # Check if data is missing
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Extract username and password from the JSON data
    username = data.get('username')
    password = data.get('password')

    # Check if username or password is missing
    if not username or not password:
        return jsonify({'error': 'Username or password missing'}), 400

    # Retrieve user from the database by username
    user = get_user_by_username(username)

    # Check if user exists
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if password matches
    if user['password'] != password:
        return jsonify({'error': 'Incorrect password'}), 401

    # If everything is valid, return success response
    return jsonify({'message': 'Login successful', 'user_id': user['id']}), 200

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']

    # print(username + ' ' + password)

    # Check if the username already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({'status': 'Username already exists'}), 409
    
    # Add the user
    user_id = add_user(username, password)
    if user_id:
        return jsonify({'status': 'User created successfully', 'user_id': user_id}), 201
    else:
        return jsonify({'status': 'Failed to create user'}), 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing username or email'}), 400
    
    user_id = add_user(data['username'], data['email'])
    return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)
