import os;
import shutil
import stripe;
import re;
import json;
from random import randint;
from dotenv import load_dotenv;
from PIL import Image;
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
    send_file,
);
from .models import (
    db,
    setup_db,
    User,
    Game,
    Transaction,
    RouletteBet
);


def create_app(test_config=None):
    load_dotenv();
    app = Flask(__name__, static_folder='static');
    CORS(app, origins='*', supports_credentials=True);
    
    # jwt config
    app.config['JWT_SECRET_KEY'] = 'pass';
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    jwt = JWTManager(app);
    
    # stripe config
    stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')
    stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY');
    
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
                    "imageProfile": current_user.imageProfile,
                    "bank": current_user.bank,
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
        new_user = User(nickname=username, password=hashed_password, email=email, bank=1000);
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
                    "bank": user.bank,
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
            print(token);
            send_reset_email(user, token);
            return jsonify(message="Petición enviada correctamente. Revisa el código de confirmación que enviamos a tu correo electrónico."), 200;
        else:
            return jsonify(message="El correo electrónico ingresado no existe."), 400;       
     
    def send_reset_email(user, token):
        msg = Message(
                'Restablecer contraseña | TumiPalace',
                sender='tumipalace@gmail.com',
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
    @app.route("/api/users/<user_id>", methods=["PUT", "GET"])
    @jwt_required()
    def update_user(user_id):
        user = User.query.get(user_id);
        if not user: return jsonify({"message": "El usuario no fue encontrado."}), 404

        if 'username' in request.form:
            new_username = request.form['username']
            
            if " " in new_username: return jsonify({"message": "El nombre de usuario no puede contener espacios."}), 400
            if (new_username == user.nickname): return jsonify({"message": "El nombre de usuario debe ser distinto al actual."}), 400
            if (User.query.filter_by(nickname=new_username).first()): return jsonify({"message": "El nombre de usuario ya se encuentra asociado a otra cuenta."}), 400
            user.nickname = new_username if new_username else user.nickname

        if 'email' in request.form:
            new_email = request.form['email']
            if (new_email == user.email): return jsonify({"message": "El correo electrónico debe ser distinto al actual."}), 400
            if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email): return jsonify({"message": "El correo electrónico es inválido."}), 400;
            if (User.query.filter_by(email=new_email).first()): return jsonify({"message": "El correo electrónico ya se encuentra asociado a otra cuenta."}), 400
            user.email = new_email if new_email else user.email

        if 'imageProfile' in request.files:
            new_image = request.files['imageProfile']
            
            user_dir = os.path.join(app.config["UPLOAD_FOLDER"], user_id) 
            if not os.path.exists(user_dir): os.makedirs(user_dir);
            
            filename = secure_filename(new_image.filename);
            current_image_path = user.imageProfile;
            
            if current_image_path and os.path.isfile(current_image_path): os.remove(current_image_path)
                        
            # convertir a png y guardar
            img = Image.open(new_image)
            user_image_path = os.path.join(user_dir, filename)
            img.convert('RGBA').save(user_image_path, "PNG")
            
            user.imageProfile = user_image_path;

        db.session.commit()

        return jsonify(user.serialize()), 200

    #===: Handle static image ===:
    @app.route("/api/<path:path>")
    def serve_file(path):
        absolute_path = os.path.join(os.getcwd(), path)
        if path.endswith(".png"):
            return send_file(absolute_path, mimetype='image/png')
        if path.endswith(".jpg"):
            return send_file(absolute_path, mimetype='image/jpg')
        elif path.endswith(".mp3"):
            return send_file(absolute_path, mimetype='audio/mpeg')
        else:
            return "File type not supported", 400

    #===: Handle delete account ===:
    @app.route("/api/users/<user_id>", methods=["DELETE"])
    @jwt_required()
    def delete_user(user_id):
        user = User.query.get(user_id);
        if not user: return jsonify({"message": "El usuario no fue encontrado."}), 404

        # verificar contraseña
        data = request.get_json();
        password = data.get("password");
        
        if not bcrypt.check_password_hash(user.password, password): return jsonify(message="La contraseña es incorrecta."), 401;

        # eliminar media del usuario
        user_folder = os.path.join(app.static_folder, 'user', user_id)
        if os.path.exists(user_folder): shutil.rmtree(user_folder)

        db.session.delete(user);
        db.session.commit();

        return jsonify({"message": "El usuario fue eliminado exitosamente. Redirigiéndote al inicio en 3 segundos..."}), 200

    #===: Handle change password ===:
    @app.route("/api/users/<user_id>/change_password", methods=["POST"])
    @jwt_required()
    def change_password(user_id):
        user = User.query.get(user_id)
        if not user: return jsonify({"message": "El usuario no fue encontrado."}), 404

        data = request.get_json();
        password = data.get("password");
        new_password = data.get("new_password");
        
        if (not password): return jsonify({"message": "No se proporcionó contraseña actual."}), 400;
        if not bcrypt.check_password_hash(user.password, password): return jsonify({"message": "Contraseña actual incorrecta."}), 401
        if bcrypt.check_password_hash(user.password, new_password): return jsonify({"message": "La nueva contraseña debe ser diferente de la actual."}), 400

        if (not new_password): return jsonify({"message": "No se proporcionó nueva contraseña."}), 400;
        if len(new_password) < 5: return jsonify({"message": "La contraseña debe tener como mínimo 5 carácteres."}), 400;
        if " " in new_password: return jsonify({"message": "La contraseña no puede contener espacios."}), 400;
        
        # Cambiar la contraseña
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8');
        user.password = hashed_password;
        db.session.commit()

        return jsonify({"message": "La contraseña ha sido cambiada exitosamente."}), 200

    #===: Handle games ===:
    @app.route("/api/games", methods=["GET"])
    def get_games():
        games = Game.query.all()
        return jsonify([game.serialize() for game in games])

    #===: Update user bank :===
    @app.route('/api/users/<user_id>/update_balance', methods=['POST'])
    @jwt_required()
    def update_balance(user_id):
        data = request.get_json()
        new_balance = data.get('balance')

        user = User.query.get(user_id)
        if not user: return jsonify({"message": "Usuario no encontrado"}), 404
        if not new_balance: return jsonify({"message": "No se proporcionó un nuevo balance"}), 400
        if new_balance < 0: return jsonify({"message": "El balance no puede ser negativo"}), 400

        user.bank = new_balance;
        db.session.commit();
        return jsonify({"message": "Balance actualizado exitosamente"}), 200

    #===: Handle transactions ===:
    @app.route('/api/add_funds', methods=['POST'])
    @jwt_required()
    def add_funds():
        try:
            user_id = get_jwt_identity();
            amount = request.json.get('amount')

            if not user_id: return jsonify({"message": "Usuario no encontrado."}), 404
            if not amount: return jsonify({"message": "No se proporcionó una cantidad."}), 400
            if amount <= 0: return jsonify({"message": "La cantidad no puede ser igual o menor que 0."}), 400
            if not isinstance(amount, (int, float)) or amount < 0.50: return jsonify({'error': 'La cantidad debe ser un número mayor o igual a 0.50'}), 400

            # intencion de pago
            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency='pen',
                description='Abono de tokens | TumiPalace',
                metadata={'user_id': user_id}
            );
            return jsonify({'clientSecret': intent['client_secret']})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 403

    @app.route('/webhook', methods=['POST'])
    def stripe_webhook():
        payload = request.data
        sig_header = request.headers.get('STRIPE_SIGNATURE')
        print(sig_header);

        try:
            event = stripe.Webhook.construct_event( payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET'))
            print(os.getenv('STRIPE_WEBHOOK_SECRET'));
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except stripe.error.SignatureVerificationError as e:
            return jsonify({'error': str(e)}), 400

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
            user_id = payment_intent['metadata']['user_id']
            amount = payment_intent['amount']
            
            print('\n\nPaymentIntent was successful! del id:', user_id);
            
            try:
                user = User.query.get(user_id)
                if user:
                    user.bank = user.bank + amount
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            print('No se hizo el pago.')

        return '', 200

    #===: Roulette Logic ===:
    @app.route('/api/roulette/bet', methods=['POST'])
    @jwt_required()
    def place_bet():
        user_id = get_jwt_identity();
        user = User.query.get(user_id);
        if not user: return jsonify({'error': 'El usuario no fue encontrado.'}), 404;
        
        bet_data = request.json.get('bet_data');
        total_bet_amount = sum(bet['amount'] for bet in bet_data);
        if total_bet_amount > user.bank: return jsonify({'error': 'Los fondos son insuficientes.'}), 400;
        
        bet = RouletteBet(user_id=user_id, bet_data=json.dumps(bet_data));
        user.bank = user.bank - total_bet_amount;
        
        db.session.add(bet)
        db.session.commit()
        return jsonify(bet.serialize()), 201

    @app.route('/api/roulette/result', methods=['GET'])
    @jwt_required()
    def get_result():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado.'}), 404
        
        bet_id = request.args.get('bet_id')
        bet = RouletteBet.query.get(bet_id)
        if not bet:
            return jsonify({'error': 'Apuesta no válida.'}), 404
        
        roulette_number = randint(0, 36)
        roulette_color = 'red' if roulette_number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else 'black'
        bet_data = json.loads(bet.bet_data)
        
        for bet_entry in bet_data:
            if (bet_entry['type'] == 'number' and bet_entry['value'] == roulette_number) or (bet_entry['type'] == 'color' and bet_entry['value'] == roulette_color):
                bet_entry['result'] = 'win'
                user.bank += bet_entry['amount'] * 2
            else:
                bet_entry['result'] = 'lose'
        
        bet.result = 'win' if any(entry['result'] == 'win' for entry in bet_data) else 'lose'
        result_data = {
            'numbers': roulette_number,
            'color': roulette_color,
            'bet_data': bet_data
        }

        db.session.commit()
        
        return jsonify(result_data), 200



    # return app as instance
    return app