from flask_restful import Resource

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
        pass

    def put(self, hotel_id):
        pass

    def delete(self, hotel_id):
        pass
