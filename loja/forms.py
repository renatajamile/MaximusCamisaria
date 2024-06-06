# criar os formulários do site
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, IntegerField, HiddenField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from loja.models import Usuario, Personalizada


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("ENTRAR")


class FormCriarConta(FlaskForm):
    username = StringField("Nome do usuário", validators=[DataRequired()])
    userlastname = StringField(
        "Sobrenome do usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação da senha", validators=[
                                      DataRequired(), EqualTo("senha")])
    cpf = StringField("CPF", validators=[DataRequired()])
    endereco = StringField("Endereço", validators=[DataRequired()])
    complemento = StringField("Complemento", validators=[DataRequired()])
    cidade = StringField("Cidade", validators=[DataRequired()])
    uf = StringField("UF", validators=[DataRequired()])
    cep = StringField("CEP", validators=[DataRequired()])
    telefone = StringField("Telefone", validators=[DataRequired()])
    botao_confirmacao = SubmitField("CADASTRAR")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(
                "E-mail já cadastrado, faça login para continuar")

    def validate_cpf(self, cpf):
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if usuario:
            raise ValidationError(
                "CPF já cadastrado, faça login para continuar")


class FormPersonalizada(FlaskForm):
    foto = FileField('Foto')
    categorias = [('personalizada', 'Personalizada'), ('tradicional', 'Tradicional'), ('raglan', 'Raglan'),
                  ('esportiva', 'Esportiva'), ('uniforme',
                                               'Escolar'), ('longa', 'Manga Longa'),
                  ('golaV', 'Gola V'), ('golapolo', 'Gola Polo'), ('oversized', 'Oversized')]
    tamanhos = [('pp', 'PP'), ('p', 'P'), ('m', 'M'), ('g', 'G'), ('gg', 'GG')]
    tecidos = [('algodao', 'Algodão'), ('piquet', 'Piquet'), ('dryfit', 'Dry Fit'),
               ('pvantipiling', 'PV Antipiling')]
    categoria = SelectField(
        'Categoria', choices=categorias, validators=[DataRequired()])
    tamanho = SelectField('Tamanho', choices=tamanhos,
                          validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    tecido = SelectField('Tecido', choices=tecidos,
                         validators=[DataRequired()])
    cor = HiddenField('Cor')
    texto_camisa = StringField('Texto na Camisa', validators=[DataRequired()])
    observacao = TextAreaField('Observações')
    botao_confirmacao = SubmitField('ENVIAR')


class FormAtualizarConta(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    userlastname = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    complemento = StringField('Complemento')
    cidade = StringField('Cidade', validators=[DataRequired()])
    uf = StringField('UF', validators=[DataRequired()])
    cep = StringField('CEP', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')


class FormAtualizarFotoPerfil(FlaskForm):
    foto_perfil = FileField("Atualizar Foto de Perfil",
                            validators=[DataRequired()])
    botao_confirmacao = SubmitField("ATUALIZAR")
