# criar a estrutura do banco de dados
from loja import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    userlastname = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    cpf = database.Column(database.String(11), nullable=False, unique=True)
    endereco = database.Column(database.String, nullable=False)
    complemento = database.Column(database.String, nullable=False)
    cidade = database.Column(database.String, nullable=False)
    uf = database.Column(database.String(2), nullable=False)
    cep = database.Column(database.String(8), nullable=False)
    telefone = database.Column(database.String, nullable=False)

class Produto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    foto_produto = database.Column(database.String, default ="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    nome_produto = database.Column(database.String, nullable=False)
    tamanho_produto = database.Column(database.String, nullable=False)
    cor_produto = database.Column(database.String, nullable=False)
    categoria_produto = database.Column(database.String, nullable=False)
    descricao_produto = database.Column(database.String, nullable=False)
    quantidade_produto = database.Column(database.Integer, nullable=False)

class Personalizada(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    foto_personalizada = database.Column(database.String, default ="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    tamanho_personalizada = database.Column(database.String, nullable=False)
    especificacao_personalizada = database.Column(database.String, nullable=False)
    cor_personalizada = database.Column(database.String, nullable=False)
    quantidade_personalizada = database.Column(database.Integer, nullable=False)
    observacao_personalizada = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)