document.getElementById('registerButton').addEventListener('click', async () => {
    // Obtener los valores del formulario
    const name = document.getElementById('registerName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value.trim();
    const confirmPassword = document.getElementById('registerConfirmPassword').value.trim();
    const messageElement = document.getElementById('registerMessage');

    console.log("Datos obtenidos del formulario:", {
        nombre: name,
        email: email,
        password: password,
        confirmPassword: confirmPassword
    });

    // Validaciones en el frontend
    if (!name || !email || !password || !confirmPassword) {
        console.error("Validación fallida: campos incompletos.");
        messageElement.textContent = "Todos los campos son obligatorios.";
        messageElement.style.color = "red";
        return;
    }

    if (password !== confirmPassword) {
        console.error("Validación fallida: las contraseñas no coinciden.");
        messageElement.textContent = "Las contraseñas no coinciden.";
        messageElement.style.color = "red";
        return;
    }

    try {
        console.log("Enviando solicitud al servidor...");

        // Realizar la solicitud al endpoint de registro
        const response = await fetch('http://127.0.0.1:5000/auth/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: name,
                email: email,
                password: password,
                rol: 'user' // Rol predeterminado
            })
        });

        console.log("Respuesta del servidor recibida. Procesando...");
        const data = await response.json();

        if (response.ok) {
            console.log("Registro exitoso. Respuesta del servidor:", data);

            // Mostrar mensaje de éxito
            messageElement.textContent = data.message || "Registro exitoso.";
            messageElement.style.color = "green";

            // Redirigir al login después de unos segundos
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            console.error("Error del servidor. Respuesta recibida:", data);
            messageElement.textContent = data.error || "Error al registrarse.";
            messageElement.style.color = "red";
        }
    } catch (error) {
        // Manejo de errores de conexión
        console.error("Error de conexión al servidor:", error);
        messageElement.textContent = "Error de conexión al servidor.";
        messageElement.style.color = "red";
    }
});
