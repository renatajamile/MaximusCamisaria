# criar as rotas do site (os links)
from flask import render_template, url_for, redirect
from loja import app, database, bcrypt
from loja.models import Usuario, Personalizada
from flask_login import login_required, login_user, logout_user, current_user
from loja.forms import FormLogin, FormCriarConta

@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('perfil', usuario=current_user.username))
    return render_template("homepage.html")

@app.route("/login", methods =["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil",usuario=usuario.username))
    return render_template ("login.html", form=form_login)


@app.route("/cadastro", methods =["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, userlastname=form_criarconta.userlastname.data, 
                          email=form_criarconta.email.data, senha=senha,
                          cpf=form_criarconta.cpf.data, endereco=form_criarconta.endereco.data,
                          complemento=form_criarconta.complemento.data,
                          cidade=form_criarconta.cidade.data, uf=form_criarconta.uf.data,
                          cep=form_criarconta.cep.data, telefone=form_criarconta.telefone.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil",usuario=usuario.username))
    return render_template ("cadastro.html", form=form_criarconta)

@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)

@app.route("/personalizar")
@login_required
def personalizar():
    return render_template ("personalizar.html", usuario=current_user.username)

@app.route("/produtos")
def produtos():
    return render_template ("produtos.html")

@app.route("/fale")
@login_required
def fale():
    return render_template("fale.html", usuario=current_user.username)

@app.route("/carrinho")
@login_required
def carrinho():
    return render_template ("carrinho.html", usuario=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))