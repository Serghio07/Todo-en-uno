from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from conexion import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Nuevo campo para la contraseña
    rol = Column(String(20), nullable=False)

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
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_programada = Column(DateTime, nullable=False)
    estado = Column(String(20), nullable=False)
    numero_copias = Column(Integer, nullable=False)
    documento_id = Column(Integer, ForeignKey('documento.id'))

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
