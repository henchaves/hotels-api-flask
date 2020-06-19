from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.hotel import HotelModel

# hoteisLista = [
#     {
#         "hotel_id": "alpha",
#         "nome": "Alpha Hotel",
#         "estrelas": 4.3,
#         "diaria": 420.30,
#         "cidade": "Rio de Janeiro"
#     },
#     {
#         "hotel_id": "bravo",
#         "nome": "Bravo Hotel",
#         "estrelas": 3.7,
#         "diaria": 250.80,
#         "cidade": "Rio de Janeiro"
#     },
#     {
#         "hotel_id": "charlie",
#         "nome": "Charlie Hotel",
#         "estrelas": 4.7,
#         "diaria": 400.10,
#         "cidade": "Niterói"
#     }
# ]


class Hoteis(Resource):
    def get(self):
        return {"hoteis": [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True,
                            help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        else:
            return {"message": f"Hotel '{hotel_id}' not found."}, 404  # Not found

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            # Bad request
            return {'message': f"Hotel '{hotel_id}' already exists."}, 400
        else:
            dados = Hotel.argumentos.parse_args()
            hotel = HotelModel(hotel_id, **dados)
            try:
                hotel.save_hotel()
                return hotel.json()
            except Exception as e:
                # Internal Server Error
                return {"message": f"An internal error ({e}) ocurred trying to save hotel '{hotel_id}'."}, 500

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
        else:
            hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
            return hotel.json()
        except Exception as e:
            # Internal Server Error
            return {"message": f"An internal error ({e}) ocurred trying to save hotel '{hotel_id}'."}, 500

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {"message": f"Hotel '{hotel_id}' deleted."}, 200
            except Exception as e:
                return {"message": f"An internal error ({e}) ocurred trying to delete hotel'{hotel_id}'."}, 500
        else:
            return {"message": f"Hotel '{hotel_id}' not found."}, 404
