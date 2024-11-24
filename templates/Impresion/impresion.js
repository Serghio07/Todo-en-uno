const fileUpload = document.getElementById("fileUpload");
const printDate = document.getElementById("printDate");
const copies = document.getElementById("copies");
const color = document.getElementById("color");

const filePreview = document.getElementById("filePreview");
const datePreview = document.getElementById("datePreview");
const copiesPreview = document.getElementById("copiesPreview");
const colorPreview = document.getElementById("colorPreview");
const costPreview = document.getElementById("costPreview");

const printHistoryTable = document.querySelector("#printHistory table tbody");
const paperSize = document.getElementById("paperSize");
const paperType = document.getElementById("paperType");

// Vista previa de las opciones seleccionadas
function updatePreview() {
    filePreview.textContent = fileUpload.files.length > 0 ? fileUpload.files[0].name : "Ninguno";
    datePreview.textContent = printDate.value ? printDate.value : "No seleccionada";
    copiesPreview.textContent = copies.value;
    colorPreview.textContent = color.options[color.selectedIndex].text;
}

// Previsualización del documento
function updateDocumentPreview() {
    const file = fileUpload.files[0];

    if (file) {
        const fileType = file.type;
        const fileURL = URL.createObjectURL(file);
        const pdfPreview = document.getElementById("pdfPreview");
        const imgPreview = document.getElementById("imgPreview");
        const previewMessage = document.getElementById("previewMessage");

        // Ocultar todas las vistas previas
        pdfPreview.style.display = "none";
        imgPreview.style.display = "none";
        previewMessage.style.display = "none";

        if (fileType === "application/pdf") {
            pdfPreview.src = fileURL;
            pdfPreview.style.display = "block";
        } else if (fileType.startsWith("image/")) {
            imgPreview.src = fileURL;
            imgPreview.style.display = "block";
        } else if (fileType === "text/plain" || file.name.endsWith(".docx")) {
            previewMessage.textContent = `Previsualización no disponible para ${file.name}. Descárgalo para visualizarlo.`;
            previewMessage.style.display = "block";
        } else {
            previewMessage.textContent = "Tipo de archivo no compatible para previsualización.";
            previewMessage.style.display = "block";
        }
    } else {
        pdfPreview.style.display = "none";
        imgPreview.style.display = "none";
        previewMessage.textContent = "No se ha seleccionado ningún archivo.";
        previewMessage.style.display = "block";
    }
}

// Actualizar el costo estimado
function updateCost() {
    const colorOption = color.value;
    const copiesCount = parseInt(copies.value);
    const costPerCopy = colorOption === "color" ? 1 : 0.5;
    const estimatedCost = (copiesCount * costPerCopy).toFixed(2);
    costPreview.textContent = `Bs ${estimatedCost}`;
}

// Agregar fila al historial
function addHistoryRow(fileName, date, copies, color) {
    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${fileName}</td>
        <td>${date}</td>
        <td>${copies}</td>
        <td>${color}</td>
        <td><button class="edit-btn" data-id="${fileName}">Editar</button></td>
        <td><button class="delete-btn">Eliminar</button></td>
    `;

    // Evento para editar
    row.querySelector(".edit-btn").addEventListener("click", function(event) {
        const docId = event.target.getAttribute("data-id");
        const row = event.target.closest("tr");
        const docName = row.cells[0].textContent;
        const docColor = row.cells[3].textContent;
        const docDate = row.cells[1].textContent;
        const docCopies = row.cells[2].textContent;

        // Mostrar modal y llenar campos
        document.getElementById("docName").value = docName;
        document.getElementById("docColor").value = docColor;
        document.getElementById("docDate").value = docDate;
        document.getElementById("docCopies").value = docCopies;

        const modal = document.getElementById("editModal");
        modal.style.display = "block";

        // Cerrar modal
        document.querySelector(".close-btn").addEventListener("click", () => {
            modal.style.display = "none";
        });

        // Enviar los cambios
        document.getElementById("editForm").addEventListener("submit", function(e) {
            e.preventDefault();

            // Actualizar en la tabla
            row.cells[0].textContent = document.getElementById("docName").value;
            row.cells[1].textContent = document.getElementById("docDate").value;
            row.cells[2].textContent = document.getElementById("docCopies").value;
            row.cells[3].textContent = document.getElementById("docColor").value;

            modal.style.display = "none";
            alert("Documento actualizado.");
        });
    });

    // Evento para eliminar
    row.querySelector(".delete-btn").addEventListener("click", function(event) {
        const row = event.target.closest("tr");
        row.remove();
        alert("Documento eliminado.");
    });

    printHistoryTable.appendChild(row);
}

// Enviar formulario de impresión
document.getElementById("printForm").addEventListener("submit", (event) => {
    event.preventDefault();

    const fileName = fileUpload.files[0]?.name || "Ninguno";
    const date = printDate.value || "No seleccionada";
    const copiesCount = copies.value || "1";
    const colorText = color.options[color.selectedIndex].text;

    addHistoryRow(fileName, date, copiesCount, colorText);

    alert("Impresión programada correctamente.");
});

// Opciones avanzadas
document.getElementById("advancedOptions").addEventListener("change", () => {
    console.log("Opciones avanzadas actualizadas: ", {
        paperSize: paperSize.value,
        paperType: paperType.value
    });
});

// Eventos para actualizar vista previa y costo
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

// Agregar eventos de cancelación a los botones
document.querySelectorAll(".cancel-btn").forEach((button) => {
    button.addEventListener("click", (event) => {
        const row = event.target.closest("tr");
        row.remove();
        alert("El documento ha sido cancelado.");
    });
});
