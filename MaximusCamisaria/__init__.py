from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates/')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///camisaria.db"

database = SQLAlchemy(app)

from MaximusCamisaria import routes