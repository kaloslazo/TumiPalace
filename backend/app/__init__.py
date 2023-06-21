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
    Employee,
    Department,
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
        age = data.get("age");
        if (not username): return jsonify({"message": "No se proporcionó nombre de usuario."}), 400;
        if (not password): return jsonify({"message": "No se proporcionó contraseña."}), 400;
        
        # validate data
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): return jsonify({"message": "El correo electrónico es inválido."}), 400;
        if age < 18: return jsonify({"message": "El usuario debe ser mayor de edad."}), 400;
        if len(password) < 5: return jsonify({"message": "La contraseña debe tener como mínimo 5 carácteres."}), 400;
        
        # check if user exists
        user = User.query.filter_by(nickname=username).first();
        if user: return jsonify({"message": "El usuario ya existe. Inténtelo de nuevo."}), 400;
        
        user = User.query.filter_by(email=email).first();
        if user: return jsonify({"message": "El correo electrónico está asociado con otra cuenta."}), 400;
        
        # encrypt password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8');
        new_user = User(nickname=username, password=hashed_password, email=email, age=age);
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















    @app.route('/employees', methods=['POST'])
    def create_employee():
        error_code = 201
        list_errors = []
        try:
            body = request.json

            if 'first_name' not in body:
                list_errors.append('first_name is required')
            else:
                first_name = body.get('first_name')

            if 'last_name' not in body:
                list_errors.append('last_name is required')
            else:
                last_name = body.get('last_name')

            if 'job_title' not in body:
                list_errors.append('job_title is required')
            else:
                job_title = body.get('job_title')

            if 'selectDepartment' not in body:
                list_errors.append('selectDepartment is required')
            else:
                department_id = body.get('selectDepartment')


            if len(list_errors) > 0:
                error_code = 400
            else:
                employee = Employee(first_name, last_name, job_title, department_id)
                db.session.add(employee)
                db.session.commit()
                employeeid_created = employee.id
                
        except Exception as e:
            db.session.rollback()
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            error_code = 500

        if error_code == 400:
            return jsonify({'success': False, 
                            'message': 'Error creating employee', 
                            'errors': list_errors}), error_code
        elif error_code != 201:
            abort(error_code)
        else:
            return jsonify({'success': True, 
                            'id': str(employeeid_created), 
                            'message': 'Employee created successfully'
                            }), 201

    @app.route('/employees', methods=['GET'])
    def get_employees():
        error_code = 200
        try:
            search_query = request.args.get('query', None)
            if search_query:
                employees = Employee.query.filter_by(is_active=True).filter(Employee.first_name.ilike('%{}%'.format(search_query))).order_by(Employee.first_name).all()
            else:
                employees = Employee.query.filter_by(is_active=True).order_by(Employee.first_name).all()
            
        except Exception as e:
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
            error_code = 500
        
        if error_code != 200:
            abort(error_code)
        else:
            return jsonify({'success': True, 
                            'employees': [e.serialize() for e in employees], 
                            'total': len(employees)
                            }), 200



    @app.route('/employees/<id>', methods=['PATCH'])
    def update_employee(id):
        returned_code = 200
        try:
            employee = Employee.query.get(id)

            if not employee:
                returned_code = 404

            data = request.json

            if 'first_name' in data:
                employee.first_name = data['first_name']

            if 'last_name' in data:
                employee.last_name = data['last_name']

            if 'job_title' in data:
                employee.job_title = data['job_title']

            if 'selectDepartment' in data:
                employee.department_id = data['selectDepartment']

            db.session.commit()
            db.session.close()
            
        except Exception as e:
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()


        if returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({
                'success':True,
                'message': 'Empleado actualizado correctamente'
                }), 200

    @app.route('/employees/<id>', methods=['DELETE'])
    def delete_employee(id):
        returned_code = 200
        try:
            employee = Employee.query.get(id)

            if not employee:
                returned_code = 404
                abort(returned_code)

            employee.is_active = False
            db.session.commit()
            db.session.close()

        except Exception as e:
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
        
        if returned_code != 200:
            abort(returned_code)
        else:
            return jsonify({'success':True,
                            'message': 'Empleado eliminado correctamente'
                            }), returned_code


    @app.route('/departments', methods=['GET'])
    def get_departments():
        error_code = 200
        try:
            search_query = request.args.get('query', None)
            if search_query:
                departments = Department.query.filter(
                    db.or_(Department.name.ilike('%{}%'.format(search_query)),
                            Department.short_name.ilike('%{}%'.format(search_query)))    
                ).order_by(Department.short_name).all()
            else:
                departments = Department.query.order_by(Department.short_name).all()

        except Exception as e:
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
            error_code = 500
        
        if error_code != 200:
            abort(error_code)
        else:
            return jsonify({'success': True, 
                            'departments': [d.serialize() for d in departments],
                            'total': len(departments)
                            }), error_code
            
        
    @app.route('/departments', methods=['POST'])
    def create_department():
        error_code = 201
        list_errors = []
        try:
            body = request.json

            if 'name' not in body:
                list_errors.append('name is required')
            else:
                name = body.get('name')

            if 'short_name' not in body:
                list_errors.append('short_name is required')
            else:
                short_name = body.get('short_name')

            if len(list_errors) > 0:
                error_code = 400
            else:
                department = Department(name, short_name)
                db.session.add(department)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            error_code = 500


        if error_code == 400:
            return jsonify({
                'success': False, 
                'message': 'Error creating department', 'errors': list_errors
            }), error_code
        elif error_code != 201:
            abort(error_code)
        else:
            return jsonify({
                'success': True, 
                'id': department.id, 
                'name':department.name, 
                'short_name':department.short_name ,
                'message': 'Department created successfully'
                }), 201

    @app.route('/departments/<id>', methods=['PATCH'])
    def update_department(id):
        error_code = 200
        try:
            department = Department.query.get(id)

            if not department:
                error_code = 404
                abort(error_code)

            data = request.json

            if 'name' in data:
                department.name = data['name']
            if 'short_name' in data:
                department.short_name = data['short_name']
            db.session.commit()
            db.session.close()

        except Exception as e:
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
            error_code = 500

        if error_code != 200:
            abort(error_code)
        else:
            return jsonify({'success': True, 
                            'message': 'Departamento actualizado exitosamente'
                            }), error_code
    
    @app.route('/departments/<id>', methods=['DELETE'])
    def delete_department(id):
        error_code = 200
        try:
            department = Department.query.get(id)

            if not department:
                error_code = 404
                abort(error_code)

            db.session.delete(department)
            db.session.commit()
            db.session.close()
        except Exception as e:
            print("error: ", e)
            print("sys.exc_info(): ", sys.exc_info())
            db.session.rollback()
            error_code = 500

        if error_code != 200:
            abort(error_code)
        else:
            return jsonify({'success': True,'message': 'Departamento eliminado exitosamente'})


    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            'success': False, 
            'message': 'Internal Server Error'
        }), 500
    
    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({
            'success': False,
            'message': 'Not Found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowd(e):
        return jsonify({
            'success': False,
            'method': 'Method Not Allowed'
        }), 405
    


    return app