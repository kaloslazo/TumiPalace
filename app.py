# ===: Import section
import uuid;
from decouple import config;
from flask import(
    Flask,
    render_template,
    url_for,
    redirect
);
from flask_sqlalchemy import SQLAlchemy;
from flask_migrate import Migrate;

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user;
from flask_wtf import FlaskForm;
from wtforms import StringField, PasswordField, SubmitField;
from wtforms.validators import InputRequired, Length, ValidationError;
from flask_bcrypt import Bcrypt;



# ===: General config
app = Flask(__name__); # app.py works as flask instance.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/tumipalace_db'; # local database.
app.config['SECRET_KEY'] = config('APP_SECRET_KEY'); # key saved at .env variables.
bcrypt = Bcrypt(app);
db = SQLAlchemy(app);



# ===: Utils
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # returns for user login.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))



# ===: Tables
class User(db.Model, UserMixin): # uses abstract UserMixin class.
    __tablename__ = 'users';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True); # unique uuid code.
    username = db.Column(db.String(20), nullable=False, unique=True);
    userpass = db.Column(db.String(80), nullable=False, unique=False);

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"});
    userpass = PasswordField(validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"});
    submit = SubmitField("Login");

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"});
    userpass = PasswordField(validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"});
    submit = SubmitField("Register");
    def check_username(self, username):
        usernameExists = User.query.filter_by(username=username.data).first();
        if usernameExists:
            raise ValidationError("Username already exists. Choose different one.");



# ===: Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html');

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first();
        if user:
            if bcrypt.check_password_hash(user.userpass, form.userpass.data):
                login_user(user);
                return redirect(url_for('home'));
    return render_template('login.html', form=form);

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm();
    if form.validate_on_submit():
        hashedPass = bcrypt.generate_password_hash(form.userpass.data).decode('utf-8');
        newUser = User(username=form.username.data, userpass=hashedPass);
        print(newUser);
        db.session.add(newUser);
        db.session.commit();
        db.session.close();
        return redirect(url_for('login'));
    return render_template('register.html', form=form);

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html');

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user();
    return redirect(url_for('login'));


# ===: Main flow
if __name__ == "__main__":
    # check if db exists & commit changes.
    with app.app_context():
        db.create_all();
    app.run(debug=True, port=8080);
else:
    print('Importing {}'.format(__name__))

# ===: Tables
class User(db.Model, UserMixin): # uses abstract UserMixin class.
    __tablename__ = 'users';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True); # unique uuid code.
    username = db.Column(db.String(20), nullable=False, unique=True);
    userpass = db.Column(db.String(80), nullable=False, unique=False);

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"});
    userpass = PasswordField(validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"});
    submit = SubmitField("Login");

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"});
    userpass = PasswordField(validators=[InputRequired(), Length(min=5, max=80)], render_kw={"placeholder": "Password"});
    submit = SubmitField("Register");
    def check_username(self, username):
        usernameExists = User.query.filter_by(username=username.data).first();
        if usernameExists:
            raise ValidationError("Username already exists. Choose different one.");



# ===: Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html');

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first();
        if user:
            if bcrypt.check_password_hash(user.userpass, form.userpass.data):
                login_user(user);
                return redirect(url_for('home'));
    return render_template('login.html', form=form);

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm();
    if form.validate_on_submit():
        hashedPass = bcrypt.generate_password_hash(form.userpass.data).decode('utf-8');
        newUser = User(username=form.username.data, userpass=hashedPass);
        print(newUser);
        db.session.add(newUser);
        db.session.commit();
        db.session.close();
        return redirect(url_for('login'));
    return render_template('register.html', form=form);

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html');



# ===: Main flow
if __name__ == "__main__":
    # check if db exists & commit changes.
    with app.app_context():
        db.create_all();
    app.run(debug=True, port=8080);
else:
    print('Importing {}'.format(__name__))