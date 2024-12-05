# Rotas do site (links)
from flask import render_template, url_for, redirect
from FakePinterest import app, bcrypt, database
from FakePinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from FakePinterest.forms import FormCadastro, FormLogin, FormFotos
import os
from werkzeug.utils import secure_filename

# ====== HomePage/Login ======
@app.route("/", methods=["GET", "POST"]) # permitir que essa página utilize o método post
def homepage():
    formLogin = FormLogin()

    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
        
    return render_template("homepage.html", form=formLogin)
# ====== HomePage/Login ======



# ====== Cadastro ======
@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    formCadastro = FormCadastro()

    if formCadastro.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCadastro.senha.data) # criptografar senha
        usuario = Usuario(username=formCadastro.username.data, email=formCadastro.email.data, senha=senha)

        database.session.add(usuario) # faz a conexão com o banco de dados, abrindo uma sessão
        database.session.commit() # faz o commit de todas as informações até agora no banco de dados

        login_user(usuario, remember=True) # faz login e possibilita o navegador lembrar o login
        return redirect(url_for("perfil", id_usuario=usuario.id))
    
    return render_template("criarconta.html", form=formCadastro)
# ====== /Cadastro ======



# ====== Pefil ======
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"]) # <usuario> significa que agora é uma variável
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # usuario está olhando seu proprio perfil
        form_foto = FormFotos()
        if form_foto.validate_on_submit():
            arquivo = form_foto.fotos.data
            nome_seguro = secure_filename(arquivo.filename)

            # salvar arquivo na pasta fotos_posts

            # 3 caminhos (caminho original do arquivo, caminho da pasta que vai ser salvo, arquivo que vai ser salvo)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"], nome_seguro)
            
            arquivo.save(caminho)

            # registrar esse arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)

            database.session.add(foto) # faz a conexão com o banco de dados, abrindo uma sessão
            database.session.commit() # faz o commit de todas as informações até agora no banco de dados

            # Redirecionar após o upload para evitar duplicação
            return redirect(url_for('perfil', id_usuario=id_usuario))
        
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)
# ====== /Login ======

# ====== Feed =======
@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)


# ====== /Feed =======

# ====== Logout ======
@app.route("/logout")
@login_required
def logout():
    logout_user() # ele ja sabe o current user(usuario atual) e desloga o mesmo
    return redirect(url_for("homepage"))
# ====== /Logout ======

