from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), default='user')
    saldo = db.Column(db.Float, default=0.0)
