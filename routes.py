#===: Import section
from flask import (
    Flask,
    render_template,
    request,
    redirect
);
from server import app;


#===: Views
@app.route('/')
def index():
    return render_template('index.html');

@app.route('/login')
def login():
    return "Login";

@app.route('/register')
def register():
    return "Register";

@app.route('/home')
def home():
    return "Home";

@app.route('/config')
def config():
    return "Config";

@app.route('/roulette')
def roulette():
    return "Roulette";

@app.route('/slots')
def slots():
    return "Slots";

@app.route('/logout')
def logout():
    return "Logout";

@app.route('/delete/<string:id>')
def deleteUser():
    return "Delete user";