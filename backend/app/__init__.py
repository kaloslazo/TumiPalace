import sys
import re
from flask_cors import CORS
from flask_bcrypt import Bcrypt;
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
);
from flask import (
    Flask,
    request,
    jsonify,
    abort,
);
from .models import (
    db,
    setup_db,
    User,
);


def create_app(test_config=None):
    app = Flask(__name__);
    CORS(app, origins='*', supports_credentials=True);
    app.config['UPLOAD_FOLDER'] = 'static/employees';
    
    # jwt config
    app.config['JWT_SECRET_KEY'] = 'pass';
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    jwt = JWTManager(app);
    
    bcrypt = Bcrypt(app);
    with app.app_context():
        setup_db(app, test_config['database_qa'] if test_config else None)


    #===: Handle CORS ===:
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Max-Age', '15')
        return response


    #===: Handle current user ===:
    @app.route("/api/current_user", methods=["GET"])
    @jwt_required()
    def current_user_route():
        current_user_id = get_jwt_identity();
        
        if current_user_id is not None:
            current_user = User.query.get(current_user_id);
            return jsonify({
                "status": "authenticated",
                "user": {
                    "id": current_user.id,
                    "username": current_user.nickname,
                    "email": current_user.email,
                }
            });
        else: return jsonify({"status": "not authenticated"}), 401;


    #===: Handle register ===:
    @app.route("/api/register", methods=["POST"])
    def register():
        data = request.get_json();
        
        # handle errors for incomplete data
        if not data: return jsonify({"message": "No se proporcionó información."}), 400;
        username = data.get("username");
        password = data.get("password");
        email = data.get("email");
        
        if (not username): return jsonify({"message": "No se proporcionó nombre de usuario."}), 400;
        if (not password): return jsonify({"message": "No se proporcionó contraseña."}), 400;
        
        # validate data
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): return jsonify({"message": "El correo electrónico es inválido."}), 400;
        if len(password) < 5: return jsonify({"message": "La contraseña debe tener como mínimo 5 carácteres."}), 400;
        
        # check if user exists
        user = User.query.filter_by(nickname=username).first();
        if user: return jsonify({"message": "El usuario ya existe. Inténtelo de nuevo."}), 400;
        
        user = User.query.filter_by(email=email).first();
        if user: return jsonify({"message": "El correo electrónico está asociado con otra cuenta."}), 400;
        
        # encrypt password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8');
        new_user = User(nickname=username, password=hashed_password, email=email);
        db.session.add(new_user);
        db.session.commit();
        return jsonify(message="User created successfully"), 201;


    #===: Handle login ===:
    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json();
        
        # handle errors if no data provided
        if not data: return jsonify({"message": "No se proporcionó información"}), 400;
        username = data.get("username");
        password = data.get("password");
        
        if (not username): return jsonify({"message": "No se proporcionó nombre de usuario."}), 400;
        if (not password): return jsonify({"message": "No se proporcionó contraseña."}), 400;
        
        #check if user exits
        user = User.query.filter_by(nickname=username).first();
        if (not user): return jsonify({"message": "El usuario no existe."}), 404;  
    
        # check user pass & return access_token
        if user and bcrypt.check_password_hash(user.password, password): 
            access_token = create_access_token(identity=user.id);
            return jsonify({
                "message": "Logged successfully",
                "access_token": access_token,
                "user": {
                    "username": user.nickname,
                    "email": user.email,
                    "image": user.imageProfile,
                }}), 200;
        else:
            return jsonify({ "message": "La contraseña no es correcta. Inténtelo de nuevo." }), 401;


    #===: Handle example protected ===:
    @app.route('/protected', methods=['GET'])
    @jwt_required
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200;


    # return app as instance
    return app