from flask import Flask, session, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import db
from models.usuarios import Usuario  # Importa la instancia y modelos
from models.pagos import Pago
from auth import auth_bp
from admin import admin_bp
from user import user_bp
from almacen import almacen_bp  
import logging
import werkzeug
import mimetypes
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


@app.route('/editor')
def editor():
    return render_template('Documentos/editor.html')


if __name__ == '__main__':
    app.run(debug=True)
