from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from auth import auth_bp  # Importar el blueprint
from conexion import get_db

app = Flask(__name__)

app.secret_key = 'tu_secreto'  # Necesario para mensajes flash

# Registrar el blueprint antes de app.run()
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return render_template('Autenticacion/login.html')

@app.route('/about')
def about():
    return render_template('Sobre_Nosotros.html')

@app.route('/services')
def services():
    return render_template('Servicios.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/almacen')
def almacen():
    return render_template('Almacen/indexAlmacen.html')

@app.route('/login')
def login():
    return render_template('Autenticacion/login.html')
@app.route('/register')
def register():
    return render_template('Autenticacion/registro.html')

if __name__ == '__main__':
    app.run(debug=True)
