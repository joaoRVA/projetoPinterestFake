# criar os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from FakePinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirm = SubmitField("Fazer Login")


class FormCadastro(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    senha_confirm = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirm = SubmitField("Fazer Cadastro")

    # validador de e-mail

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first() # se tiver um e-mail aqui, ele pega o primeiro e joga na variavel

        if usuario:
            return ValidationError("E-mail já cadastrado, faça login ou cadastre outro E-mail.")
        
class FormFotos(FlaskForm):
    fotos = FileField("Foto", validators=[DataRequired()])
    botao_confirm = SubmitField("Enviar")