document.addEventListener("DOMContentLoaded", () => {
    // Solo mantener funciones de eliminación y búsqueda, ya que la carga de archivos es manejada por Flask
    document.querySelector(".btn-search").addEventListener("click", buscarArchivo);
});

function buscarArchivo() {
    console.log("Botón de búsqueda clickeado."); // Debug
    const searchQuery = document.querySelector("#searchInput").value.trim();

    if (!searchQuery) {
        alert("Por favor, ingrese un término de búsqueda.");
        return;
    }

    fetch(`/buscar_archivo?nombre=${encodeURIComponent(searchQuery)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Archivo no encontrado.");
            }
            return response.json();
        })
        .then(data => {
            renderArchivos([data]);
        })
        .catch(error => alert(error.message));
}

function eliminarArchivo(id) {
    if (!confirm("¿Estás seguro de eliminar este archivo?")) return;

    fetch(`/archivo/delete/${id}`, {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();  // Recargar la página para reflejar el cambio
        })
        .catch(error => console.error('Error al eliminar archivo:', error));
}
