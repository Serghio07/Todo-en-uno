// Selección de elementos del formulario y de vista previa
const fileUpload = document.getElementById("fileUpload");
const printDate = document.getElementById("printDate");
const copies = document.getElementById("copies");
const color = document.getElementById("color");

const filePreview = document.getElementById("filePreview");
const datePreview = document.getElementById("datePreview");
const copiesPreview = document.getElementById("copiesPreview");
const colorPreview = document.getElementById("colorPreview");

// Función para actualizar la vista previa
function updatePreview() {
    // Muestra el nombre del archivo cargado
    filePreview.textContent = fileUpload.files.length > 0 ? fileUpload.files[0].name : "Ninguno";
    
    // Muestra la fecha seleccionada
    datePreview.textContent = printDate.value ? printDate.value : "No seleccionada";

    // Muestra el número de copias
    copiesPreview.textContent = copies.value;

    // Muestra el color seleccionado
    colorPreview.textContent = color.options[color.selectedIndex].text;
}

// Eventos que llaman a updatePreview cuando el usuario cambia algo
fileUpload.addEventListener("change", updatePreview);
printDate.addEventListener("input", updatePreview);
copies.addEventListener("input", updatePreview);
color.addEventListener("change", updatePreview);
