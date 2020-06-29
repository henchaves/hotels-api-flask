from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hotel, Hoteis
from resources.usuario import User, Users, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Sites, Site
from flask_jwt_extended import JWTManager
from db_credentials import *
from sql_alchemy import banco
from blacklist import BLACKLIST

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_ADDRESS}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return "<h1>Hello World!</h1>"


@app.before_first_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({"message": "You have been logged out."}), 401


api.add_resource(Hoteis, '/hoteis/')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>/')
api.add_resource(Users, '/usuarios/')
api.add_resource(User, '/usuarios/<string:login>/')
api.add_resource(UserRegister, '/cadastro/')
api.add_resource(UserLogin, '/login/')
api.add_resource(UserLogout, '/logout/')
api.add_resource(Sites, '/sites/')
api.add_resource(Site, '/sites/<string:nome>/')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>/')

banco.init_app(app)
