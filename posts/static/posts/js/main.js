console.log("El blog cargó correctamente");
const titulo = document.querySelector("h1");
if (titulo) {
    titulo.addEventListener("click", function () {
    alert("Hiciste clic en el título del blog");
    });
}