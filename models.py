from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from conexion import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    rol = Column(String(50), default='user')

    # Relaciones
    pagos = relationship("Pago", back_populates="usuario")
    documentos = relationship("Documento", back_populates="usuario")

class Pago(Base):
    __tablename__ = 'pago'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Float(2), nullable=False)
    fecha_pago = Column(DateTime, nullable=False)
    metodo = Column(String(20), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="pagos")

class Documento(Base):
    __tablename__ = 'documento'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    almacenamiento_id = Column(Integer, ForeignKey('almacenamiento.id'), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="documentos")
    almacenamiento = relationship("Almacenamiento", back_populates="documentos", uselist=False)
    impresiones = relationship("Impresion", back_populates="documento")
    versiones = relationship("VersionControl", back_populates="documento")
    plantillas = relationship("Plantilla", back_populates="documento")

class Impresion(Base):
    __tablename__ = 'impresion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_programada = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False)
    numero_copias = Column(Integer, nullable=False)
    documento_id = Column(Integer, ForeignKey('documento.id'), nullable=False)

    # Relaciones
    documento = relationship("Documento", back_populates="impresiones")

class Almacenamiento(Base):
    __tablename__ = 'almacenamiento'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    espacio_utilizado = Column(Float, nullable=False)
    fecha_almacenamiento = Column(DateTime, nullable=False)

    # Relaciones
    documentos = relationship("Documento", back_populates="almacenamiento")

class Plantilla(Base):
    __tablename__ = 'plantilla'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_version = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    documento_id = Column(Integer, ForeignKey('documento.id'), nullable=False)

    # Relaciones
    documento = relationship("Documento", back_populates="plantillas")

class VersionControl(Base):
    __tablename__ = 'version_control'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(20), nullable=False)
    fecha_version = Column(DateTime, nullable=False)
    comentario = Column(Text, nullable=True)
    documento_id = Column(Integer, ForeignKey('documento.id'), nullable=False)

    # Relaciones
    documento = relationship("Documento", back_populates="versiones")
