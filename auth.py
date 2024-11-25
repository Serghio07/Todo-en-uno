from flask import Blueprint, request, session, redirect, url_for, flash, render_template, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from sqlalchemy.orm import Session
from models import Usuario  # Tu modelo de usuario
from conexion import get_db  # Importa la función para conectar a la BD

# Crear el Blueprint
auth_bp = Blueprint('auth_bp', __name__)

# Clave secreta para firmar los tokens (usa una más robusta en producción y mantenla segura)
SECRET_KEY = "tu_clave_secreta_segura"

# Ruta de inicio de sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    # Obtener los datos enviados en el formulario o JSON
    email = request.json.get('email') if request.is_json else request.form.get('email')
    password = request.json.get('password') if request.is_json else request.form.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    # Conectar a la base de datos
    db_session = next(get_db())

    try:
        # Buscar el usuario por email
        usuario = db_session.query(Usuario).filter_by(email=email).first()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar la contraseña usando hashing
        if not check_password_hash(usuario.password, password):
            return jsonify({"error": "Contraseña incorrecta"}), 401

        # Generar el token JWT
        token = jwt.encode({
            "user_id": usuario.id,
            "email": usuario.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Token expira en 2 horas
        }, SECRET_KEY, algorithm="HS256")

        # Si todo está bien
        return jsonify({
            "message": "Inicio de sesión exitoso",
            "token": token,
            "user": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

    finally:
        db_session.close()

# Ruta de registro
@auth_bp.route('/registro', methods=['POST'])
def register():
    try:
        print("Datos recibidos en /registro:", request.json)
        data = request.json
        email = data.get('email')
        password = data.get('password')  # Contraseña enviada desde el frontend
        nombre = data.get('nombre')
        rol = data.get('rol', 'user')

        if not email or not password or not nombre:
            return jsonify({"error": "Email, contraseña y nombre son requeridos"}), 400

        db_session = next(get_db())

        # Verificar si el usuario ya existe
        usuario_existente = db_session.query(Usuario).filter_by(email=email).first()
        if usuario_existente:
            return jsonify({"error": "El usuario ya existe"}), 409

        # Hashear la contraseña y asignarla al campo correcto
        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuario(email=email, hashed_password=hashed_password, nombre=nombre, rol=rol)  # Ajuste aquí
        db_session.add(nuevo_usuario)
        db_session.commit()

        return jsonify({
            "message": "Registro exitoso",
            "user": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email,
                "rol": nuevo_usuario.rol
            }
        }), 201

    except Exception as e:
        print(f"Error en /registro: {e}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

    finally:
        db_session.close()




# Ruta para manejar el cierre de sesión
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    session.pop('role', None)
    session.pop('name', None)
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('auth_bp.login'))
