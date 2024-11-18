from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from conexion import get_db
from models import Usuario
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'tu_secreto'  # Necesario para mensajes flash


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('Sobre_Nosotros.html')

@app.route('/services')
def services():
    return render_template('Servicios.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/almacen')
def almacen():
    return render_template('Almacen/indexAlmacen.html')


@app.route('/login')
def login():
    return render_template('Autenticacion/login.html')


if __name__ == '__main__':
    app.run(debug=True)
