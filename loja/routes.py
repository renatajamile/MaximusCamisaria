# criar as rotas do site (os links)
from flask import render_template, url_for, redirect
from loja import app
from loja.models import Usuario
from flask_login import login_required

@app.route("/")
def homepage():
    return render_template ("homepage.html")

@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)

@app.route("/login")
def login():
    return render_template ("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template ("cadastro.html")

@app.route("/personalizar")
def personalizar():
    return render_template ("personalizar.html")

@app.route("/produtos")
def produtos():
    return render_template ("produtos.html")