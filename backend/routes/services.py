from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Servicio
from backend.schemas import ServiceCreate, ServicioResponse
from backend.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/services", tags=["Servicios"])

# 🔹 Obtener todos los servicios (solo usuarios autenticados)
@router.get("/", response_model=list[ServicioResponse])
def get_services(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Obtiene la lista de todos los servicios. 
    **Solo usuarios autenticados pueden acceder.**
    """
    services = db.query(Servicio).all()
    if not services:
        raise HTTPException(status_code=404, detail="No hay servicios disponibles")
    return services

# 🔹 Crear un nuevo servicio (solo administradores)
@router.post("/", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service: ServiceCreate, 
    db: Session = Depends(get_db), 
    admin: dict = Depends(get_current_admin)
):
    """
    Crea un nuevo servicio. 
    **Requiere autenticación de administrador.**
    """
    new_service = Servicio(
        nombre=service.nombre,
        descripcion=service.descripcion,
        precio_base=service.precio_base
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# 🔹 Eliminar un servicio (solo administradores)
@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
def delete_service(service_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """
    Elimina un servicio por ID. 
    **Requiere autenticación de administrador.**
    """
    service = db.query(Servicio).filter(Servicio.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    db.delete(service)
    db.commit()
    return {"message": f"Servicio '{service.nombre}' eliminado exitosamente"}
