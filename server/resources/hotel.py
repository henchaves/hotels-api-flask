from flask_restful import Resource, reqparse
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
        return {"hoteis": hoteisLista}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found."}, 404  # Not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            # Bad request
            return {'message': f"hotel_id '{hotel_id}' already exists."}, 400
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return hotel.json(), 200
        else:
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201

    def delete(self, hotel_id):
        hotelToDelete = Hotel.find_hotel(hotel_id)
        if hotelToDelete:
            global hoteisLista
            hoteisLista = [
                hotel for hotel in hoteisLista if hotel['hotel_id'] != hotel_id
            ]
            return hotelToDelete, 200
        return {"message": "Hotel not found."}, 404
