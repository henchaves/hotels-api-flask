from flask import Flask
from flask_restful import Api
from resources.hotel import Hotel, Hoteis
from resources.usuario import User, Users, UserRegister, UserLogin
from flask_jwt_extended import JWTManager
from sql_alchemy import banco

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'

api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis/')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>/')
api.add_resource(Users, '/usuarios/')
api.add_resource(User, '/usuarios/<string:login>/')
api.add_resource(UserRegister, '/cadastro/')
api.add_resource(UserLogin, '/login/')

banco.init_app(app)


# if __name__ == "__main__":
#   app.run(debug=True)
# from sql_alchemy import banco
# banco.init_app(app)
