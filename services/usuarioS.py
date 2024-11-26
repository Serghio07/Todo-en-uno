from flask import jsonify
from werkzeug.security import check_password_hash
from models.usuarios import Usuario
from models import db

def verify_user(data):
    try:
        email = data.get('email')
        password = data.get('password')
        print(f"Email recibido: {email}")
        print(f"Password recibido: {password}")

        if not email or not password:
            return jsonify({"valid": False, "error": "Faltan campos obligatorios"}), 400

        user = Usuario.query.filter_by(email=email).first()
        if user:
            print(f"Usuario encontrado: {user.email}")
        else:
            print("Usuario no encontrado")
            return jsonify({"valid": False, "error": "Usuario no encontrado"}), 404

        # Verificar la contraseña usando hashing
        if check_password_hash(user.hashed_password, password):
            print("Contraseña válida")
            return jsonify({"valid": True, "user_id": user.id, "saldo": user.saldo}), 200
        else:
            print("Contraseña inválida")
            return jsonify({"valid": False, "error": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"Error en verify_user: {e}")
        return jsonify({"valid": False, "error": "Error interno en el servidor"}), 500
