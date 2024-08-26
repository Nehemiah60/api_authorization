from flask import Blueprint, jsonify, request
from src.models import User, db
import validators
from werkzeug.security import (check_password_hash, 
                                generate_password_hash)
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, jwt_required, get_jwt_identity)


auth = Blueprint('auth', __name__, url_prefix="/api/v1/auth")

@auth.route("/register", methods=['POST'])
def register_user():
    body = request.get_json()

    username = body.get('username')
    email = body.get('email')
    user_password = body.get('user_password')

    if len(user_password) < 8:
        return jsonify({
            'error': "Password is too short"
        })

    if len(username) < 3:
        return jsonify({
            'error': "Username is too short"
        })
    
    if not username.isalnum() or " " in username:
        return jsonify({
            "error": "Username should be alphanumeric and no spaces"
        })

    if not validators.email(email):
        return jsonify({
            'error':"Email not valid"
        })
    
    # Check if user already exists in our db
    existing_user = User.query.filter_by(username=username).first()
     
    if existing_user:
        return jsonify({
            'error': "That user already exists"
        })
    # Check if email already exists
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({
            'error': "The email is taken"
        })
    
    hashed_password = generate_password_hash(user_password)
    user = User(
        username=username,
        email = email,
        user_password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created successfully",
        'user':{
            'username': username,
            'email': email
        }
    })

@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body.get('email')
    user_password = body.get('user_password')

    user = User.query.filter_by(email=email).first()
    
    if user:

        check_password = check_password_hash(user.user_password, user_password)
            
        if check_password:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                    'user':{
                        'refresh': refresh,
                        'access': access,
                        'name': user.username,
                        'email': user.email
                    }
                })
        
    return jsonify({
                    'message':'Wrong credentials'
                        })

# Get specific user details based on provided web tokens
@auth.route('/users/details', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    })

#The endpoint to refresh access tokens

@auth.route('/tokens/refresh', methods=['GET', 'POST'])
@jwt_required(refresh=True)
def refresh_tokens():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    })


#Get a list of all the users saved in the database
@auth.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users':[user.username for user in users]})

   