// Configuración de Quill con la barra de herramientas personalizada
const quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
      toolbar: [
        [{ header: [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['link', 'image'],
        [{ align: [] }],
        [{ color: [] }, { background: [] }],
        ['clean']
      ]
    }
  });
  
  // Función para "descargar" el contenido como archivo HTML
  function saveContent() {
    const content = quill.root.innerHTML;
    const blob = new Blob([content], { type: 'text/html' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'documento.html';
    link.click();
    URL.revokeObjectURL(link.href);
  }
  
  // Función para cargar un archivo HTML y mostrarlo en el editor
  function uploadContent(event) {
    const file = event.target.files[0];
    if (file && file.type === 'text/html') {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        quill.root.innerHTML = content;
      };
      reader.readAsText(file);
    } else {
      alert("Por favor, selecciona un archivo HTML válido.");
    }
  }
  