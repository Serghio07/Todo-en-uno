from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='user')
    saldo = db.Column(db.Float, default=0.0)
    documentos = db.relationship('Documento', backref='usuario', lazy=True)
    transacciones = db.relationship('Transaccion', backref='usuario', lazy=True)
    programaciones = db.relationship('ProgramacionImpresion', backref='usuario', lazy=True)
    archivos = db.relationship('Archivo', backref='usuario', lazy=True)

# Modelo de Documentos
class Documento(db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    versiones = db.relationship('Version', backref='documento', lazy=True)
    programaciones = db.relationship('ProgramacionImpresion', backref='documento', lazy=True)

# Modelo de Plantillas
class Plantilla(db.Model):
    __tablename__ = 'plantillas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)

# Modelo de Versiones
class Version(db.Model):
    __tablename__ = 'versiones'
    id = db.Column(db.Integer, primary_key=True)
    numero_version = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)

# Modelo de Transacciones
class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    monto = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ej: Pago por impresión, almacenamiento
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Modelo de Programaciones de Impresión
class ProgramacionImpresion(db.Model):
    __tablename__ = 'programacion_impresion'
    id = db.Column(db.Integer, primary_key=True)
    fecha_impresion = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")  # Pendiente, Completo, Cancelado
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Modelo de Archivos
class Archivo(db.Model):
    __tablename__ = 'archivos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    tamano = db.Column(db.Float, nullable=False)
    ruta = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Crear todas las tablas
with app.app_context():
    db.create_all()
    print("Tablas creadas exitosamente.")
