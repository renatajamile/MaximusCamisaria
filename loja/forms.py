# criar os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from loja.models import Usuario 

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Entrar")

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
    botao_confirmacao = SubmitField("Cadastrar")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")
        
    def validate_cpf(self, cpf):
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if usuario:
            return ValidationError("CPF já cadastrado, faça login para continuar")