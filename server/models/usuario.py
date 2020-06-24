from sql_alchemy import banco
from flask import request, url_for
from requests import post
import yagmail
from email_credentials import EMAIL, PASSWORD

MAILGUN_DOMAIN = "sandbox7678d1582790407a9948f037fc15b994.mailgun.org"
MAILGUN_API_KEY = "595e7234581cbab54c9d6d6a04a718f0-468bde97-270ab189"
FROM_TITLE = "NO-REPLY"
FROM_EMAIL = "no-reply@restapi.com"


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100))
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, nome, login, email, senha, ativado):
        self.nome = nome
        self.login = login
        self.email = email
        self.senha = senha
        self.ativado = ativado

    def json(self):
        return {
            "user_id": self.user_id,
            "nome": self.nome,
            "login": self.login,
            "email": self.email,
            "ativado": self.ativado
        }

    def send_confirmation_email(self):
        yag = yagmail.SMTP(EMAIL, PASSWORD)
        link = request.url_root[:-1] + \
            url_for('userconfirm', user_id=self.user_id)

        contents = [f"""<html>
                        <p>Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR E-MAIL</a></p>
                    </html>"""]
        yag.send(self.email, 'NO-REPLY: Confirmação de Cadastro', contents)

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

    @classmethod
    def find_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
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
