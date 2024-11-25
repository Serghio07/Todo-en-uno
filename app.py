import logging
from flask import Flask, session, render_template, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.pagos import db
from auth import auth_bp
from admin import admin_bp
from user import user_bp
from almacen import almacen_bp  


# Registrar el blueprint en la aplicación principal


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
app.secret_key = 'tu_secreto'
db.init_app(app)





# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(almacen_bp, url_prefix='/almacen')

@app.before_request
def set_default_role():
    if 'role' not in session:
        session['role'] = 'Sin Registro'
    # Registrar el rol actual en los logs
    logger.info(f"Rol actual del usuario: {session.get('role')}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('Autenticacion/login.html')

@app.route('/register')
def register():
    return render_template('Autenticacion/registro.html')

@app.route('/pagos/pago')
def pago():
    return render_template('Pagos/pago.html')  # Ruta relativa dentro de 'templates'



if __name__ == '__main__':
    app.run(debug=True)
