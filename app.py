from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('Sobre_Nosotros.html')

@app.route('/servicios')
def services():
    return render_template('Servicios.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/almacen')
def almacen():  # Aquí cambiamos el nombre de la función a "almacen"
    return render_template('Almacen/indexAlmacen.html')



if __name__ == '__main__':
    app.run(debug=True)
