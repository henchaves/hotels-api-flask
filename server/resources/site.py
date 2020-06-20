from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {"sites": [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, nome):
        site = SiteModel.find_site_by_name(nome)
        if site:
            return site.json(), 200
        else:
            return {"message": f"Site '{nome}'' not found."}, 404

    def post(self, nome, url):
        if SiteModel.find_site_by_name(nome):
            return {"message": f"The site '{nome}' already exists."}, 400
        else:
            site = SiteModel(nome, url)
            try:
                site.save_site()
                return site.json()
            except Exception as e:
                return {"message": f"An internal error ({e}) ocurred trying to save site '{hotel_id}'."}, 500

    def delete(self, nome):
        site = SiteModel.find_site_by_name(nome)
        if site:
            try:
                site.delete_site()
                return {"message": f"Site '{nome}' deleted."}
            except Exception as e:
                return {"message": f"An internal error ({e}) ocurred trying to delete site '{hotel_id}'."}, 500
        else:
            return {"message": f"Site '{nome}' not found."}
