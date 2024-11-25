document.addEventListener("DOMContentLoaded", async () => {
    const navLinks = document.querySelector(".nav-links"); // Selecciona el contenedor de enlaces
    const token = localStorage.getItem("authToken"); // Recupera el token desde localStorage

    if (!token) {
        // Si no hay token, renderiza opciones para usuarios no registrados
        navLinks.innerHTML = `
            <li><a href="/">Inicio</a></li>
            <li><a href="/soporte">Soporte Técnico</a></li>
            <li><a href="/version_freemium">Impresión</a></li>
            <li><a href="/software">Información</a></li>
            <li><a href="/catalogo">Subscripciones</a></li>
            <li><a href="/login">Iniciar Sesión</a></li>
        `;
        return;
    }

    try {
        // Verificar el token con el servidor
        const response = await fetch("http://127.0.0.1:5000/auth/verify_token", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error("Token inválido o expirado");
        }

        const data = await response.json(); // Decodifica la respuesta del servidor
        const userRole = data.user.rol; // Obtiene el rol del usuario
        const userName = data.user.nombre; // Obtiene el nombre del usuario
        console.log("Respuesta del servidor:", data);

        // Renderizar enlaces según el rol
        let links = `<li><a href="/">Inicio</a></li>`;
        if (userRole === "Sin Registro") {
            links += `
                <li><a href="/soporte">Soporte Técnico</a></li>
                <li><a href="/version_freemium">Impresión</a></li>
                <li><a href="/software">Información</a></li>
                <li><a href="/catalogo">Subscripciones</a></li>
            `;
        } else if (userRole === "user") {
            links += `
                <li><a href="/soporte">Soporte Técnico</a></li>
                <li><a href="/user/catalogo">Subscripciones</a></li>
                <li><a href="/impresion">Impresión</a></li>
                <li><a href="/user/software">Información</a></li>
            `;
        } else if (userRole === "PremiumUser") {
            links += `
                <li><a href="/soporte">Soporte Técnico</a></li>
                <li><a href="/user_panel_control">Documentos</a></li>
                <li><a href="/version_freemium">Impresión</a></li>
                <li><a href="/informes">Historial</a></li>
                <li><a href="/software">Información</a></li>
            `;
        } else if (userRole === "Admin") {
            links += `
                <li><a href="/gestion_inventarios">Gestión Inventarios</a></li>
                <li><a href="/panel_control">Gestión Redes Clientes</a></li>
                <li><a href="/gestion_software">Gestión Software</a></li>
                <li><a href="/informe_seguridad">Informe de Seguridad</a></li>
                <li><a href="/modulo_contable">Módulo Contable</a></li>
            `;
        }

        // Agregar la opción de cerrar sesión para usuarios autenticados
        links += `
            <li class="dropdown">
                <a href="#" class="dropbtn">${userName} <span class="caret">▼</span></a>
                <div class="dropdown-content">
                    <a href="/InfoUsuario">Info Usuario</a>
                    <a href="/canjear">Canjear Código</a>
                    <a href="#" onclick="logout()">Cerrar Sesión</a>
                </div>
            </li>
        `;

        // Insertar los enlaces en el Navbar
        navLinks.innerHTML = links;

    } catch (error) {
        console.error("Error al verificar el token:", error);
        // Si ocurre un error, redirigir al login
        navLinks.innerHTML = `
            <li><a href="/">Inicio</a></li>
            <li><a href="/login">Iniciar Sesión</a></li>
        `;
    }
});

// Función para cerrar sesión
function logout() {
    localStorage.removeItem("authToken"); // Eliminar el token del almacenamiento local
    window.location.href = "/login"; // Redirigir al login
}
