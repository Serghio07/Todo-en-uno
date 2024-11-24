from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt

# Inicializar aplicaciones
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Cambia esto según tu configuración de base de datos
app.config['JWT_SECRET_KEY'] = 'mi_clave_secreta'  # Cambia esta clave por una más segura
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    # Obtener datos del cuerpo de la solicitud
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Email y contraseña son requeridos"}), 400

    # Buscar al usuario en la base de datos
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario is None:
        return jsonify({"msg": "Correo electrónico o contraseña incorrectos"}), 401
    
    # Verificar la contraseña
    if not bcrypt.check_password_hash(usuario.password, password):
        return jsonify({"msg": "Correo electrónico o contraseña incorrectos"}), 401

    # Generar el token JWT
    access_token = create_access_token(identity={'id': usuario.id, 'email': usuario.email})
    
    return jsonify({
        'msg': 'Inicio de sesión exitoso',
        'access_token': access_token,
        'usuario': {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'rol': usuario.rol
        }
    })

# Inicializar la base de datos (solo para este ejemplo)
@app.before_first_request
def create_tables():
    db.create_all()

