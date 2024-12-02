from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from conexion import get_db  # Obtener la función para la sesión
from models import Usuario  # Si tienes el modelo Usuario
from functools import wraps
from sqlalchemy.orm import Session

# Crear el Blueprint para 'impresion'
impresion_bp = Blueprint('impresion', __name__)

# Función para proteger las rutas que requieren autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Verificar si el usuario está logueado
            flash('Por favor, inicia sesión para continuar.')
            return redirect(url_for('auth.login'))  # Redirige a la página de login
        return f(*args, **kwargs)
    return decorated_function

# Ruta para la página de impresión (mostrar formulario y documentos)
@impresion_bp.route('/')
@login_required  # Solo accesible si el usuario está logueado
def programar_impresion():
    db = next(get_db())  # Obtener la sesión de la base de datos
    documentos = db.execute("SELECT * FROM documentos").fetchall()
    return render_template('impresion.html', documentos=documentos)

# Ruta para buscar un documento por su id
@impresion_bp.route('/buscar_documento', methods=['GET'])
@login_required  # Solo accesible si el usuario está logueado
def buscar_documento():
    documento_id = request.args.get('documento_id')
    db = next(get_db())  # Obtener la sesión de la base de datos
    documentos = db.execute(f"SELECT * FROM documentos WHERE id = {documento_id}").fetchall()
    return render_template('impresion.html', documentos=documentos)

# Ruta para programar una impresión
@impresion_bp.route('/programar_impresion', methods=['POST'])
@login_required  # Solo accesible si el usuario está logueado
def programar():
    documento_id = request.form['documento_id']
    db = next(get_db())  # Obtener la sesión de la base de datos
    db.execute(
        "INSERT INTO programacion_impresion (documento_id) VALUES (:documento_id)",
        {'documento_id': documento_id}
    )
    db.commit()
    return redirect(url_for('impresion.programar_impresion'))

# Ruta para crear una programación de impresión
@impresion_bp.route('/crear_programacion', methods=['POST'])
@login_required  # Solo accesible si el usuario está logueado
def crear_programacion():
    fecha_impresion = request.form['fecha_impresion']
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
        "INSERT INTO programacion_impresion (fecha_impresion, estado, numero_copias, tipo_impresion, tamaño_papel, color_impresion, comentarios, documento_id) VALUES (:fecha_impresion, :estado, :numero_copias, :tipo_impresion, :tamaño_papel, :color_impresion, :comentarios, :documento_id)",
        nueva_programacion
    )
    db.commit()

    flash('La programación de impresión fue guardada exitosamente.')
    return redirect(url_for('impresion.programar_impresion'))
