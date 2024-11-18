// Función para subir un archivo
function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        alert("Por favor selecciona un archivo");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fileInput.value = '';  // Limpiar el input de archivo
    })
    .catch(error => {
        alert('Error al subir el archivo: ' + error);
    });
}

// Función para listar los archivos
function listFiles() {
    fetch('/files')
    .then(response => response.json())
    .then(data => {
        const fileList = document.getElementById('file-list');
        fileList.innerHTML = '';

        data.forEach(file => {
            const listItem = document.createElement('li');
            listItem.textContent = `Archivo: ${file.name} - Última Modificación: ${new Date(file.updated).toLocaleString()}`;
            fileList.appendChild(listItem);
        });
    })
    .catch(error => {
        alert('Error al listar los archivos: ' + error);
    });
}

// Función para descargar un archivo
function downloadFile() {
    const fileName = document.getElementById('download-input').value;

    if (!fileName) {
        alert("Por favor ingresa el nombre del archivo");
        return;
    }

    fetch(`/download/${fileName}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Archivo no encontrado');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        alert('Error al descargar el archivo: ' + error);
    });
}

