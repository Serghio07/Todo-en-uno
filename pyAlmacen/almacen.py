from flask import Blueprint, jsonify, request
import os
import mysql.connector
from werkzeug.utils import secure_filename

# Crear el blueprint para Almacen
almacen_bp = Blueprint('almacen', __name__)

# Configuración para MySQL (ajusta estos datos según tu entorno)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_password',
    'database': 'nombre_base_datos'
}

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Función para obtener todos los archivos
@almacen_bp.route('/archivos', methods=['GET'])
def get_archivos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM archivos")
    archivos = cursor.fetchall()
    conn.close()
    return jsonify(archivos)

# Función para agregar un archivo
@almacen_bp.route('/archivo', methods=['POST'])
def upload_archivo():
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'El archivo no tiene nombre'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join('static/uploads', filename)
    file.save(filepath)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO archivos (nombre, tipo, tamanio, ruta) VALUES (%s, %s, %s, %s)",
        (filename, file.mimetype, os.path.getsize(filepath), filepath)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Archivo subido exitosamente'}), 201

# Función para eliminar un archivo
@almacen_bp.route('/archivo/<int:id>', methods=['DELETE'])
def delete_archivo(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener el archivo antes de eliminarlo
    cursor.execute("SELECT ruta FROM archivos WHERE id = %s", (id,))
    archivo = cursor.fetchone()
    if not archivo:
        return jsonify({'error': 'Archivo no encontrado'}), 404

    # Eliminar archivo del sistema
    os.remove(archivo[0])

    # Eliminar archivo de la base de datos
    cursor.execute("DELETE FROM archivos WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Archivo eliminado exitosamente'})
