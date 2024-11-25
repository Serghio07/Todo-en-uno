async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const messageElement = document.getElementById('loginMessage');

    if (!email || !password) {
        messageElement.textContent = "Por favor, completa todos los campos.";
        messageElement.style.color = "red";
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('authToken', data.token); // Guardar el token
            messageElement.textContent = "Inicio de sesión exitoso. Redirigiendo...";
            messageElement.style.color = "green";

            setTimeout(() => {
                window.location.href = '/'; // Redirigir al inicio
            }, 2000);
        } else {
            messageElement.textContent = data.error || "Error al iniciar sesión.";
            messageElement.style.color = "red";
        }
    } catch (error) {
        messageElement.textContent = "Error de conexión al servidor.";
        messageElement.style.color = "red";
    }
}
