from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Clave para JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)
from flask import request, jsonify
from conexion import get_db
from models import Usuario
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'tu_secreto'  # Necesario para mensajes flash

# Inicializar Firebase
cred = credentials.Certificate('path/to/your/firebase_credentials.json')
firebase_admin.initialize_app(cred)

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

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



if __name__ == '__main__':
    app.run(debug=True)
