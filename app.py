from flask import Flask, render_template
import paypalrestsdk

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Ruta para crear el pago
@app.route('/pay')
def pay():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for('payment_success', _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Documento Impreso",
                    "sku": "001",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "10.00",
                "currency": "USD"},
            "description": "Pago por el servicio de impresión de documentos"}]})

    if payment.create():
        # Redirige al usuario a PayPal para completar el pago
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return "Error al crear el pago"

# Ruta para manejar el éxito del pago
@app.route('/payment_success')
def payment_success():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return "Pago realizado con éxito"
    else:
        return "El pago no pudo completarse"

# Ruta para manejar la cancelación del pago
@app.route('/payment_cancel')
def payment_cancel():
    return "El pago fue cancelado"

if __name__ == '__main__':
    app.run(debug=True)
