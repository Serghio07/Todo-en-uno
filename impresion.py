from flask import Blueprint, render_template, request, redirect, url_for, flash
from conexion import get_db  # Obtener la función para la sesión
from sqlalchemy.orm import Session

# Crear el Blueprint para 'impresion'
impresion_bp = Blueprint('impresion', __name__)

# Ruta para la página de impresión (mostrar formulario y documentos)
@impresion_bp.route('/')
def programar_impresion():
    db = next(get_db())  # Obtener la sesión de la base de datos
    documentos = db.execute("SELECT * FROM documentos").fetchall()
    return render_template('impresion.html', documentos=documentos)

# Ruta para buscar un documento por su id
@impresion_bp.route('/buscar_documento', methods=['GET'])
def buscar_documento():
    documento_id = request.args.get('documento_id')
    db = next(get_db())  # Obtener la sesión de la base de datos
    documentos = db.execute(f"SELECT * FROM documentos WHERE id = {documento_id}").fetchall()
    return render_template('impresion.html', documentos=documentos)

# Ruta para programar una impresión (renombrar el endpoint)
@impresion_bp.route('/programar_impresion', methods=['POST'])
def programar_impresion_ruta():
    documento_id = request.form['documento_id']
    db = next(get_db())  # Obtener la sesión de la base de datos
    db.execute(
        "INSERT INTO programacion_impresion (documento_id) VALUES (:documento_id)",
        {'documento_id': documento_id}
    )
    db.commit()
    return redirect(url_for('impresion.programar_impresion'))

# Ruta para crear una programación de impresión (renombrar el endpoint)
@impresion_bp.route('/crear_programacion', methods=['POST'])
def crear_programacion_ruta():
    fecha_impresion = request.form['fecha_programada']
    estado = request.form['estado']
    numero_copias = request.form['numero_copias']
    tipo_impresion = request.form['tipo_impresion']
    tamaño_papel = request.form['tamaño_papel']
    color_impresion = request.form['color_impresion']
    comentarios = request.form['comentarios']
    documento_id = request.form['documento_id']

    db = next(get_db())  # Obtener la sesión de la base de datos

    nueva_programacion = {
        'fecha_impresion': fecha_impresion,
        'estado': estado,
        'numero_copias': numero_copias,
        'tipo_impresion': tipo_impresion,
        'tamaño_papel': tamaño_papel,
        'color_impresion': color_impresion,
        'comentarios': comentarios,
        'documento_id': documento_id
    }

    # Insertar la programación de impresión en la base de datos
    db.execute(
        "INSERT INTO programacion_impresion (fecha_impresion, estado, numero_copias, tipo_impresion, tamaño_papel, color_impresion, comentarios, documento_id) "
        "VALUES (:fecha_impresion, :estado, :numero_copias, :tipo_impresion, :tamaño_papel, :color_impresion, :comentarios, :documento_id)",
        nueva_programacion
    )
    db.commit()

    flash('La programación de impresión fue guardada exitosamente.')
    return redirect(url_for('impresion.programar_impresion'))
