// script.js
const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.17.359/pdf.worker.min.js';

const pdfCanvas = document.getElementById('pdf-canvas');
const canvasContext = pdfCanvas.getContext('2d');
const fileInput = document.getElementById('file-input');
const prevPageButton = document.getElementById('prev-page');
const nextPageButton = document.getElementById('next-page');
const zoomInButton = document.getElementById('zoom-in');
const zoomOutButton = document.getElementById('zoom-out');
const pageInfo = document.getElementById('page-info');

let pdfDoc = null;
let currentPage = 1;
let scale = 1.5;

function renderPage(pageNumber) {
    pdfDoc.getPage(pageNumber).then(page => {
        const viewport = page.getViewport({ scale });
        pdfCanvas.width = viewport.width;
        pdfCanvas.height = viewport.height;

        const renderContext = {
            canvasContext,
            viewport,
        };
        page.render(renderContext);
        pageInfo.textContent = `Página ${currentPage} de ${pdfDoc.numPages}`;
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage === pdfDoc.numPages;
    });
}

function renderPDF(file) {
    const reader = new FileReader();
    reader.onload = function (event) {
        const pdfData = new Uint8Array(event.target.result);
        pdfjsLib.getDocument({ data: pdfData }).promise.then(doc => {
            pdfDoc = doc;
            currentPage = 1;
            renderPage(currentPage);
            zoomInButton.disabled = false;
            zoomOutButton.disabled = false;
        }).catch(err => {
            console.error("Error al cargar el PDF:", err);
        });
    };
    reader.readAsArrayBuffer(file);
}

fileInput.addEventListener('change', event => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
        renderPDF(file);
    } else {
        alert("Por favor, selecciona un archivo PDF válido.");
    }
});

prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderPage(currentPage);
    }
});

nextPageButton.addEventListener('click', () => {
    if (currentPage < pdfDoc.numPages) {
        currentPage++;
        renderPage(currentPage);
    }
});

zoomInButton.addEventListener('click', () => {
    scale += 0.2;
    renderPage(currentPage);
});

zoomOutButton.addEventListener('click', () => {
    if (scale > 0.4) {
        scale -= 0.2;
        renderPage(currentPage);
    }
});
