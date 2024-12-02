// Función para subir archivos
document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];

    if (!file) {
        alert("Por favor, selecciona un archivo para subir.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const token = localStorage.getItem("authToken");
    if (!token) {
        alert("No estás autenticado. Por favor, inicia sesión.");
        return;
    }

    try {
        const response = await fetch("/almacen/archivo", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}` // Incluir el token en el encabezado
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error("Error al subir el archivo");
        }

        const data = await response.json();
        alert("Archivo subido con éxito.");
        window.location.reload();
    } catch (error) {
        console.error("Error:", error);
        alert("Error al subir el archivo. Intenta nuevamente.");
    }
});

// Función para cargar archivos del usuario
async function loadFiles() {
    const tableBody = document.querySelector("table tbody");
    console.log("Elemento tableBody encontrado:", tableBody); // LOG: Verificar el elemento

    if (!tableBody) {
        console.error("Error: No se encontró el elemento <tbody> en la tabla.");
        return; // Salir de la función si no se encuentra el elemento
    }

    try {
        const response = await fetch("/almacen/archivos", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("authToken")}`
            }
        });

        if (!response.ok) {
            throw new Error("Error al obtener los archivos del servidor");
        }

        const data = await response.json();
        console.log("Datos obtenidos del servidor:", data); // LOG: Verificar los datos obtenidos

        tableBody.innerHTML = ""; // Limpiar el contenido anterior

        data.forEach((archivo) => {
            console.log("Procesando archivo:", archivo); // LOG: Verificar cada archivo procesado

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${archivo.id}</td>
                <td>${archivo.nombre}</td>
                <td>${archivo.tipo}</td>
                <td>${(archivo.tamano / 1024).toFixed(2)} KB</td>
                <td><a href="/uploads/${archivo.ruta}" target="_blank">Ver archivo</a></td>
                <td>${archivo.fecha_subida}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteFile(${archivo.id})">Eliminar</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error al cargar los archivos:", error); // LOG: Mostrar errores
    }
}


// Función para buscar archivos por nombre
async function searchFile() {
    const searchInput = document.getElementById("searchInput").value;
    const token = localStorage.getItem("authToken");

    if (!token) {
        alert("No estás autenticado. Por favor, inicia sesión.");
        return;
    }

    try {
        const response = await fetch(`/almacen/buscar_archivo?nombre=${searchInput}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Error al buscar el archivo.");
        }

        const archivo = await response.json();
        const filesTable = document.getElementById("filesTable");
        filesTable.innerHTML = ""; // Limpiar la tabla

        const row = `
            <tr>
                <td>${archivo.id}</td>
                <td>${archivo.nombre}</td>
                <td>${archivo.tipo}</td>
                <td>${(archivo.tamano / 1024).toFixed(2)} KB</td>
                <td><a href="/almacen/download/${archivo.nombre}" target="_blank">Ver</a></td>
                <td>${archivo.fecha}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteFile(${archivo.id})">Eliminar</button>
                </td>
            </tr>
        `;
        filesTable.innerHTML = row;
    } catch (error) {
        console.error("Error al buscar el archivo:", error);
        alert("Archivo no encontrado o error al buscar. Intenta nuevamente.");
    }
}

// Función para eliminar un archivo
async function deleteFile(fileId) {
    const token = localStorage.getItem("authToken");

    if (!token) {
        alert("No estás autenticado. Por favor, inicia sesión.");
        return;
    }

    try {
        const response = await fetch(`/almacen/archivo/delete/${fileId}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Error al eliminar el archivo.");
        }

        alert("Archivo eliminado con éxito.");
        window.location.reload();
    } catch (error) {
        console.error("Error al eliminar el archivo:", error);
        alert("Error al eliminar el archivo. Intenta nuevamente.");
    }
}

// Cargar los archivos al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM completamente cargado y procesado."); // LOG: Verificar carga del DOM
    loadFiles(); // Llamar a la función después de la carga del DOM
});
