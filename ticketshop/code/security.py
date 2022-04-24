from models.userModel import UserModel

def authenticate (email, password):
    user = UserModel.find_by_email(email)
    if user and user.password == password:
        return user

def identity (payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)