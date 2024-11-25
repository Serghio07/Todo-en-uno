document.getElementById('registerButton').addEventListener('click', async () => {
    const name = document.getElementById('registerName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value.trim();
    const confirmPassword = document.getElementById('registerConfirmPassword').value.trim();
    const messageElement = document.getElementById('registerMessage');

    // Validaciones
    if (!name || !email || !password || !confirmPassword) {
        messageElement.textContent = "Todos los campos son obligatorios.";
        messageElement.style.color = "red";
        return;
    }

    if (password !== confirmPassword) {
        messageElement.textContent = "Las contraseñas no coinciden.";
        messageElement.style.color = "red";
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/auth/registro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: name, email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            messageElement.textContent = "Registro exitoso. Redirigiendo...";
            messageElement.style.color = "green";
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            messageElement.textContent = data.error || "Error en el registro.";
            messageElement.style.color = "red";
        }
    } catch (error) {
        messageElement.textContent = "Error de conexión con el servidor.";
        messageElement.style.color = "red";
    }
});
