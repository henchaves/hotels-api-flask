from flask_restful import Resource, reqparse

hoteisLista = [
    {
        "hotel_id": "alpha",
        "nome": "Alpha Hotel",
        "estrelas": 4.3,
        "diaria": 420.30,
        "cidade": "Rio de Janeiro"
    },
    {
        "hotel_id": "bravo",
        "nome": "Bravo Hotel",
        "estrelas": 3.7,
        "diaria": 250.80,
        "cidade": "Rio de Janeiro"
    },
    {
        "hotel_id": "charlie",
        "nome": "Charlie Hotel",
        "estrelas": 4.7,
        "diaria": 400.10,
        "cidade": "Niterói"
    }
]


class Hoteis(Resource):
    def get(self):
        return {"hoteis": hoteisLista}


class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteisLista:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return {"message": "Hotel not found."}, 404  # Not found

    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        dados = argumentos.parse_args()

        novo_hotel = {
            'hotel_id': hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }

        hoteisLista.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        pass

    def delete(self, hotel_id):
        pass
