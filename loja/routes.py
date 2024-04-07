# criar as rotas do site (os links)
from flask import render_template, url_for
from loja import app

@app.route("/")
def homepage():
    return render_template("inicio.html")

@app.route("/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html",usuario=usuario)

