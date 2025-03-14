import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.database import SessionLocal, get_db
from backend.models import Usuario
from sqlalchemy.orm import Session

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de autenticación
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Configuración de encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticación OAuth2 (utilizado para recibir el token en cada solicitud)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/")

# 🔹 Funciones de encriptación y verificación de contraseñas
def hash_password(password: str) -> str:
    """Hashea una contraseña con bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña en texto plano contra un hash."""
    return pwd_context.verify(plain_password, hashed_password)

# 🔹 Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Crea un JWT Token con información del usuario."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Función para verificar un token JWT
def verify_token(token: str):
    """Verifica un JWT y devuelve el payload si es válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# 🔹 Obtener usuario actual basado en el token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Verifica el token y devuelve el usuario autenticado."""
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="No se encontró usuario en el token")

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user

# 🔹 Obtener administrador basado en el token JWT
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Verifica el token y devuelve el usuario si es administrador."""
    user = get_current_user(token, db)
    if user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador",
        )
    return user
