from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp
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

    @jwt_required
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


class UserRegister(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('nome', type=str)
        atributos.add_argument('login', type=str, required=True,
                               help="The field 'login' cannot be left blank.")
        atributos.add_argument('senha', type=str, required=True,
                               help="The field 'senha' cannot be left blank.")
        dados = atributos.parse_args()
        if UserModel.find_user_by_login(dados['login']):
            return {"message": f"User '{dados['login']}' already exists."}
        else:
            user = UserModel(**dados)
            user.save_user()
            return {"message": f"User '{dados['login']}' created successfully!"}, 201


class UserLogin(Resource):

    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True,
                               help="The field 'login' cannot be left blank.")
        atributos.add_argument('senha', type=str, required=True,
                               help="The field 'senha' cannot be left blank.")
        dados = atributos.parse_args()
        user = UserModel.find_user_by_login(dados['login'])
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {"access_token": token_de_acesso}, 200
        else:
            # Unauthorized
            return {"message": "The username or password is incorrect."}, 401
