const validarlistado = () => {
    window.location.href = "./listado.html";  
};

const validarmenu = () => {
    window.location.href = "./index.html";  
};

const validarimagen = (elem) => {
  
    let abririmagen = document.createElement("img");
    abririmagen.id = "imagengrande"
    abririmagen.src = elem.src;
  
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
  
  
    let pagina = document.querySelector(".main-container");
  
    contenedorImagen.appendChild(abririmagen)
    contenedorImagen.appendChild(cerrarImagen)

    pagina.appendChild(contenedorImagen);
  
    cerrarImagen.addEventListener("click", () => {
      pagina.removeChild(contenedorImagen);
    });
  }
  
let submitBtn1 = document.getElementById("listado");
submitBtn1.addEventListener("click", validarlistado);

let submitBtn2 = document.getElementById("menu");
submitBtn2.addEventListener("click", validarmenu);

const validateNombre = (name) => {
  if(!name) return false;
  let nameSinEspacios = name.replace(/\s+/g, "");
  let lengthValidmax = nameSinEspacios.length <= 80
  let lengthValidmin = nameSinEspacios.length > 2;
  return lengthValidmax && lengthValidmin;
};

const validateComentario = (comentario) => {
  if(!comentario) return false;
  let comentarioSinEspacios = comentario.replace(/\s+/g, "");
  let lengthValidmin = comentarioSinEspacios.length > 4;
  return lengthValidmin;
};

const validateNuevoComentario = () => {
  let myForm = document.forms["comentarioForm"];
  let nombre = myForm["nombre"].value;
  let comentario = myForm["comentario"].value;

  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  if (!validateNombre(nombre)) {
      setInvalidInput("Escriba un nombre correcto (min 3 carácteres)");
  }
  if (!validateComentario(comentario)) {
    setInvalidInput("Escriba un comentario válido (min 5 carácteres)");
  }
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "El comentario ha sido publicado con éxito";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }
}

let agregarBtn = document.getElementById("botonComentario");
agregarBtn.addEventListener("click", validateNuevoComentario);