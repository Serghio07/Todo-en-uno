// app.js
document.addEventListener("DOMContentLoaded", () => {
    // Inicializa TinyMCE
    tinymce.init({
      selector: "#editor",
      plugins: "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table code help wordcount",
      toolbar: "undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat",
      height: 400
    });
  
    const uploadInput = document.getElementById("upload-docx");
    const downloadButton = document.getElementById("download-docx");
  
    let zip; // Variable para almacenar el archivo cargado
  
    // Cargar archivo DOCX y mostrar contenido
    uploadInput.addEventListener("change", async (event) => {
      const file = event.target.files[0];
      if (file && file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        const reader = new FileReader();
        reader.onload = (e) => {
          zip = new PizZip(e.target.result); // Carga el contenido del archivo
          const doc = new docxtemplater().loadZip(zip);
          const text = doc.getFullText(); // Extrae el texto
          tinymce.get("editor").setContent(text); // Carga el texto al editor
        };
        reader.readAsArrayBuffer(file);
      } else {
        alert("Por favor, selecciona un archivo DOCX válido.");
      }
    });
  
    // Descargar el contenido del editor como DOCX
    downloadButton.addEventListener("click", () => {
      if (!zip) {
        alert("Primero carga un archivo DOCX para editar.");
        return;
      }
  
      const editorContent = tinymce.get("editor").getContent(); // Obtiene el contenido del editor
      const doc = new docxtemplater().loadZip(zip);
      doc.setData({ content: editorContent }); // Establece el contenido editado
  
      try {
        doc.render(); // Genera el archivo final
        const output = doc.getZip().generate({ type: "blob" });
        saveAs(output, "documento-editado.docx"); // Guarda el archivo
      } catch (error) {
        console.error("Error al generar el archivo DOCX:", error);
        alert("Ocurrió un error al generar el archivo DOCX.");
      }
    });
  });
  