from flask_restful import Resource, reqparse

from models.userModel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type =str, required = True, help="Es muss eine Emailadresse angegeben werden")
    parser.add_argument('password', type=str, required=True, help="Es muss ein Passwort angegeben werden")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "Es gibt bereits einen User mit derselben Emailadresse."}, 400

        user = UserModel(data['email'], data['password'])
        user.save_to_db()

        return {"message": "User erfolgreich erstellt."}, 201

class User(Resource):
    def get(self, email):
        user = UserModel.find_by_email(email)
        if user:
            return user.json()

        return {"message": "Es gibt keinen User mit dieser Emailadresse."}, 400


    def delete(self, email):
        user = UserModel.find_by_email(email)
        if user:
            user.delete_from_db()
        return {"message": "User erfolgreich geloescht."}, 200

