from fastapi import FastAPI
from backend.routes import users, services, quotes
from backend.database import engine, Base


app = FastAPI()

# Incluir las rutas
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(services.router, prefix="/services", tags=["Servicios"])
app.include_router(quotes.router, prefix="/quotes", tags=["Cotizaciones"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de cotizaciones"}
