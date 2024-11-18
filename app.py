from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

# Configuración de la aplicación Flask
app = Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Cambiar 'localhost' por el nombre del contenedor si usas Docker
app.config['MYSQL_USER'] = 'myuser'     # Usuario de la base de datos
app.config['MYSQL_PASSWORD'] = 'mypassword'  # Contraseña de la base de datos
app.config['MYSQL_DB'] = 'mydatabase'   # Nombre de la base de datos
app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se almacenarán los archivos
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'png'}  # Tipos de archivo permitidos
app.secret_key = 'supersecretkey'  # Clave secreta para sesiones de Flask

# Inicializa la conexión MySQL
mysql = MySQL(app)

# Verifica si la carpeta 'uploads' existe, si no la crea
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal: Listar archivos
@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda
    
    cur = mysql.connection.cursor()
    
    # Si hay un término de búsqueda, ejecuta la consulta con LIKE
    if search_query:
        # Hacer la búsqueda por nombre usando LIKE (insensible a mayúsculas/minúsculas)
        cur.execute("SELECT * FROM archivos WHERE nombre LIKE %s", ('%' + search_query + '%',))
    else:
        # Si no hay término de búsqueda, mostrar todos los archivos
        cur.execute("SELECT * FROM archivos")
        
    archivos = cur.fetchall()
    cur.close()
    
    # Pasar los archivos y la query de búsqueda a la plantilla
    return render_template('Almacen/indexAlmacen.html', archivos=archivos, search_query=search_query)

    
    # Buscar archivos por nombre si se pasa un término de búsqueda
    if search_query:
        cur.execute("SELECT * FROM archivos WHERE nombre LIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM archivos")
        
    archivos = cur.fetchall()
    cur.close()
    
    return render_template('Almacen/indexAlmacen.html', archivos=archivos, search_query=search_query)

# Ruta para subir archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se seleccionó ningún archivo', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Guardar información del archivo en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO archivos (nombre, tipo, tamano, ruta, fecha_subida) VALUES (%s, %s, %s, %s, NOW())",
            (filename, file.content_type, os.path.getsize(filepath), filepath))
        mysql.connection.commit()
        cur.close()

        flash('Archivo subido exitosamente', 'success')
        return redirect(url_for('index'))

    flash('Tipo de archivo no permitido', 'danger')
    return redirect(url_for('index'))

# Ruta para descargar archivos
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para eliminar archivo
@app.route('/delete/<int:id>', methods=['POST'])
def delete_file(id):
    cur = mysql.connection.cursor()
    
    # Obtener la información del archivo a eliminar
    cur.execute("SELECT * FROM archivos WHERE id = %s", (id,))
    archivo = cur.fetchone()
    
    if archivo:
        # Eliminar el archivo de la base de datos
        cur.execute("DELETE FROM archivos WHERE id = %s", (id,))
        mysql.connection.commit()
        
        # Verifica si la ruta del archivo está en el índice correcto
        ruta_archivo = archivo[3]  # Asegúrate de que esto sea la ruta del archivo
        
        if os.path.exists(ruta_archivo):  # Verifica si el archivo realmente existe
            os.remove(ruta_archivo)  # Elimina el archivo físico
            flash('Archivo eliminado exitosamente', 'success')
        else:
            flash('El archivo no existe en el servidor', 'danger')
        
        cur.close()
        
    return redirect(url_for('index'))

    
    # Obtener la información del archivo a eliminar
    cur.execute("SELECT * FROM archivos WHERE id = %s", (id,))
    archivo = cur.fetchone()
    
    if archivo:
        # Eliminar el archivo de la base de datos
        cur.execute("DELETE FROM archivos WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        # Eliminar el archivo físico
        os.remove(archivo[3])  # Asegúrate de que la ruta esté en la columna correcta

        flash('Archivo eliminado exitosamente', 'success')
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
