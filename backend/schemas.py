from pydantic import BaseModel
from typing import List, Optional

# ✅ Esquema para crear un usuario
class UserCreate(BaseModel):
    nombre: str
    email: str
    password: str

# ✅ Esquema para iniciar sesión
class UserLogin(BaseModel):
    email: str
    password: str

# ✅ Esquema para devolver un token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ Esquema para crear un servicio
class ServiceCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float

# ✅ Esquema para crear una cotización (🔹 Agregar esto)
class QuoteCreate(BaseModel):
    servicio_id: int
    subtotal: float
    descuento: float
    total: float
    # Esquema para crear insumos
class InsumoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    costo: float

# Esquema para mostrar insumos
class InsumoResponse(InsumoCreate):
    id: int
    class Config:
        from_attributes = True


# Esquema para mostrar servicios con insumos
class ServicioResponse(ServiceCreate):
    id: int
    insumos: List[InsumoResponse] = []
    class Config:
        from_attributes = True
