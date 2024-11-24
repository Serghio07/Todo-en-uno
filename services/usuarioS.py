from flask import jsonify
from models.usuarios import Usuario
from models.pagos import db

def verify_user(data):
    try:
        email = data.get('email')
        password = data.get('password')  # Este es un ejemplo básico, no estamos validando contraseñas reales

        if not email or not password:
            return jsonify(error="Faltan campos obligatorios (email o password)"), 400

        user = Usuario.query.filter_by(email=email).first()
        if user:
            return jsonify(valid=True, saldo=user.saldo, user_id=user.id)
        return jsonify(valid=False, error="Usuario no encontrado"), 404
    except Exception as e:
        print(f"Error en verify_user: {e}")
        return jsonify(error="Error interno en el servidor"), 500
