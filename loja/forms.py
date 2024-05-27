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
    username = StringField ("Nome do usuário", validators=[DataRequired()])
    userlastname = StringField("Sobrenome do usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação da senha", validators=[DataRequired(), EqualTo("senha")])
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
            return ValidationError("E-mail já cadastrado, faça login para continuar")
        
    def validate_cpf(self, cpf):
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if usuario:
            return ValidationError("CPF já cadastrado, faça login para continuar")

class FormPersonalizada(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    categorias = [('personalizada', 'Personalizada'), ('tradicional', 'Tradicional'), ('raglan', 'Raglan'),
        ('esportiva', 'Esportiva'), ('uniforme', 'Escolar'), ('longa', 'Manga Longa'), 
        ('golaV', 'Gola V'), ('golapolo', 'Gola Polo'), ('oversized', 'Oversized')]
    tamanhos = [('pp', 'PP'), ('p', 'P'), ('m', 'M'), ('g', 'G'), ('gg', 'GG')]
    tecidos = [('algodao', 'Algodão'), ('piquet', 'Piquet'), ('dryfit', 'Dry Fit'), 
        ('pvantipiling', 'PV Antipiling')]
    cores = [('#ff0000', 'Vermelho'), ('#0000ff', 'Azul'), ('#00ff00', 'Verde'), 
        ('#000000', 'Preto'), ('#ffffff', 'Branco')]
    categoria = SelectField('Categoria', choices=categorias, validators=[DataRequired()])
    tamanho = SelectField('Tamanho', choices=tamanhos, validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    tecido = SelectField('Tecido', choices=tecidos, validators=[DataRequired()])
    cor = HiddenField('Cor', validators=[DataRequired()])
    texto_camisa = StringField('Texto na Camisa', validators=[DataRequired()])
    observacao = TextAreaField('Observações')
    botao_confirmacao = SubmitField('SOLICITAR ORÇAMENTO')