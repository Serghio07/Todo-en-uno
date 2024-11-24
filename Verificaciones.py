from flask import Flask, request, jsonify
from conexion import get_db
from models import Usuario

app = Flask(__name__)

@app.route('/api/usuario', methods=['POST'])
def crear_usuario():
    data = request.json  # Datos enviados en el cuerpo de la solicitud (JSON)
    
    # Verifica que los datos necesarios estén presentes
    nombre = data.get('nombre')
    email = data.get('email')
    rol = data.get('rol')
    
    if not (nombre and email and rol):
        return jsonify({"error": "Faltan datos necesarios"}), 400
    
    # Crear una instancia del modelo Usuario
    nuevo_usuario = Usuario(nombre=nombre, email=email, rol=rol)
    
    # Guardar en la base de datos
    with get_db() as db:
        db.add(nuevo_usuario)
        db.commit()
    
    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

if __name__ == '__main__':
    app.run(debug=True)
