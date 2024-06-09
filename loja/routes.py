# criar as rotas do site (os links)
import os
import uuid
from datetime import datetime
from flask import render_template, url_for, redirect, request, flash
from loja import app, database, bcrypt, allowed_file
from loja.models import Usuario, Personalizada
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from loja.forms import FormLogin, FormCriarConta, FormPersonalizada, FormAtualizarConta, FormAtualizarFotoPerfil

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
        # Verificar se o email já existe
        if Usuario.query.filter_by(email=form_criarconta.email.data).first():
            flash('O e-mail informado já está cadastrado. Por favor, tente outro e-mail.', 'danger')
            return redirect(url_for('criarconta'))
        
        # Verificar se o CPF já existe
        if Usuario.query.filter_by(cpf=form_criarconta.cpf.data).first():
            flash('O CPF informado já está cadastrado. Por favor, tente outro CPF.', 'danger')
            return redirect(url_for('criarconta'))

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
        try:
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario, remember=True)
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for("perfil", id_usuario=current_user.id))
        except IntegrityError:
            database.session.rollback()
            flash('Ocorreu um erro ao criar a conta. Por favor, tente novamente.', 'danger')

    return render_template("cadastro.html", form=form_criarconta)


#rota para visualizar os dados
@app.route("/visualizarDados")
@login_required
def visualizarDados():
    return render_template("visualizar_dados.html", usuario=current_user.id)

@app.route("/editar_usuario/<int:id_usuario>", methods=["GET", "POST"])
@login_required
def editar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if usuario != current_user:
        abort(403)  # Proibir acesso se o usuário não for o atual

    form = FormAtualizarConta()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.userlastname = form.userlastname.data
        current_user.email = form.email.data
        current_user.cpf = form.cpf.data
        current_user.endereco = form.endereco.data
        current_user.complemento = form.complemento.data
        current_user.cidade = form.cidade.data
        current_user.uf = form.uf.data
        current_user.cep = form.cep.data
        current_user.telefone = form.telefone.data
        database.session.commit()
        flash("Conta atualizada com sucesso.", "success")
        return redirect(url_for("visualizarDados"))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.userlastname.data = current_user.userlastname
        form.email.data = current_user.email
        form.cpf.data = current_user.cpf
        form.endereco.data = current_user.endereco
        form.complemento.data = current_user.complemento
        form.cidade.data = current_user.cidade
        form.uf.data = current_user.uf
        form.cep.data = current_user.cep
        form.telefone.data = current_user.telefone

    return render_template('editar_usuario.html', form=form)

@app.route("/perfil/<id_usuario>")
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    return render_template("perfil.html", usuario=current_user.id)

@app.route("/personalizar", methods=["GET", "POST"])
@login_required
def personalizar():
    form = FormPersonalizada()
    if form.validate_on_submit():
        if form.foto.data:  # Verifica se foi enviado um arquivo de foto
            file = form.foto.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()  # Obter a extensão do arquivo
                unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                file.save(upload_path)
        else:  # Se não houver arquivo de foto, defina como vazio
            unique_filename = ''
        
        cor_selecionada = form.cor.data if form.cor.data else ''  # Verifica se a cor foi selecionada
        
        nova_personalizada = Personalizada(
            foto=unique_filename,
            categoria=form.categoria.data,
            cor=cor_selecionada,
            tamanho=form.tamanho.data,
            quantidade=form.quantidade.data,
            tecido=form.tecido.data,
            texto_camisa=form.texto_camisa.data,
            observacao=form.observacao.data,
            id_usuario=current_user.id
        )
        
        database.session.add(nova_personalizada)
        database.session.commit()
        
        return redirect(url_for('carrinho'))
    
    return render_template('personalizar.html', usuario=current_user, form=form)

@app.route("/produtos")
def produtos():
    return render_template ("produtos.html")

# ROTA FALE
@app.route("/fale")
@login_required
def fale():
    return render_template("fale.html", usuario=current_user)

@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    assunto = request.form["assunto"]
    mensagem = request.form["mensagem"]
    return render_template("fale.html", mensagem_sucesso="Mensagem enviada com sucesso!", usuario=current_user)


# ROTA Avaliação
@app.route("/avaliacao")
@login_required
def avaliacao():
    return render_template("avaliacao.html", usuario=current_user)

# ROTA DA MINHA CONTA
@app.route("/minhaconta")
@login_required
def minhaconta():
    return render_template("minhaconta.html", usuario=current_user)

@app.route("/atualizar_foto_perfil", methods=["GET", "POST"])
@login_required
def atualizar_foto_perfil():
    form = FormAtualizarFotoPerfil()
    if form.validate_on_submit():
        if form.foto_perfil.data:
            file = form.foto_perfil.data
            if file and allowed_file(file.filename):
                # Excluir a foto antiga se não for a padrão
                if current_user.foto_perfil != 'default_profile.png':
                    try:
                        os.remove(os.path.join(app.config['PROFILE_PIC_UPLOAD_FOLDER'], current_user.foto_perfil))
                    except Exception as e:
                        print(f"Erro ao excluir a imagem antiga: {e}")

                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"
                upload_path = os.path.join(app.config['PROFILE_PIC_UPLOAD_FOLDER'], unique_filename)
                file.save(upload_path)
                current_user.foto_perfil = unique_filename

                database.session.commit()
                flash("Foto de perfil atualizada com sucesso.", "success")
                return redirect(url_for("minhaconta", id_usuario=current_user.id))
        else:
            flash("Nenhum arquivo selecionado.", "danger")
    return render_template("atualizar_foto_perfil.html", form=form)

@app.route("/excluir_foto_perfil", methods=["POST"])
@login_required
def excluir_foto_perfil():
    # Excluir a foto antiga se não for a padrão
    if current_user.foto_perfil != 'default_profile.png':
        try:
            os.remove(os.path.join(app.config['PROFILE_PIC_UPLOAD_FOLDER'], current_user.foto_perfil))
        except Exception as e:
            print(f"Erro ao excluir a imagem antiga: {e}")
    
    current_user.foto_perfil = 'default_profile.png'
    database.session.commit()
    flash("Foto de perfil excluída com sucesso.", "success")
    return redirect(url_for("minhaconta", id_usuario=current_user.id))

@app.route('/profile/<filename>')
def profile(filename):
    file_url = url_for('static', filename=f'profile_pics/{filename}')
    return render_template('minhaconta.html', file_url=file_url)

@app.route("/carrinho")
@login_required
def carrinho():
    # Consulta todos os itens personalizados do usuário atual
    itens_personalizados = Personalizada.query.filter_by(id_usuario=current_user.id).all()
    return render_template("carrinho.html", itens_personalizados=itens_personalizados)

@app.route("/deletar_item/<int:id>")
@login_required
def deletar_item(id):
    item = Personalizada.query.get_or_404(id)
    if item.id_usuario != current_user.id:
        abort(403)  # Proibir acesso se o item não pertencer ao usuário atual

    # Excluir a imagem do sistema de arquivos
    if item.foto != "default.png":
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.foto))
        except Exception as e:
            print(f"Erro ao excluir a imagem: {e}")

    database.session.delete(item)
    database.session.commit()
    flash('Item deletado com sucesso.')
    return redirect(url_for('carrinho'))

@app.route("/editar_item/<int:id>", methods=["GET", "POST"])
@login_required
def editar_item(id):
    item = Personalizada.query.get_or_404(id)
    form = FormPersonalizada()

    if form.validate_on_submit():
        if form.foto.data:  # Verifica se foi enviado um arquivo de foto
            file = form.foto.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()  # Obter a extensão do arquivo
                unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(upload_path)
                item.foto = unique_filename
        elif "remove_foto" in request.form:
            item.foto = None

        item.categoria = form.categoria.data
        item.cor = form.cor.data  # Atualiza a cor do item
        item.tamanho = form.tamanho.data
        item.quantidade = form.quantidade.data
        item.tecido = form.tecido.data
        item.texto_camisa = form.texto_camisa.data
        item.observacao = form.observacao.data

        database.session.commit()
        return redirect(url_for('carrinho'))

    # Preencher o formulário com os valores atuais do item
    form.categoria.data = item.categoria
    form.cor.data = item.cor
    form.tamanho.data = item.tamanho
    form.quantidade.data = item.quantidade
    form.tecido.data = item.tecido
    form.texto_camisa.data = item.texto_camisa
    form.observacao.data = item.observacao

    return render_template('editar_item.html', form=form, item=item)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))