from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/servicios')
def servicios():
    return render_template('Servicios.html')

@app.route('/nosotros')
def about():
    return render_template('Sobre_Nosotros.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
