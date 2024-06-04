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
    foto_perfil = database.Column(database.String, default="default_profile.png")
    
class Personalizada(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    foto = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    categoria = database.Column(database.String, nullable=False)
    cor = database.Column(database.String, nullable=False)
    tamanho = database.Column(database.String, nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)
    tecido = database.Column(database.String, nullable=False)
    texto_camisa = database.Column(database.String, nullable=False)
    observacao = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

