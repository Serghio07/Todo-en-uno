from models import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Cambiado de hashed_password a password
    nombre = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(20), default='user')
    saldo = db.Column(db.Float, default=0.0)

