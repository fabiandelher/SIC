from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

# Tabla intermedia para la relación muchos a muchos entre Servicios e Insumos
servicio_insumo = Table(
    "servicio_insumo",
    Base.metadata,
    Column("servicio_id", Integer, ForeignKey("servicios.id")),
    Column("insumo_id", Integer, ForeignKey("insumos.id"))
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    rol = Column(String, default="cliente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Servicio(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio_base = Column(Float)

    # Relación con insumos (muchos a muchos)
    insumos = relationship("Insumo", secondary=servicio_insumo, back_populates="servicios")

class Insumo(Base):
    __tablename__ = "insumos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    costo = Column(Float)

    # Relación con servicios
    servicios = relationship("Servicio", secondary=servicio_insumo, back_populates="insumos")

class Cotizacion(Base):
    __tablename__ = "cotizaciones"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    subtotal = Column(Float)
    descuento = Column(Float, default=0)
    total = Column(Float)
    estado = Column(String, default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
