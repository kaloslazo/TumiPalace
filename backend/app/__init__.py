import sys;
import os;
import re;
from flask_cors import CORS
from flask_bcrypt import Bcrypt;
from werkzeug.utils import secure_filename;
from flask_mail import (
    Mail,
    Message,
);
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
    url_for,
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
    
    # mail config
    app.config["MAIL_SERVER"] = "smtp.gmail.com";
    app.config["MAIL_PORT"] = 587;
    app.config["MAIL_USE_TLS"] = True;
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME');
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD');
    mail = Mail(app);
    
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
                    "id": user.id,
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
    
    #===: Handle forgot password ===:
    @app.route("/api/reset_password", methods=["POST"])
    def reset_password_request():
        data = request.get_json();
        email = data.get("email");
        user = User.query.filter_by(email=email).first();
        if user: 
            token = user.get_reset_password_token();
            send_reset_email(user, token);
            return jsonify(message="Petición enviada correctamente. Revisa el código de confirmación que enviamos a tu correo electrónico."), 200;
        else:
            return jsonify(message="El correo electrónico ingresado no existe."), 400;        
    def send_reset_email(user, token):
        msg = Message(
                'Restablecer contraseña | TumiPalace',
                sender='noreply@tumipalace.com',
                recipients=[user.email]);
        msg.html = f'''
        <h1>Restablecimiento de contraseña</h1>
        <p>Hola,</p>
        <p>Recibimos una solicitud para restablecer tu contraseña. Si tú hiciste esta solicitud, haz clic en el siguiente enlace para restablecer tu contraseña:</p>
        <p><a target="_BLANK" href="http://127.0.0.1:8080/reset_password/{token}">Cambiar contraseña</a></p>
        <p>El token expira en 10 minutos. Si tú no realizaste la solicitud de cambio de contraseña, ignora este correo electrónico.</p>
        <p>Saludos,</p>
        <p>El equipo de TumiPalace Perú.</p>
        '''
        mail.send(msg);

    #===: Handle password reset as email link ===:
    @app.route("/api/reset_password/<token>", methods=["POST"])
    def reset_password(token):
        user = User.verify_reset_password_token(token);
        if not user: return jsonify(message="El token es inválido o ya expiró."), 400
        
        data = request.get_json();
        password = data.get("password");
        
        # si la contraseña es la misma que la anterior no se actualiza
        if bcrypt.check_password_hash(user.password, password): return jsonify(message="La contraseña es la misma que la anterior."), 400;
        
        # encrypt password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8');
        user.password = hashed_password;
        user.reset_password_token = None
        user.reset_password_token_expires_at = None
        db.session.commit();
        return jsonify(message="La contraseña se actualizó exitosamente."), 200;

    #===: Handle update account ===:
    @app.route("/api/users/<user_id>", methods=["PUT"])
    def update_user(user_id):
        user = User.query.get(user_id);
        if not user: return jsonify({"message": "El usuario no fue encontrado."}), 404

        data = request.get_json()
        new_nickname = data.get("nickname", user.nickname)
        new_email = data.get("email", user.email)

        if new_nickname and (new_nickname != user.nickname) and (User.query.filter_by(nickname=new_nickname).first()): return jsonify({"message": "El nickname está registrado en otra cuenta."}), 400
        if new_email and (new_email != user.email) and (User.query.filter_by(email=new_email).first()): return jsonify({"message": "Email already in use"}), 400

        user.nickname = new_nickname if new_nickname else user.nickname
        user.email = new_email if new_email else user.email

        # Handle the profile image
        image = request.files.get('imageProfile')
        
        if image:
            filename = secure_filename(image.filename);
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.imageProfile = url_for('uploaded_file', filename=filename)

        db.session.commit()

        return jsonify(user.serialize()), 200

    # return app as instance
    return app