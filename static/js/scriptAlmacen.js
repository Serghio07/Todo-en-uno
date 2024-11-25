document.addEventListener("DOMContentLoaded", () => {
    fetchArchivos();
});

// Función para obtener archivos desde el servidor
function fetchArchivos() {
    fetch('/api/archivos')
        .then(response => response.json())
        .then(data => renderArchivos(data))
        .catch(error => console.error('Error al obtener archivos:', error));
}

// Función para renderizar archivos en la tabla
function renderArchivos(archivos) {
    const tableBody = document.querySelector("table tbody");
    tableBody.innerHTML = ""; // Limpiar la tabla

    if (archivos.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="7" class="text-center">No se encontraron archivos</td></tr>`;
        return;
    }

    archivos.forEach(archivo => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${archivo[0]}</td>
            <td>${archivo[1]}</td>
            <td>${archivo[2]}</td>
            <td>${(archivo[3] / 1024).toFixed(2)} KB</td>
            <td>${archivo[4]}</td>
            <td>${archivo[5]}</td>
            <td>
                <button onclick="descargarArchivo('${archivo[1]}')" class="btn btn-info">Descargar</button>
                <button onclick="eliminarArchivo(${archivo[0]})" class="btn btn-danger">Eliminar</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Función para subir un archivo
document.querySelector(".form-upload").addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    fetch('/api/archivo', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchArchivos();
        })
        .catch(error => console.error('Error al subir archivo:', error));
});

// Función para eliminar un archivo
function eliminarArchivo(id) {
    if (!confirm("¿Estás seguro de eliminar este archivo?")) return;

    fetch(`/api/archivo/${id}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchArchivos();
        })
        .catch(error => console.error('Error al eliminar archivo:', error));
}
