document.getElementById("printForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append("documento", document.getElementById("documento").files[0]);
    formData.append("fecha", document.getElementById("fecha").value);
    formData.append("copias", document.getElementById("copias").value);
    formData.append("color", document.getElementById("color").value);

    fetch("URL_DEL_MICROSERVICIO_DE_IMPRESION/schedulePrint", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("responseMessage").textContent = data.message;
    })
    .catch(error => {
        console.error("Error al programar la impresión:", error);
        document.getElementById("responseMessage").textContent = "Hubo un error al programar la impresión.";
    });
});
