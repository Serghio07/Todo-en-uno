from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from auth import auth_bp  # Importar el blueprint
from conexion import get_db
from flask import Flask, render_template, request, jsonify
from models.pagos import db
from services.usuarioS import verify_user
from services.pagoS import process_payment

app = Flask(__name__)

app.secret_key = 'tu_secreto'  # Necesario para mensajes flash

# Registrar el blueprint antes de app.run()
app.register_blueprint(auth_bp, url_prefix='/auth')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db.init_app(app)

@app.route('/')
def home():
    return render_template('Autenticacion/login.html')
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('team.html')

@app.route('/Sobre_Nosotros')
def about():
    return render_template('Sobre_Nosotros.html')

@app.route('/Servicios')
def services():
    return render_template('Servicios.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/verify_user', methods=['POST'])
def verify_user_route():
    data = request.json
    return verify_user(data)

@app.route('/process_payment', methods=['POST'])
def process_payment_route():
    data = request.json
    return process_payment(data)

@app.route('/login')
def login():
    return render_template('Autenticacion/login.html')
@app.route('/register')
def register():
    return render_template('Autenticacion/registro.html')

if __name__ == '__main__':
    app.run(debug=True)
