from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for, flash
import os
import pymysql
from datetime import datetime
from werkzeug.utils import secure_filename
from auth import token_required

impresion_bp = Blueprint('impresion', __name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'mypassword',
    'database': 'mydatabase'
}

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Ruta para mostrar documentos disponibles y la página de impresión
@impresion_bp.route('/', methods=['GET'])
@token_required
def index_impresion(decoded_token):
    usuario_id = decoded_token.get('user_id')
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM almacen WHERE id IS NOT NULL")
        archivos = cursor.fetchall()
    conn.close()
    return render_template('impresion/indexImpresion.html', archivos=archivos)

# Ruta para guardar la programación de una impresión
@impresion_bp.route('/programar', methods=['POST'])
@token_required
def programar_impresion(decoded_token):
    usuario_id = decoded_token.get('user_id')
    data = request.json

    try:
        documento_id = data.get('documento_id')
        fecha_programada = data.get('fecha_programada')
        estado = data.get('estado')
        numero_copias = data.get('numero_copias')

        if not all([documento_id, fecha_programada, estado, numero_copias]):
            return jsonify({"error": "Datos incompletos"}), 400

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO impresion (documento_id, fecha_programada, estado, numero_copias) VALUES (%s, %s, %s, %s)",
                (documento_id, fecha_programada, estado, numero_copias)
            )
            conn.commit()
        conn.close()
        return jsonify({"message": "Impresión programada exitosamente"}), 200
    except Exception as e:
        print("Error al programar la impresión:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

# Ruta para cargar documentos para la tabla
@impresion_bp.route('/documentos', methods=['GET'])
@token_required
def get_documentos(decoded_token):
    usuario_id = decoded_token.get('user_id')

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre AS titulo, tipo, DATE_FORMAT(fecha, '%%Y-%%m-%%d %%H:%%i:%%s') AS fecha_creacion "
                "FROM almacen WHERE id IS NOT NULL"
            )
            documentos = cursor.fetchall()
        conn.close()
        return jsonify(documentos), 200
    except Exception as e:
        print("Error al obtener documentos:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@impresion_bp.route('/guardar_impresion', methods=['POST'])
@token_required
def guardar_impresion(decoded_token):
    try:
        print("Iniciando el proceso de guardar impresión...")  # LOG 1
        usuario_id = decoded_token.get("user_id")
        archivo_id = request.form.get("archivo_id")
        fecha_programada = request.form.get("fecha_programada")
        estado = request.form.get("estado")
        numero_copias = request.form.get("numero_copias")

        print(f"Datos recibidos: usuario_id={usuario_id}, archivo_id={archivo_id}, "
              f"fecha_programada={fecha_programada}, estado={estado}, numero_copias={numero_copias}")  # LOG 2

        # Verificación de datos obligatorios
        if not archivo_id or not fecha_programada or not numero_copias:
            print("Error: Faltan campos obligatorios")  # LOG 3
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Validar que el archivo existe y pertenece al usuario
        print("Verificando que el archivo exista y pertenezca al usuario...")  # LOG 4
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM archivos WHERE id = %s AND usuario_id = %s",
                (archivo_id, usuario_id)
            )
            archivo = cursor.fetchone()
            print(f"Archivo encontrado: {archivo}")  # LOG 5
            if not archivo:
                print("Error: El archivo no existe o no pertenece al usuario")  # LOG 6
                return jsonify({"error": "El archivo no existe o no pertenece al usuario"}), 400

        # Guardar la programación de impresión en la base de datos
        print("Insertando programación de impresión en la base de datos...")  # LOG 7
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO programacion_impresion (fecha_impresion, estado, numero_copias, archivo_id, usuario_id) "
                "VALUES (%s, %s, %s, %s, %s)",
                (fecha_programada, estado, numero_copias, archivo_id, usuario_id)
            )
            conn.commit()
            print("Programación de impresión guardada exitosamente.")  # LOG 8

        return jsonify({"message": "Impresión guardada exitosamente"}), 200

    except Exception as e:
        print("Error al guardar la impresión:", e)  # LOG 9
        return jsonify({"error": "No se pudo guardar la impresión"}), 500

