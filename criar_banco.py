from loja import database, app
from loja.models import Usuario, Personalizada

with app.app_context():
    database.create_all()