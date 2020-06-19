from sql_alchemy import banco


class UsuerModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100))
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha

    def json(self):
        return {
            "user_id": self.user_id,
            "nome": self.nome,
            "login": self.login
        }

    @classmethod
    def find_user_by_id(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        else:
            return None

    @classmethod
    def find_user_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        else:
            return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
