import logging
from flask import Flask, session, render_template, redirect, url_for
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

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,  # Nivel de logs
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato
    handlers=[
        logging.FileHandler("app.log"),  # Archivo donde se guardan los logs
        logging.StreamHandler()  # Mostrar logs en la consola
    ]
)
logger = logging.getLogger(__name__)

# Registrar Blueprints
app.register_blueprint(auth_bp)
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
    return render_template('Autenticacion/register.html')

if __name__ == '__main__':
    app.run(debug=True)
