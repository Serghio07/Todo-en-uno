from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Sobre_Nosotros')
def about():
    return render_template('Sobre_Nosotros.html')

@app.route('/Servicios')
def services():
    return render_template('Servicios.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Almacen')
def almacen():
    return render_template('indexAlmacen.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')  # Crea faq.html en templates

if __name__ == '__main__':
    app.run(debug=True)