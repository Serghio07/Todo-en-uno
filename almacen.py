from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for, flash, send_from_directory
import os
import pymysql  # Usamos pymysql en lugar de mysql.connector
from werkzeug.utils import secure_filename
from auth import token_required
from datetime import datetime

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
    """Crear una conexión con la base de datos usando pymysql."""
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


# Ruta para renderizar la página principal
@almacen_bp.route('/', methods=['GET'])
@token_required
def index_almacen(decoded_token):
    usuario_id = decoded_token.get('user_id')
    conn = get_db_connection()
    with conn.cursor() as cursor:
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
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, nombre, tipo, tamano, ruta, DATE_FORMAT(fecha, '%Y-%m-%d %H:%i:%s') AS fecha_subida "
            "FROM almacen WHERE id IS NOT NULL"
        )
        archivos = cursor.fetchall()
    conn.close()
    return jsonify(archivos), 200

# Ruta para subir un archivo
@almacen_bp.route('/archivo', methods=['POST'])
@token_required
def upload_archivo(decoded_token):
    file = request.files.get('file')  # Obtener el archivo del formulario
    usuario_id = decoded_token.get('user_id')  # Obtener el ID del usuario autenticado

    if not file or file.filename == '':
        return jsonify({"error": "Archivo no válido"}), 400

 
    
   # Guardar el archivo físicamente
    # Asegurar un nombre seguro para el archivo
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOADS_PATH, filename)
    file.save(filepath)

    # Preparar los datos del archivo
    file_size = os.path.getsize(filepath)
    file_type = file.mimetype
    relative_path = os.path.join('uploads', filename)

    # Guardar la información en la base de datos
    filepath = os.path.join(UPLOADS_PATH, filename)  # Ruta absoluta para guardar el archivo
    file.save(filepath)  # Guardar el archivo en el servidor

    # Crear la ruta relativa con barras normales (para URLs)
    ruta_relativa = os.path.join('uploads', filename).replace("\\", "/")

    # Guardar los detalles del archivo en la base de datos
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Insertar en la tabla archivos
            cursor.execute(
                "INSERT INTO archivos (nombre, tipo, tamano, ruta, usuario_id) VALUES (%s, %s, %s, %s, %s)",
                (filename, file_type, file_size, relative_path, usuario_id)
            )

            # Insertar en la tabla almacen con fecha explícita
            cursor.execute(
                "INSERT INTO almacen (nombre, tipo, tamano, ruta, fecha) VALUES (%s, %s, %s, %s, %s)",
                (filename, file_type, file_size, relative_path, datetime.now())
            )

            conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error al insertar en la base de datos:", e)
        return jsonify({"error": "Error al subir el archivo."}), 500
    finally:
        conn.close()

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO archivos (nombre, tipo, tamano, ruta, usuario_id) VALUES (%s, %s, %s, %s, %s)",
        (filename, file.mimetype, os.path.getsize(filepath), ruta_relativa, usuario_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Archivo subido exitosamente"}), 200



# Ruta para buscar un archivo
@almacen_bp.route('/buscar_archivo', methods=['GET'])
@token_required
def buscar_archivo(decoded_token):
    usuario_id = decoded_token.get('user_id')
    nombre = request.args.get('nombre', '')
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, tipo, tamano, ruta, DATE_FORMAT(fecha_subida, '%%Y-%%m-%%d %%H:%%i:%%s') AS fecha_subida "
            "FROM archivos WHERE usuario_id = %s AND nombre LIKE %s",
            (usuario_id, f"%{nombre}%")
        )
        archivos = cursor.fetchall()
    conn.close()
    return jsonify(archivos)


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
    try:
        with conn.cursor() as cursor:
            # Obtener ruta del archivo
            cursor.execute("SELECT ruta FROM archivos WHERE id = %s AND usuario_id = %s", (id, usuario_id))
            archivo = cursor.fetchone()

            if not archivo:
                return jsonify({"error": "Archivo no encontrado o no tienes permisos para eliminarlo"}), 404
            
            # Eliminar archivo del sistema
            archivo_path = os.path.join(os.getcwd(), archivo['ruta'])
            if os.path.exists(archivo_path):
                os.remove(archivo_path)
            else:
                return jsonify({"error": "El archivo físico no existe en el sistema"}), 404

            # Eliminar registro en la base de datos
            cursor.execute("DELETE FROM archivos WHERE id = %s AND usuario_id = %s", (id, usuario_id))
            conn.commit()

        return jsonify({"message": "Archivo eliminado correctamente"}), 200
    except Exception as e:
        conn.rollback()
        print("Error al eliminar el archivo:", e)
        return jsonify({"error": "No se pudo eliminar el archivo"}), 500
    finally:
        conn.close()
