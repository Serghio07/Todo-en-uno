from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Clave para JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Inicializar Firebase
cred = credentials.Certificate('path/to/your/firebase_credentials.json')
firebase_admin.initialize_app(cred)

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta de contacto
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Ruta de registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user(email=email, password=password)
            return jsonify({"message": "Usuario registrado exitosamente", "uid": user.uid})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return render_template('register.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.get_user_by_email(email)
            # Aquí deberías verificar la contraseña; Firebase no lo permite directamente en el backend.
            access_token = create_access_token(identity={"email": email})
            return jsonify(access_token=access_token)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

