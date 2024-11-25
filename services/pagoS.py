from flask import jsonify
from models import db  # Asegúrate de que este sea el mismo db que inicializaste en app.py
from models.usuarios import Usuario
from models.pagos import Pago

def process_payment(data):
    try:
        # Obtener los datos del cliente
        user_id = data.get('user_id')
        payment_amount = data.get('amount')  # Usar un nombre claro para el monto del pago
        metodo = data.get('metodo', 'tarjeta')

        # Validación de los datos obligatorios
        if not user_id or not payment_amount:
            return jsonify({"success": False, "error": "Faltan campos obligatorios"}), 400

        # Buscar el usuario en la base de datos
        user = Usuario.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "Usuario no encontrado"}), 404

        print(f"Usuario encontrado: {user.email}, Saldo actual: {user.saldo}")

        # Verificar que el usuario tenga suficiente saldo
        if user.saldo < float(payment_amount):
            return jsonify({"success": False, "error": "Saldo insuficiente"}), 400

        # Registrar el pago en la base de datos
        pago = Pago(usuario_id=user_id, monto=float(payment_amount), metodo=metodo)
        db.session.add(pago)
        user.saldo -= float(payment_amount)
        db.session.commit()

        print(f"Pago registrado exitosamente. Nuevo saldo: {user.saldo}")
        return jsonify({"success": True}), 200

    except Exception as e:
        # Manejo de errores internos
        print(f"Error interno en process_payment: {str(e)}")
        return jsonify({"success": False, "error": f"Error interno: {str(e)}"}), 500
