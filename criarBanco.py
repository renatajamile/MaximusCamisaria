from MaximusCamisaria import database, app
from MaximusCamisaria.models import Usuario

with app.app_context():
    database.create_all()