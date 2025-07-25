import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from models import db
from uuid import uuid4
from blacklist import blacklist
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Dummy in-memory store (for demo)
# users = []

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     try:
#         data = request.get_json(force=True)
#         print("Incoming data:", data)

#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')

#         if not username or not email or not password or not role:
#             return jsonify({'error': 'Missing fields'}), 400

#         hashed_password = generate_password_hash(password)

#         users.append({
#             'username': username,
#             'email': email,
#             'password': hashed_password,
#             'role': role
#         })

#         return jsonify({'message': 'User registered successfully'}), 201

#     except Exception as e:
#         # NEW LINE: Print the actual error to the terminal
#         print("EXCEPTION:", str(e))
#         return jsonify({'error': 'Something went wrong'}), 500


# 🔐 REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create and save user
    new_user = User(email=email, password=hashed_password, username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201





# 🔑 LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'username': user.username,
            'access_token': access_token,
            'role': user.role
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401



# 🔓 LOGOUT
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # token ID
    blacklist.add(jti)
    return jsonify({"message": "Logged out successfully"}), 200




@auth_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if request.method == 'GET':
        return jsonify({
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'profile_image': user.profile_image
        })

    # 🟡 PUT = Update profile + image
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    image = request.files.get('profile_image')

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = generate_password_hash(password)

    if image:
        filename = secure_filename(image.filename)
        unique_filename = f"{uuid4()}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static/profile_pics')
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, unique_filename)
        image.save(image_path)
        user.profile_image = unique_filename

    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'}), 200



# ❌ DELETE ACCOUNT
@auth_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Account deleted successfully'}), 200


