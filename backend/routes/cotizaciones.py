from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Cotizacion, Servicio, Insumo
from backend.schemas import CotizacionCreate, CotizacionResponse
from backend.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/quotes", tags=["Cotizaciones"])

# 🔹 Obtener todas las cotizaciones de un usuario
@router.get("/", response_model=list[CotizacionResponse])
def get_cotizaciones(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Obtiene todas las cotizaciones del usuario autenticado.  
    **Requiere autenticación.**
    """
    cotizaciones = db.query(Cotizacion).filter(Cotizacion.cliente_id == user["id"]).all()
    
    if not cotizaciones:
        raise HTTPException(status_code=404, detail="No tienes cotizaciones registradas")
    
    return cotizaciones

# 🔹 Crear una nueva cotización
@router.post("/", response_model=CotizacionResponse, status_code=status.HTTP_201_CREATED)
def create_cotizacion(cotizacion: CotizacionCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Crea una nueva cotización basada en los servicios e insumos seleccionados.  
    **Requiere autenticación de usuario.**
    """
    servicio = db.query(Servicio).filter(Servicio.id == cotizacion.servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="El servicio no existe")

    # 🔹 Calcular subtotal sumando el precio base del servicio + costo de insumos
    subtotal = servicio.precio_base
    insumos_total = sum(db.query(Insumo).filter(Insumo.id.in_(cotizacion.insumos)).with_entities(Insumo.costo).all())[0] if cotizacion.insumos else 0

    total = subtotal + insumos_total - cotizacion.descuento

    new_cotizacion = Cotizacion(
        cliente_id=user["id"],
        servicio_id=cotizacion.servicio_id,
        subtotal=subtotal,
        descuento=cotizacion.descuento,
        total=total,
        estado="pendiente"
    )
    
    db.add(new_cotizacion)
    db.commit()
    db.refresh(new_cotizacion)
    return new_cotizacion

# 🔹 Eliminar una cotización (solo administradores)
@router.delete("/{cotizacion_id}", status_code=status.HTTP_200_OK)
def delete_cotizacion(cotizacion_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """
    Elimina una cotización por ID.  
    **Requiere autenticación de administrador.**
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    db.delete(cotizacion)
    db.commit()
    return {"message": f"Cotización con ID {cotizacion.id} eliminada correctamente"}
