from flask import render_template, url_for
from MaximusCamisaria import app

@app.route("/")
def homepage():
    return render_template("estrutura.html")

@app.route("/perfil/<usuario>")
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html")