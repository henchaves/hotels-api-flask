from sql_alchemy import banco


class SiteModel(banco.Model):
    __table__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(40))
    url = banco.Column(banco.String(80))
    # Lista de objetos hoteis que possuem o site_id como chave secundaria
    hoteis = banco.relationship('HotelModel')

    def __init__(self, nome, url):
        self.nome = nome
        self.url = url

    def json(self):
        return {
            "site_id": self.site_id,
            "nome": self.nome,
            "url": self.url,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site_by_name(cls, nome):
        site = cls.query.filter_by(nome=nome).first()
        if site:
            return site
        else:
            return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()
