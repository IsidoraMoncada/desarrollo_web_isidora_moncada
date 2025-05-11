const validaragregar = () => {
    window.location.href = "./formulario.html";  
};

const validarlistado = () => {
    window.location.href = "./listado.html";
};

const validarestadisticas = () => {
    window.location.href = "./estadisticas.html";
};
  
let submitBtn1 = document.getElementById("agregar");
submitBtn1.addEventListener("click", validaragregar);

let submitBtn2 = document.getElementById("listado");
 submitBtn2.addEventListener("click", validarlistado);

 let submitBtn3 = document.getElementById("estadisticas");
 submitBtn3.addEventListener("click", validarestadisticas);