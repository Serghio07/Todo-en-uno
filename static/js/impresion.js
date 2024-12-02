document.addEventListener("DOMContentLoaded", () => {
    loadDocuments();
});

// Función para cargar los documentos disponibles
async function loadDocuments() {
    const tableBody = document.querySelector("#documentosTable tbody");
    if (!tableBody) {
        console.error("No se encontró el cuerpo de la tabla para los documentos.");
        return;
    }

    try {
        const response = await fetch("/impresion/documentos", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("authToken")}`
            }
        });

        if (!response.ok) {
            throw new Error("Error al obtener los documentos del servidor.");
        }

        const documentos = await response.json();
        tableBody.innerHTML = "";

        documentos.forEach((doc) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${doc.id}</td>
                <td>${doc.titulo}</td>
                <td>${doc.tipo}</td>
                <td>${doc.fecha_creacion}</td>
                <td>
                    <button class="btn btn-primary" onclick="selectDocument(${doc.id})">Seleccionar</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error al cargar los documentos:", error);
    }
}

// Función para programar una impresión
async function programPrint() {
    const documentoId = document.getElementById("documentoSelect").value;
    const fechaProgramada = document.getElementById("fechaProgramada").value;
    const estado = document.getElementById("estadoSelect").value;
    const numeroCopias = document.getElementById("numeroCopias").value;

    const payload = {
        documento_id: documentoId,
        fecha_programada: fechaProgramada,
        estado: estado,
        numero_copias: numeroCopias
    };

    try {
        const response = await fetch("/impresion/programar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("authToken")}`
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Error al programar la impresión.");
        }

        alert("Impresión programada exitosamente.");
        window.location.reload();
    } catch (error) {
        console.error("Error al programar la impresión:", error);
        alert("Error al programar la impresión. Intenta nuevamente.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadDocuments();
});

async function loadDocuments() {
    const tableBody = document.getElementById("documentosBody");

    try {
        const response = await fetch("/impresion/documentos", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("authToken")}`,
            },
        });

        if (!response.ok) throw new Error("Error al obtener los documentos");

        const documentos = await response.json();
        tableBody.innerHTML = "";

        documentos.forEach((doc) => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${doc.id}</td>
                <td>${doc.titulo}</td>
                <td>${doc.tipo}</td>
                <td>${new Date(doc.fecha_creacion).toLocaleString()}</td>
                <td>
                    <button onclick="seleccionarDocumento(${doc.id}, '${doc.titulo}')">Seleccionar</button>
                </td>
            `;

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error al cargar los documentos:", error);
    }
}

function seleccionarDocumento(id, titulo) {
    const selectDocumento = document.getElementById("documento");
    const option = document.createElement("option");
    option.value = id;
    option.textContent = titulo;
    option.selected = true;

    selectDocumento.innerHTML = ""; // Limpiar opciones previas
    selectDocumento.appendChild(option);
}

document.getElementById("formImpresion").addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("authToken");
    if (!token) {
        alert("No estás autenticado. Por favor, inicia sesión.");
        return;
    }

    const formData = new FormData(e.target);

    try {
        const response = await fetch("/impresion/guardar_impresion", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Error al guardar la impresión");
        }

        alert("Impresión guardada exitosamente.");
        e.target.reset(); // Limpiar el formulario
    } catch (error) {
        console.error("Error al guardar la impresión:", error);
        alert("Error al guardar la impresión. Intenta nuevamente.");
    }
});
