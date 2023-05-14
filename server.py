#===: Import section
import os
import uuid;
from datetime import datetime;

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
);
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    logout_user,
    current_user,
    login_user
);
from flask_sqlalchemy import SQLAlchemy;
from flask_bcrypt import Bcrypt;
from flask_migrate import Migrate;
from flask_wtf import FlaskForm;

from wtforms import (
    StringField, 
    IntegerField,
    PasswordField, 
    SubmitField,
);
from wtforms.validators import (
    InputRequired, 
    Length, 
    ValidationError,
    NumberRange
);
from wtforms.validators import (
    ValidationError,
);


#===: INITIAL SETUP :===
db = SQLAlchemy();
dbConfig = "postgresql://postgres@localhost:5432/dev_tumipalace_db";
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
);

SECRET_KEY = os.urandom(32);
app.config['SQLALCHEMY_DATABASE_URI'] = dbConfig;
app.config["TEMPLATES_AUTO_RELOAD"] = True;
app.config['SECRET_KEY'] = SECRET_KEY;
bcrypt = Bcrypt(app);

db.init_app(app);

login_manager = LoginManager();
login_manager.init_app(app)
login_manager.login_view = 'login' # returns for user login.

@login_manager.user_loader
def load_user(client_id):
    return Client.query.get(str(client_id))

#===: MODELS :===
class Client(db.Model, UserMixin):
    __tablename__ = 'client';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    age = db.Column(db.Integer, unique=False, nullable=False);
    nickname = db.Column(db.String(20), nullable=False, unique=True);
    email = db.Column(db.String(80), nullable=False, unique=True);
    password = db.Column(db.String(80), nullable=False, unique=False);
    bank = db.Column(db.Integer(), nullable=False, unique=False, default=0);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    imageProfile = db.Column(db.String(255), default=None);
    def __init__(self, age, nickname, email, password):
        self.age = age;
        self.nickname = nickname;
        self.email = email;
        self.password = password;
        self.bank = 0;
        self.imageProfile = None;
        self.creationDate = datetime.utcnow();
    def serialize(self):
        return {
            'id': self.id,
            'age': self.age,
            'nickname': self.nickname,
            'email': self.email,
            'password': self.password,
            'bank': self.bank,
            'imageProfile': self.imageProfile,
            'creationDate': self.creationDate,
        };

class Bet(db.Model):
    __tablename__ = 'bet';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    quantityDollar = db.Column(db.Integer(), nullable=False, unique=False);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    user_id = db.Column(db.String(36), db.ForeignKey('client.id'), nullable=False);
    def __init__(self, id, quantityDollar):
        self.id = id;
        self.quantityDollar = quantityDollar;
        self.creationDate = datetime.utcnow();
    def serialize(self):
        return {
            'id': self.id,
            'quantityDollar': self.quantityDollar,
            'creationDate': self.creationDate,
        };

class Game(db.Model):
    __tablename__ = 'games';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    name = db.Column(db.String(255), nullable=False);
    description = db.Column(db.Text, nullable=True);
    imageGame = db.Column(db.String(255), default=None);
    def __init__(self, id, name, description, imageGame):
        self.id = id;
        self.name = name;
        self.description = description;
        self.imageGame = imageGame;
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'imageGame': self.imageGame,
        };

class Deposit(db.Model):
    __tablename__ = 'deposit';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    quantityDollar = db.Column(db.Integer(), nullable=False, unique=False);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    user_id = db.Column(db.String(36), db.ForeignKey('client.id'), nullable=False);
    def __init__(self, id, quantityDollar):
        self.id = id;
        self.quantityDollar = quantityDollar;
        self.creationDate = datetime.utcnow();
    def serialize(self):
        return {
            'id': self.id,
            'quantityDollar': self.quantityDollar,
            'creationDate': self.creationDate,
        };

class LoginForm(FlaskForm):
    userNickname = StringField(validators=[InputRequired(message='El nombre de usuario no existe.'), Length(min=1, max=20)], render_kw={"placeholder": "@Nickname"});
    userPass = PasswordField(validators=[InputRequired(message='La contraseña es incorrecta.'), Length(min=5, max=80)], render_kw={"placeholder": "Contraseña"});
    submit = SubmitField("Iniciar sesión");
    def checkDatabaseRepetition(self, userNickname, userPass):
        user = Client.query.filter_by(nickname=userNickname).first();
        if user is None:
            raise ValidationError("El usuario ingresado no existe.");
        if not bcrypt.check_password_hash(user.password, userPass):
            raise ValidationError("La contraseña no es correcta, inténtelo de nuevo.");
    
class RegisterForm(FlaskForm):
    userAge = IntegerField(validators=[
        InputRequired(message='La edad es requerida.'),
        NumberRange(min=1, message="La edad debe ser un número mayor a 1.")],
        render_kw={"placeholder": "Edad"}
    );
    userNickname = StringField(validators=[InputRequired(message='El nombre de usuario es requerido.'), Length(min=1, max=20)], render_kw={"placeholder": "@Nickname"});
    userEmail = StringField(validators=[InputRequired(message='El correo electrónico es requerido.'), Length(min=1, max=80)], render_kw={"placeholder": "Email"});
    userPass = PasswordField(validators=[InputRequired(message='La contraseña es requerida.'), Length(min=1, max=80)], render_kw={"placeholder": "Contraseña"});
    submit = SubmitField("Registrarse");
    def checkDatabaseRepetition(self, userAge, userNickname, userEmail):
        nicknameExists = Client.query.filter_by(nickname=userNickname).first();
        userEmailExists = Client.query.filter_by(email=userEmail).first();
        if userAge < 18:
            raise ValidationError("Lo lamentamos, para poder crear una cuenta debes ser mayor de edad.");
        if nicknameExists:
            raise ValidationError("El nickname ya existe. Inténtalo de nuevo con uno distinto.");
        if userEmailExists:
            raise ValidationError("El correo ya se encuentra asociado a otra cuenta. Inténtalo de nuevo con uno distinto.");


#===: ROUTES :===
@app.route('/')
def index():
    return render_template('index.html');

@app.route('/home')
@login_required
def home():
    return render_template('views/home.html');

@app.route('/config')
def config():
    return "Config";

@app.route('/roulette')
def roulette():
    return "Roulette";

@app.route('/slots')
def slots():
    return "Slots";

@app.route('/rewards')
def rewards():
    return "Slots";

@app.route('/support')
def support():
    return "support";

@app.route('/logout')
def logout():
    return "Logout";

@app.route('/delete/<string:id>')
def deleteUser():
    return "Delete user";

#===: Auth modules
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        try:
            user = Client.query.filter_by(nickname=form.userNickname.data).first();
            form.checkDatabaseRepetition(form.userNickname.data, form.userPass.data);
            # if data passed validation
            login_user(user);
            return redirect(url_for('home'));
        except ValidationError as e:
            form.userNickname.errors.append(str(e));
    return render_template('auth/login.html', form=form);

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm();
    if form.validate_on_submit():
        try:
            form.checkDatabaseRepetition(form.userAge.data, form.userNickname.data, form.userEmail.data);
            # if data passed validators
            hashedPass = bcrypt.generate_password_hash(form.userPass.data).decode('utf-8');
            newUser = Client(
                nickname=form.userNickname.data, 
                password=hashedPass, 
                age=form.userAge.data, 
                email=form.userEmail.data
            );
            print(f"Client ('{newUser.nickname}', '{newUser.email}', '{newUser.age}', '{newUser.password}')");
            db.session.add(newUser);
            db.session.commit();
            db.session.close();
            return redirect(url_for('login'));
        except ValidationError as e:
            form.userAge.errors.append(str(e));
    return render_template('auth/register.html', form=form);


#===: Deploy :===
if __name__ == "__main__":
    # check if db exists & commit changes.
    with app.app_context():
        db.create_all();
    app.run(debug=True, port=8080);