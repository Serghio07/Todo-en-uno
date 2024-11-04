from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db = SQLAlchemy(app)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Rutas para cada una de las páginas
@app.route('/documentos')
def documentos():
    return render_template('documentos.html')

@app.route('/almacenamiento')
def almacenamiento():
    return render_template('almacenamiento.html')

@app.route('/impresion')
def impresion():
    return render_template('impresion.html')

@app.route('/pagos')
def pagos():
    return render_template('pagos.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

# Rutas adicionales para términos y privacidad
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)
