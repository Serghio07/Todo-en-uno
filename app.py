from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia si es necesario
app.config['MYSQL_PASSWORD'] = 'rootpassword'  # Cambia si es necesario
app.config['MYSQL_DB'] = 'mydatabase'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se almacenarán los archivos
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'png'}  # Tipos de archivo permitidos

mysql = MySQL(app)

# Verifica que la carpeta de carga exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Función para verificar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal: Listar archivos
@app.route('/')
def index():
    search_query = request.args.get('search', '')  # Obtener el término de búsqueda
    cur = mysql.connection.cursor()
    
    # Buscar archivos por nombre
    if search_query:
        cur.execute("SELECT * FROM archivos WHERE nombre LIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM archivos")
        
    archivos = cur.fetchall()
    cur.close()
    
    return render_template('indexAlmacen.html', archivos=archivos, search_query=search_query)

# Ruta para subir archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Guardar información en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO archivos (nombre, tipo, tamano, ruta) VALUES (%s, %s, %s, %s)",
                    (filename, file.content_type, os.path.getsize(filepath), filepath))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    return 'Tipo de archivo no permitido', 400

# Ruta para listar archivos
@app.route('/list')
def list_files():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM archivos")
    archivos = cur.fetchall()
    cur.close()
    return render_template('indexAlmacen.html', archivos=archivos)

# Ruta para descargar archivos
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para eliminar archivo
@app.route('/delete/<int:id>', methods=['POST'])
def delete_file(id):
    cur = mysql.connection.cursor()
    
    # Obtener información del archivo a eliminar
    cur.execute("SELECT * FROM archivos WHERE id = %s", (id,))
    archivo = cur.fetchone()
    
    if archivo:
        # Eliminar archivo de la base de datos
        cur.execute("DELETE FROM archivos WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        # Eliminar el archivo físico
        os.remove(archivo[3])  # Asegúrate de que la ruta esté en la columna correcta
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
