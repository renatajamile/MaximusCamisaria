from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Equalto, Length, ValidationError
from MaximusCamisaria.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer Login")


class FormCadastro(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    userlastname = StringField("Userlastname", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacaoSenha = PasswordField("Confirmacao de Senha", validators=[DataRequired(), Equalto("senha")])
    botao = SubmitField("criar conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("Email já cadastrado, faça login para continuar")