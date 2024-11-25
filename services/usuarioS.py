from flask import jsonify
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

        if user and user.password == password:
            print("Contraseña válida")
            return jsonify({"valid": True, "user_id": user.id, "saldo": user.saldo}), 200
        else:
            print(f"Contraseña almacenada: {user.password}")
            print("Contraseña inválida")
        return jsonify({"valid": False, "error": "Credenciales inválidas"}), 404
    except Exception as e:
        print(f"Error en verify_user: {e}")
        return jsonify({"valid": False, "error": "Error interno en el servidor"}), 500
