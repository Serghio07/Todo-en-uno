from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Datos de conexión
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"  # Cambia este valor si estás usando un host diferente
DB_PORT = "3306"
DB_NAME = "mydatabase"

# Crear la URI de conexión
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de conexión
engine = create_engine(DATABASE_URI, pool_pre_ping=True)

# Crear una sesión para manejar las transacciones
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Crear la base para los modelos
Base = declarative_base()

def get_db():
    """
    Esta función devuelve una sesión de la base de datos. 
    Úsala con el contexto `with` o cierra la sesión manualmente para evitar fugas de conexión.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
