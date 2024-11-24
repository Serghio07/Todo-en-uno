from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
import os

# Configuración de la aplicación Flask para Almacen
app = Flask(__name__, template_folder='templates')  # Aseguramos que la carpeta templates esté bien configurada
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'myuser'         
app.config['MYSQL_PASSWORD'] = 'mypassword' 
app.config['MYSQL_DB'] = 'mydatabase'       
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'png'}
app.secret_key = 'supersecretkey'

# Inicializa la conexión MySQL
mysql = MySQL(app)

# Verifica si la carpeta 'uploads' existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal: Listar archivos
@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '')
    cur = mysql.connection.cursor()
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
    cur.execute("SELECT * FROM archivos WHERE id = %s", (id,))
    archivo = cur.fetchone()
    if archivo:
        cur.execute("DELETE FROM archivos WHERE id = %s", (id,))
        mysql.connection.commit()
        ruta_archivo = archivo[3]
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
            flash('Archivo eliminado exitosamente', 'success')
        else:
            flash('El archivo no existe en el servidor', 'danger')
        cur.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
