document.getElementById("payButton").addEventListener("click", () => {
    document.getElementById("authModal").style.display = "block";
});

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
        if (data.valid) {
            document.getElementById("amount").textContent = data.saldo;
            document.getElementById("authModal").style.display = "none";
            document.getElementById("confirmModal").style.display = "block";
            window.localStorage.setItem("userId", data.user_id); // Almacena el ID del usuario
        } else {
            alert(data.error || "Credenciales inválidas");
        }
    } catch (error) {
        console.error("Error al verificar el usuario:", error);
        alert("Ocurrió un error al verificar el usuario. Intenta nuevamente más tarde.");
    }
});

document.getElementById("confirmPayment").addEventListener("click", async () => {
    const userId = localStorage.getItem("userId");
    const amount = parseFloat(document.getElementById("amount").textContent);
    const metodo = "tarjeta"; // Define el método de pago (puede ser dinámico)

    if (!userId || isNaN(amount)) {
        alert("Error: Usuario no autenticado o monto inválido");
        return;
    }

    try {
        console.log("Enviando datos a /process_payment:", { user_id: userId, amount, metodo });

        const response = await fetch("/process_payment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, amount, metodo })
        });

        if (!response.ok) {
            throw new Error("Error en el servidor");
        }

        const data = await response.json();
        if (data.success) {
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
