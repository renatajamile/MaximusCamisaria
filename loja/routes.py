# criar as rotas do site (os links)
from flask import render_template, url_for, redirect, request, flash
from loja import app, database, bcrypt, allowed_file
from loja.models import Usuario, Personalizada
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from loja.forms import FormLogin, FormCriarConta, FormPersonalizada

@app.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('perfil', id_usuario=current_user.id))
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=current_user.id))
    return render_template("login.html", form=form_login)

@app.route("/cadastro", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form_criarconta.username.data,
            userlastname=form_criarconta.userlastname.data,
            email=form_criarconta.email.data,
            senha=senha,
            cpf=form_criarconta.cpf.data,
            endereco=form_criarconta.endereco.data,
            complemento=form_criarconta.complemento.data,
            cidade=form_criarconta.cidade.data,
            uf=form_criarconta.uf.data,
            cep=form_criarconta.cep.data,
            telefone=form_criarconta.telefone.data
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=current_user.id))
    return render_template("cadastro.html", form=form_criarconta)

@app.route("/perfil/<id_usuario>")
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    return render_template("perfil.html", usuario=current_user.id)

@app.route("/personalizar", methods=["GET", "POST"])
@login_required
def personalizar():
    form = FormPersonalizada()
    cores = [
        ('#ff0000', 'Vermelho'),
        ('#0000ff', 'Azul'),
        ('#00ff00', 'Verde'),
        ('#000000', 'Preto'),
        ('#ffffff', 'Branco')
    ]
    if form.validate_on_submit():
        if 'foto' not in request.files:
            flash('Nenhum arquivo foi enviado.')
            return redirect(request.url)
        file = request.files['foto']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Continue com o processamento do formulário
        return redirect(url_for('solicitar_orcamento'))
    return render_template('personalizar.html', usuario=current_user, form=form, cores=cores)

@app.route('/solicitar_orcamento', methods=['GET', 'POST'])
def solicitar_orcamento():
    # Lógica para solicitar orçamento
    return "Orçamento solicitado!"

@app.route("/produtos")
def produtos():
    return render_template ("produtos.html")

@app.route("/fale")
@login_required
def fale():
    return render_template("fale.html", usuario=current_user)
@app.route("/carrinho")
@login_required
def carrinho():
    return render_template ("carrinho.html", usuario=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))