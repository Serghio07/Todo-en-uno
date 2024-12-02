
from flask import Flask, render_template,session, request, redirect, url_for, flash, send_from_directory

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import db
from models.usuarios import Usuario  # Importa la instancia y modelos
from models.pagos import Pago
from auth import auth_bp
from admin import admin_bp
from user import user_bp
from almacen import almacen_bp  
from impresion import impresion_bp
from almacen import almacen_bp
from impresion import impresion_bp  
import logging
import werkzeug
import mimetypes
import os
mimetypes.add_type('application/javascript', '.mjs')
logging.basicConfig(level=logging.DEBUG)


# Registrar el blueprint en la aplicación principal


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
app.secret_key = 'tu_secreto'
db.init_app(app)

with app.app_context():
    db.create_all()  # Crea las tablas si no existen

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(almacen_bp, url_prefix='/almacen')
app.register_blueprint(impresion_bp, url_prefix='/impresion')
app.register_blueprint(impresion_bp, url_prefix='/impresion')


@app.before_request
def set_default_role():
    if 'role' not in session:
        session['role'] = 'Sin Registro'
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('Autenticacion/login.html')

@app.route('/register')
def register():
    return render_template('Autenticacion/registro.html')

@app.route('/plantillas')
def plantillas():
    return render_template('Documentos/indexdoc.html')

@app.route('/pagos/pago')
def pago():
    return render_template('Pagos/pago.html')  # Ruta relativa dentro de 'templates'

@app.route('/impresion')
def impresion():
    return render_template('impresion/impresion.html')

from flask import request, render_template
import urllib.parse

@app.route('/editor')
def editor():
    file_path = request.args.get('file')

    # Decodificar la ruta para asegurarnos que los caracteres especiales son manejados correctamente
    file_path = urllib.parse.unquote(file_path)

    # Aquí debería ir el código para mostrar el archivo PDF usando PDF.js o lo que necesites
    return render_template('Documentos/editor.html', file_path=file_path)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)
