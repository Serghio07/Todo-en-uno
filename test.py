from conexion import engine

try:
    connection = engine.connect()
    print("Conexión exitosa")
except Exception as e:
    print(f"Error en la conexión: {e}")
