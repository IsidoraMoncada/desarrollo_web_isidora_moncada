const validarlistado = () => {
    window.location.href = "./listado.html";  
};

const validarmenu = () => {
    window.location.href = "./index.html";  
};

const validarimagen = () => {
  
    //Creamos el elemento imagen que contiene las características solicitadas por eneunciado y un contenedor en donde pondremos la imagen
    let abririmagen = document.createElement("img");
    abririmagen.id = "imagengrande"
    abririmagen.src = "../images/plantas.jpg";
  
    abririmagen.style.width = "600px"; 
    abririmagen.style.height = "800px"; 
    abririmagen.style.objectFit = "contain";

    let contenedorImagen = document.createElement("div");
    let cerrarImagen = document.createElement("button");

    contenedorImagen.id = "nuevodiv"
    contenedorImagen.style.position = "fixed";
    contenedorImagen.style.top = "0";
    contenedorImagen.style.left = "0";
    contenedorImagen.style.width = "100%";
    contenedorImagen.style.height = "100%";
    contenedorImagen.style.display = "flex";
    contenedorImagen.style.justifyContent = "center";

    cerrarImagen.textContent = "Cerrar";
    cerrarImagen.style.position = "absolute";
    cerrarImagen.style.top = "20px"; 
    cerrarImagen.style.right = "20px"; 
    cerrarImagen.style.padding = "10px 20px";
    cerrarImagen.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    cerrarImagen.style.color = "white"; 
    cerrarImagen.style.border = "none";
    cerrarImagen.style.borderRadius = "5px";
    cerrarImagen.style.cursor = "pointer";
  
  
    //Tomamos los elementos necesarios para poner la imagen
    let pagina = document.querySelector(".main-container");
  
    //Agregamos la imagen al contenedor que creamos para ella
    contenedorImagen.appendChild(abririmagen)
    contenedorImagen.appendChild(cerrarImagen)

    //Ahora situamos el contenedor con la imagen en main-container
    pagina.appendChild(contenedorImagen);
  
    // Agregamos un evento para cerrar la imagen que fue agrandada
    cerrarImagen.addEventListener("click", () => {
      pagina.removeChild(contenedorImagen);
    });
  }
  
let submitBtn1 = document.getElementById("listado");
submitBtn1.addEventListener("click", validarlistado);

let submitBtn2 = document.getElementById("menu");
submitBtn2.addEventListener("click", validarmenu);

let submitBtn3 = document.getElementById("imagen");
submitBtn3.addEventListener("click", validarimagen);