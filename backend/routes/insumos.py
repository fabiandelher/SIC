from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Insumo
from backend.schemas import InsumoCreate, InsumoResponse
from backend.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/insumos", tags=["Insumos"])

# 🔹 Obtener todos los insumos (solo usuarios autenticados)
@router.get("/", response_model=list[InsumoResponse])
def get_insumos(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Obtiene la lista de todos los insumos.  
    **Solo usuarios autenticados pueden acceder.**
    """
    insumos = db.query(Insumo).all()
    if not insumos:
        raise HTTPException(status_code=404, detail="No hay insumos disponibles")
    return insumos

# 🔹 Crear un nuevo insumo (solo administradores)
@router.post("/", response_model=InsumoResponse, status_code=status.HTTP_201_CREATED)
def create_insumo(insumo: InsumoCreate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """
    Crea un nuevo insumo.  
    **Requiere autenticación de administrador.**
    """
    new_insumo = Insumo(
        nombre=insumo.nombre,
        descripcion=insumo.descripcion,
        costo=insumo.costo,
        servicio_id=insumo.servicio_id  # Asegurar que el insumo esté vinculado a un servicio
    )
    db.add(new_insumo)
    db.commit()
    db.refresh(new_insumo)
    return new_insumo

# 🔹 Eliminar un insumo (solo administradores)
@router.delete("/{insumo_id}", status_code=status.HTTP_200_OK)
def delete_insumo(insumo_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """
    Elimina un insumo por ID.  
    **Requiere autenticación de administrador.**
    """
    insumo = db.query(Insumo).filter(Insumo.id == insumo_id).first()
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    
    db.delete(insumo)
    db.commit()
    return {"message": f"Insumo '{insumo.nombre}' eliminado correctamente"}

