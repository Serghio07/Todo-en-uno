from datetime import datetime
from models import db

class ProgramacionImpresion(db.Model):
    __tablename__ = 'programacion_impresion'
    id = db.Column(db.Integer, primary_key=True)
    fecha_impresion = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")  # Estados: Pendiente, Completo, Cancelado
    numero_copias = db.Column(db.Integer, nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
