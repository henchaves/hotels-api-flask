from flask_restful import Resource
from models.usuario import UserModel


class Users(Resource):
    def get(self):
        return {"usuarios": [user.json() for user in UserModel.query.all()]}


class User(Resource):
    # atributos = reqparse.RequestParser()
    # atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
    # atributos.add_argument('nome')
    # atributos.add_argument('senha')

    def get(self, login):
        user = UserModel.find_user_by_login(login)
        if user:
            return user.json()
        else:
            return {"message": f"User '{login}' not found."}, 404

    def delete(self, login):
        user = UserModel.find_user_by_login(login)
        if user:
            try:
                user.delete_user()
                return {"message": f"User '{login}' deleted."}, 200
            except Exception as e:
                return {"message": f"An internal error ({e}) ocurred trying to delete user '{login}'."}, 500
        else:
            return {"message": f"User '{login}' not found."}, 404
