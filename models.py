#===: Importing modules :===
import uuid;
from datetime import datetime;
from flask_sqlalchemy import SQLAlchemy;
from flask_migrate import Migrate;


#===: Importing section :==
from routes import *;
from server import db;


#===: Model User
class Users(db.Model):
    __tablename__ = 'users';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    firstname = db.Column(db.String(20), nullable=False, unique=False);
    lastname = db.Column(db.String(20), nullable=False, unique=False);
    age = db.Column(db.Integer, unique=False, nullable=False);
    nickname = db.Column(db.String(20), nullable=False, unique=True);
    email = db.Column(db.String(80), nullable=False, unique=True);
    password = db.Column(db.Integer(255), nullable=False, unique=False);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    imageProfile = db.Column(db.String(255), default=None);
    def __init__(self, firstname, lastname, age, nickname, email, password):
        self.firstname = firstname;
        self.lastname = lastname;
        self.age = age;
        self.nickname = nickname;
        self.email = email;
        self.password = password;
        self.imageProfile = None;
        self.creationDate = datetime.utcnow();
    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'nickname': self.nickname,
            'email': self.email,
            'password': self.password,
            'imageProfile': self.imageProfile,
            'creationDate': self.creationDate,
        };

class Bet(db.Model):
    __tablename__ = 'bet';
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"), unique=True);
    quantityDollar = db.Column(db.Integer(), nullable=False, unique=False);
    creationDate = db.Column(db.DateTime, default=datetime.utcnow());
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False);
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
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False);
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