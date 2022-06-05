from models.userModel import UserModel
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash


def authenticate (email, password):
    user = UserModel.find_by_email(email)
    if user and check_password_hash(user.password, password):
        return user

def identity (payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)