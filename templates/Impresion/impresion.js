const fileUpload = document.getElementById("fileUpload");
const printDate = document.getElementById("printDate");
const copies = document.getElementById("copies");
const color = document.getElementById("color");

const filePreview = document.getElementById("filePreview");
const datePreview = document.getElementById("datePreview");
const copiesPreview = document.getElementById("copiesPreview");
const colorPreview = document.getElementById("colorPreview");
const costPreview = document.getElementById("costPreview");

const pdfPreview = document.getElementById("pdfPreview");
const previewMessage = document.getElementById("previewMessage");

// Función para actualizar la vista previa de las opciones seleccionadas
function updatePreview() {
    filePreview.textContent = fileUpload.files.length > 0 ? fileUpload.files[0].name : "Ninguno";
    datePreview.textContent = printDate.value ? printDate.value : "No seleccionada";
    copiesPreview.textContent = copies.value;
    colorPreview.textContent = color.options[color.selectedIndex].text;
}

// Función para previsualizar el documento si es PDF
function updateDocumentPreview() {
    const file = fileUpload.files[0];
    
    if (file) {
        const fileType = file.type;

        if (fileType === "application/pdf") {
            const fileURL = URL.createObjectURL(file);
            pdfPreview.src = fileURL;
            pdfPreview.style.display = "block";
            previewMessage.style.display = "none";
        } else {
            pdfPreview.style.display = "none";
            previewMessage.textContent = "Previsualización no disponible para este archivo. Solo archivos PDF son compatibles.";
            previewMessage.style.display = "block";
        }
    } else {
        pdfPreview.style.display = "none";
        previewMessage.style.display = "block";
    }
}

// Función para actualizar el costo estimado
function updateCost() {
    const colorOption = color.value;
    const copiesCount = parseInt(copies.value);
    const costPerCopy = colorOption === "color" ? 1 : 0.5;
    const estimatedCost = (copiesCount * costPerCopy).toFixed(2);
    costPreview.textContent = `Bs ${estimatedCost}`;
}

// Eventos para actualizar vista previa y costo cuando se cambia el valor de algún campo
fileUpload.addEventListener("change", () => {
    updatePreview();
    updateDocumentPreview();
});
printDate.addEventListener("input", updatePreview);
copies.addEventListener("input", () => {
    updatePreview();
    updateCost();
});
color.addEventListener("change", () => {
    updatePreview();
    updateCost();
});
