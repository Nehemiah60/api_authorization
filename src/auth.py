from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix="/api/v1/auth")

@auth.route("/register", methods=['GET'])
def register_user():
    return {"user1":"created successfully"}

@auth.get("/me")
def user():
    return {"message":"surrender"}