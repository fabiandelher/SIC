from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Cotizacion
from backend.schemas import QuoteCreate
from backend.auth import get_current_user



router = APIRouter()

# Obtener todas las cotizaciones del usuario autenticado
@router.get("/")
def get_quotes(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Cotizacion).filter(Cotizacion.cliente_id == user["sub"]).all()

# Crear una nueva cotización (disponible para usuarios autenticados)
@router.post("/", response_model=QuoteCreate)
def create_quote(quote: QuoteCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    new_quote = Cotizacion(
        cliente_id=user["sub"],
        servicio_id=quote.servicio_id,
        subtotal=quote.subtotal,
        descuento=quote.descuento,
        total=quote.total
    )
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote
