from flask import Blueprint, jsonify, request, render_template
import os
import mysql.connector
from werkzeug.utils import secure_filename
from flask import current_app
from flask import redirect, url_for, flash
from flask import send_from_directory


# Crear el blueprint para Almacen
almacen_bp = Blueprint('almacen', __name__)

# Configuración para MySQL (ajusta estos datos según tu entorno)
db_config = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'mydatabase'  # Ajusta el nombre de la base de datos
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

# Ruta directa para la carpeta 'uploads' que está fuera de 'static'
UPLOADS_PATH = os.path.join(os.getcwd(), 'uploads')

# Verificar que la carpeta 'uploads' exista
if not os.path.exists(UPLOADS_PATH):
    os.makedirs(UPLOADS_PATH)

@almacen_bp.route('/archivo', methods=['POST'])
def upload_archivo():
    if 'file' not in request.files:
        flash('No se envió ningún archivo', 'error')
        return redirect(url_for('almacen.index_almacen'))

    file = request.files['file']
    if file.filename == '':
        flash('El archivo no tiene nombre', 'error')
        return redirect(url_for('almacen.index_almacen'))

    # Guardar el archivo en la carpeta 'uploads'
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOADS_PATH, filename)  # Ruta completa del archivo
    file.save(filepath)

    # Insertar información del archivo en la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO archivos (nombre, tipo, tamano, ruta) VALUES (%s, %s, %s, %s)",
        (filename, file.mimetype, os.path.getsize(filepath), os.path.join('uploads', filename))
    )
    conn.commit()
    conn.close()

    flash('Archivo subido exitosamente', 'success')
    return redirect(url_for('almacen.index_almacen'))

# Ruta para mostrar la página principal con los archivos
# Esta ruta debe estar solo en almacen.py
@almacen_bp.route('/', methods=['GET'])
def index_almacen():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM archivos")
    archivos = cursor.fetchall()
    conn.close()
    return render_template('almacen/indexAlmacen.html', archivos=archivos)


# Ruta para buscar archivos por nombre
@almacen_bp.route('/buscar_archivo', methods=['GET'])
def buscar_archivo():
    nombre = request.args.get('nombre')  # Parámetro enviado desde el frontend
    conn = get_db_connection()
    cursor = conn.cursor()

    # Buscar archivo por nombre
    query = "SELECT * FROM archivos WHERE nombre = %s"
    cursor.execute(query, (nombre,))
    archivo = cursor.fetchone()  # Obtiene solo un resultado

    conn.close()

    if archivo:
        return jsonify({
            "id": archivo[0],
            "nombre": archivo[1],
            "tipo": archivo[2],
            "tamaño": archivo[3],
            "ruta": archivo[4],
            "fecha": archivo[5]
        })
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404



# Ruta para descargar un archivo
@almacen_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Servir el archivo desde la carpeta 'uploads'
    return send_from_directory(UPLOADS_PATH, filename)

@almacen_bp.route('/archivo/delete/<int:id>', methods=['POST'])
def delete_archivo(id):
    # Conexión a la base de datos para eliminar el archivo
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM archivos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    
    flash('Archivo eliminado correctamente', 'success')
    return redirect(url_for('almacen.index_almacen'))