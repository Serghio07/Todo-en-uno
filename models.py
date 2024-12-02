from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from conexion import Base
from flask_sqlalchemy import SQLAlchemy

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # Nota: Este campo podría ser 'hashed_password'
    nombre = Column(String(255), nullable=False)
    rol = Column(String(50), default='user')
    # Relaciones
    pagos = relationship("Pago", back_populates="usuario")
    documentos = relationship("Documento", back_populates="usuario")

class Pago(Base):
    __tablename__ = 'pago'
    
    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float(2), nullable=False)
    fecha_pago = Column(DateTime, nullable=False)
    metodo = Column(String(20), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    # Relaciones
    usuario = relationship("Usuario", back_populates="pagos")


class Documento(Base):
    __tablename__ = 'documento'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    almacenamiento_id = Column(Integer, ForeignKey('almacenamiento.id'))

    # Relaciones
    usuario = relationship("Usuario", back_populates="documentos")
    almacenamiento = relationship("Almacenamiento", back_populates="documentos")
    impresiones = relationship("Impresion", back_populates="documento")
    versiones = relationship("VersionControl", back_populates="documento")
    plantillas = relationship("Plantilla", back_populates="documento")


class Impresion(Base):
    __tablename__ = 'impresion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_impresion = Column(DateTime, nullable=False)  # Fecha y hora de la programación de impresión
    estado = Column(String(20), default='Pendiente')  # Estado inicial: Pendiente, Completado, Fallido, etc.
    documento_id = Column(Integer, ForeignKey('documento.id'), nullable=False)  # ID del documento a imprimir
    numero_copias = Column(Integer, nullable=False, default=1)  # Número de copias a imprimir
    tipo_impresion = Column(String(50), default='Simplex')  # Tipo de impresión: Simplex (una cara) o Dúplex (doble cara)
    tamaño_papel = Column(String(20), default='A4')  # Tamaño del papel: A4, Carta, Legal, etc.
    color_impresion = Column(String(20), default='Color')  # Tipo de impresión: Color o Blanco y Negro
    comentarios = Column(Text, nullable=True)  # Comentarios adicionales sobre la impresión

    # Relaciones
    documento = relationship("Documento", back_populates="impresiones")


class Almacenamiento(Base):
    __tablename__ = 'almacenamiento'
    
    id = Column(Integer, primary_key=True, index=True)
    espacio_utilizado = Column(Float, nullable=False)
    fecha_almacenamiento = Column(DateTime, nullable=False)

    # Relaciones
    documentos = relationship("Documento", back_populates="almacenamiento")


class Plantilla(Base):
    __tablename__ = 'plantilla'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_version = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    documento_id = Column(Integer, ForeignKey('documento.id'))

    # Relaciones
    documento = relationship("Documento", back_populates="plantillas")


class VersionControl(Base):
    __tablename__ = 'versioncontrol'
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(20), nullable=False)
    fecha_version = Column(DateTime, nullable=False)
    comentario = Column(Text, nullable=True)
    documento_id = Column(Integer, ForeignKey('documento.id'))

    # Relaciones
    documento = relationship("Documento", back_populates="versiones")
