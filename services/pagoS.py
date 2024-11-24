from flask import jsonify
from models.pagos import Pago, db
from models.usuarios import Usuario

def process_payment(data):
    try:
        user_id = data.get('user_id')
        amount = data.get('amount')
        metodo = data.get('metodo', 'efectivo')

        if not user_id or not amount:
            return jsonify(success=False, error="Faltan campos obligatorios"), 400

        amount = float(amount)
        user = db.session.get(Usuario, user_id)

        if not user:
            return jsonify(success=False, error="Usuario no encontrado"), 404

        if user.saldo < amount:
            return jsonify(success=False, error="Saldo insuficiente"), 400

        # Procesa el pago
        user.saldo -= amount
        nuevo_pago = Pago(monto=amount, usuario_id=user.id, metodo=metodo)
        db.session.add(nuevo_pago)
        db.session.commit()

        return jsonify(success=True)
    except Exception as e:
        print(f"Error en process_payment: {e}")
        return jsonify(success=False, error="Error interno en el servidor"), 500
