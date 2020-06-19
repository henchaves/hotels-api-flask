from flask import Flask
from flask_restful import Api
from resources.hotel import Hotel, Hoteis
from resources.usuario import User, Users
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis/')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>/')
api.add_resource(Users, '/usuarios/')
api.add_resource(User, '/usuarios/<string:login>/')

banco.init_app(app)


# if __name__ == "__main__":
#   app.run(debug=True)
# from sql_alchemy import banco
# banco.init_app(app)
