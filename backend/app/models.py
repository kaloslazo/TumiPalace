import uuid;
from datetime import datetime, timedelta
from config.development import config;
from flask_sqlalchemy import SQLAlchemy;
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer;
from flask import current_app;


db = SQLAlchemy();


def setup_db(app, db_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URI"] if db_uri is None else db_uri;
    app.config["SECRET_KEY"] = "dev_secret_key";
    app.config["UPLOAD_FOLDER"] = "static/users";
    db.app = app;
    db.init_app(app);
    db.create_all();


#===: user class :===
class User(db.Model):
    __tablename__ = 'user_table';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    nickname = db.Column(db.String(20), nullable=False, unique=True);
    email = db.Column(db.String(80), nullable=False, unique=True);
    password = db.Column(db.String(80), nullable=False, unique=False);
    reset_password_token = db.Column(db.String(255), default=None);
    reset_password_token_expires_at = db.Column(db.DateTime , default=datetime.utcnow());
    bank = db.Column(db.Integer(), nullable=False, unique=False, default=0);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    imageProfile = db.Column(db.String(255), default=None);
    
    def __init__(self, nickname, email, password):
        self.nickname = nickname;
        self.email = email;
        self.password = password;
        self.reset_password_token = None;
        self.reset_password_token_expires_at = datetime.utcnow();
        self.bank = 0;
        self.imageProfile = None;
        self.creationDate = datetime.utcnow();
        
    def serialize(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'password': self.password,
            'bank': self.bank,
            'imageProfile': self.imageProfile,
            'creationDate': self.creationDate,
        };
        
    def get_reset_password_token(self, expires_sec=600):
        s = Serializer(str(current_app.config['SECRET_KEY']), expires_sec);
        token = s.dumps({'user_id': self.id}).decode('utf-8');
        
        self.reset_password_token = token;
        self.reset_password_token_expires_at = datetime.utcnow() + timedelta(seconds=expires_sec);
        db.session.commit();
        return token;
    
    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try: user_id = s.loads(token)['user_id']
        except: return None;
        
        user = User.query.get(user_id);
        if user is None or user.reset_password_token != token or user.reset_password_token_expires_at < datetime.utcnow(): return None;
        return user;


#===: games class :===
class Game(db.Model):
    __tablename__ = 'game_table';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    alias = db.Column(db.String(255), nullable=False);
    name = db.Column(db.String(255), nullable=False);
    description = db.Column(db.Text, nullable=True);
    imageGame = db.Column(db.String(255), default=None);
    def __init__(self, alias, name, description, imageGame):
        self.alias = alias;
        self.name = name;
        self.description = description;
        self.imageGame = imageGame;
    def serialize(self):
        return {
            'id': self.id,
            'alias': self.alias,
            'name': self.name,
            'description': self.description,
            'imageGame': self.imageGame,
        };


#===: transaction class :===
class Transaction(db.Model):
    __tablename__ = 'transaction_table';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    quantityDollar = db.Column(db.Integer(), nullable=False, unique=False);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    user_id = db.Column(db.String(36), db.ForeignKey('user_table.id'), nullable=False);
    def __init__(self, quantityDollar):
        self.quantityDollar = quantityDollar;
        self.creationDate = datetime.utcnow();
    def serialize(self):
        return {
            'id': self.id,
            'quantityDollar': self.quantityDollar,
            'creationDate': self.creationDate,
        };