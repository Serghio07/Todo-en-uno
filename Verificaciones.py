from sqlalchemy import inspect
from conexion import engine

inspector = inspect(engine)

# Obtener lista de tablas
tables = inspector.get_table_names()
print("Tablas en la base de datos:", tables)
