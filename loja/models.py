# criar a estrutura do banco de dados
from loja import database

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    userlastname = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    cpf = database.Column(database.String(11), nullable=False)
    endereco = database.Column(database.String, nullable=False)
    complemento = database.Column(database.String, nullable=False)
    cidade = database.Column(database.String, nullable=False)
    uf = database.Column(database.String(2), nullable=False)
    cep = database.Column(database.String(8), nullable=False)
    telefone = database.Column(database.String, nullable=False)

