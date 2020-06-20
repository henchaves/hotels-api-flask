from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params


class Hoteis(Resource):
    path_params = reqparse.RequestParser()
    path_params.add_argument('cidade', type=str)
    path_params.add_argument('estrelas_min', type=float)
    path_params.add_argument('estrelas_max', type=float)
    path_params.add_argument('diaria_min', type=float)
    path_params.add_argument('diaria_max', type=float)
    path_params.add_argument('limit', type=int)
    path_params.add_argument('offset', type=int)

    def get(self):
        dados = Hoteis.path_params.parse_args()
        dados_validos = {k: v for k, v in dados.items() if v is not None}
        query_params = normalize_path_params(**dados_validos)
        if 'cidade' in query_params.keys():
            hoteis = HotelModel.query.filter(
                HotelModel.cidade == query_params['cidade'])
        else:
            hoteis = HotelModel.query
        hoteis_filtered = hoteis.filter(
            HotelModel.estrelas >= query_params['estrelas_min']).filter(
            HotelModel.estrelas <= query_params['estrelas_max']).filter(
            HotelModel.diaria >= query_params['diaria_min']).filter(
            HotelModel.diaria <= query_params['diaria_max']).offset(query_params['offset']).limit(query_params['limit']).all()
        return {"hoteis": [hotel.json() for hotel in hoteis_filtered]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True,
                            help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True,
                            help="Every hotel needs to be linked with a site.")

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
            if not SiteModel.find_site_by_id(dados.get('site_id')):
                return {"message": "The hotel must be associated to a valid site id."}, 400
            else:
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
