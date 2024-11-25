// Abrir modal de autenticación
document.getElementById("payButton").addEventListener("click", () => {
    document.getElementById("authModal").style.display = "block";
});

// Manejo del formulario de autenticación
document.getElementById("authForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/verify_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            throw new Error("Error en el servidor");
        }

        const data = await response.json();
        console.log("Respuesta del servidor:", data); // Debugging

        if (data.valid) {
            document.getElementById("authModal").style.display = "none";
            document.getElementById("confirmModal").style.display = "block";

            // Obtener el monto del pago desde la URL
            const paymentAmount = parseFloat(new URLSearchParams(window.location.search).get('monto'));

            // Mostrar el monto correcto en el modal de confirmación
            if (!isNaN(paymentAmount)) {
                document.getElementById("amount").textContent = `$${paymentAmount}`;
            } else {
                alert("No se encontró un monto válido para procesar.");
                document.getElementById("confirmModal").style.display = "none";
            }

            // Guardar el ID del usuario en localStorage
            window.localStorage.setItem("userId", data.user_id);
        } else {
            alert(data.error || "Credenciales inválidas");
        }
    } catch (error) {
        console.error("Error al verificar el usuario:", error);
        alert("Ocurrió un error al verificar el usuario. Intenta nuevamente más tarde.");
    }
});

// Confirmar y procesar el pago
document.getElementById("confirmPayment").addEventListener("click", async () => {
    const userId = localStorage.getItem("userId");
    const paymentAmount = parseFloat(new URLSearchParams(window.location.search).get('monto'));
    const metodo = "tarjeta";

    if (!userId || isNaN(paymentAmount)) {
        alert("Error: Usuario no autenticado o monto inválido");
        return;
    }

    try {
        console.log("Enviando datos a /process_payment:", { user_id: userId, amount: paymentAmount, metodo });

        const response = await fetch("/process_payment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, amount: paymentAmount, metodo }),
        });

        if (!response.ok) {
            throw new Error("Error en el servidor");
        }

        const data = await response.json();
        if (data.success) {
            alert("Pago realizado con éxito.");
            window.location.href = "/result/success";
        } else {
            alert(data.error || "Error en el pago");
            window.location.href = "/result/error";
        }
    } catch (error) {
        console.error("Error al procesar el pago:", error);
        alert("Ocurrió un error al procesar el pago. Intenta nuevamente más tarde.");
    }
});
