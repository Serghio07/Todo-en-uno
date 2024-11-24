from flask import Flask, render_template, request, jsonify
from models.pagos import db
from services.usuarioS import verify_user
from services.pagoS import process_payment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('team.html')

@app.route('/Sobre_Nosotros')
def about():
    return render_template('Sobre_Nosotros.html')

@app.route('/Servicios')
def services():
    return render_template('Servicios.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/verify_user', methods=['POST'])
def verify_user_route():
    data = request.json
    return verify_user(data)

@app.route('/process_payment', methods=['POST'])
def process_payment_route():
    data = request.json
    return process_payment(data)

if __name__ == '__main__':
    app.run(debug=True)
