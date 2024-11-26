from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for, flash, send_from_directory
import os
import mysql.connector
from werkzeug.utils import secure_filename
from auth import token_required

almacen_bp = Blueprint('almacen', __name__)

# Configuración de MySQL
db_config = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'mydatabase'
}

UPLOADS_PATH = os.path.join(os.getcwd(), 'uploads')

if not os.path.exists(UPLOADS_PATH):
    os.makedirs(UPLOADS_PATH)

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Ruta para renderizar la página principal
@almacen_bp.route('/', methods=['GET'])
@token_required
def index_almacen(decoded_token):
    usuario_id = decoded_token.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM archivos WHERE usuario_id = %s", (usuario_id,))
    archivos = cursor.fetchall()
    conn.close()
    return render_template('almacen/indexAlmacen.html', archivos=archivos)

# Ruta para obtener archivos de un usuario
@almacen_bp.route('/archivos', methods=['GET'])
@token_required
def get_archivos(decoded_token):
    usuario_id = decoded_token.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM archivos WHERE usuario_id = %s", (usuario_id,))
    archivos = cursor.fetchall()
    conn.close()
    archivos_data = [
        {"id": archivo[0], "nombre": archivo[1], "tipo": archivo[2], "tamano": archivo[3], "ruta": archivo[4], "fecha_subida": archivo[5].strftime("%Y-%m-%d %H:%M:%S") if archivo[5] else "Sin fecha"}
        for archivo in archivos
    ]
    return jsonify(archivos_data), 200

# Ruta para subir un archivo
@almacen_bp.route('/archivo', methods=['POST'])
@token_required
def upload_archivo(decoded_token):
    file = request.files.get('file')
    usuario_id = decoded_token.get('user_id')

    if not file or file.filename == '':
        return jsonify({"error": "Archivo no válido"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOADS_PATH, filename)
    file.save(filepath)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO archivos (nombre, tipo, tamano, ruta, usuario_id) VALUES (%s, %s, %s, %s, %s)",
        (filename, file.mimetype, os.path.getsize(filepath), os.path.join('uploads', filename), usuario_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Archivo subido exitosamente"}), 200

# Ruta para buscar un archivo
@almacen_bp.route('/buscar_archivo', methods=['GET'])
@token_required
def buscar_archivo(decoded_token):
    usuario_id = decoded_token.get('user_id')
    nombre = request.args.get('nombre')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM archivos WHERE usuario_id = %s AND nombre LIKE %s", (usuario_id, f"%{nombre}%"))
    archivos = cursor.fetchall()
    conn.close()
    if archivos:
        return jsonify([{"id": archivo[0], "nombre": archivo[1]} for archivo in archivos]), 200
    else:
        return jsonify({"error": "No se encontraron archivos"}), 404

# Ruta para descargar un archivo
@almacen_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOADS_PATH, filename)

# Ruta para eliminar un archivo
@almacen_bp.route('/archivo/delete/<int:id>', methods=['POST'])
@token_required
def delete_archivo(decoded_token, id):
    usuario_id = decoded_token.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ruta FROM archivos WHERE id = %s AND usuario_id = %s", (id, usuario_id))
    archivo = cursor.fetchone()
    if not archivo:
        return jsonify({"error": "Archivo no encontrado o sin permisos"}), 404
    os.remove(archivo[0])  # Eliminar archivo del sistema
    cursor.execute("DELETE FROM archivos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Archivo eliminado correctamente"}), 200
