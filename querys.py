from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db = SQLAlchemy(app)

# Tabla de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # Cliente, Admin, etc.
    documentos = db.relationship('Documento', backref='usuario', lazy=True)

# Tabla de Documentos
class Documento(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ej: Texto, Presentación
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    versiones = db.relationship('Version', backref='documento', lazy=True)

# Tabla de Plantillas
class Plantilla(db.Model):
    __tablename__ = 'plantillas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)  # El contenido base de la plantilla

# Tabla de Versiones (para el control de versiones)
class Version(db.Model):
    __tablename__ = 'versiones'
    id = db.Column(db.Integer, primary_key=True)
    numero_version = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)

# Tabla de Transacciones (para pagos)
class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    monto = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ej: Pago por impresión, almacenamiento
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

# Tabla de Programación de Impresión
class ProgramacionImpresion(db.Model):
    __tablename__ = 'programacion_impresion'
    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)
    fecha_impresion = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")  # Pendiente, Completo, Cancelado
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

# Inicializar la base de datos
with app.app_context():
    db.create_all()