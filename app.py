
from flask import Flask, render_template, request, jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('service.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/almacen')
def almacen():
    return render_template('Almacen/indexAlmacen.html')

@app.route('/pagos')
def pagos():
    return render_template('Pagos/pago.html')
# Modelo para Usuario
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    saldo = db.Column(db.Float, default=0.0)
    rol = db.Column(db.String(20), nullable=False)

# Modelo para Pago
# Modelo para Pago
class Pago(db.Model):
    __tablename__ = 'pago'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, default=db.func.current_timestamp())
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    metodo = db.Column(db.String(20), nullable=False)  # Campo agregado


@app.route('/verify_user', methods=['POST'])
def verify_user():
    try:
        data = request.json
        if not data:
            return jsonify(error="No se enviaron datos"), 400

        email = data.get('email')
        password = data.get('password')  # Aún no validamos contraseñas en este ejemplo.

        if not email or not password:
            return jsonify(error="Faltan campos obligatorios (email o password)"), 400

        user = Usuario.query.filter_by(email=email).first()
        if user:
            return jsonify(valid=True, saldo=user.saldo, user_id=user.id)
        return jsonify(valid=False, error="Usuario no encontrado"), 404
    except Exception as e:
        print(f"Error en /verify_user: {e}")
        return jsonify(error="Error interno en el servidor"), 500

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        data = request.json
        if not data:
            return jsonify(success=False, error="No se enviaron datos"), 400

        user_id = data.get('user_id')
        amount = data.get('amount')
        metodo = data.get('metodo', 'efectivo')  # Valor predeterminado si no se envía

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

        print(f"Pago procesado exitosamente para el usuario {user.nombre}, Monto: {amount}, Método: {metodo}")
        return jsonify(success=True)
    except Exception as e:
        print(f"Error en /process_payment: {e}")
        return jsonify(success=False, error="Error interno en el servidor"), 500

@app.route('/result/<status>')
def result(status):
    message = "Pago realizado con éxito" if status == "success" else "Error en el pago"
    return render_template('Pagos/result.html', message=message)

if __name__ == '__main__':
    # Bloque de prueba para verificar conexión con la base de datos
    with app.app_context():
        user = Usuario.query.first()
        if user:
            print(f"Primer usuario: {user.nombre}, Email: {user.email}, Rol: {user.rol}, Saldo: {user.saldo}")
        else:
            print("No se encontraron usuarios en la base de datos.")

    app.run(debug=True)