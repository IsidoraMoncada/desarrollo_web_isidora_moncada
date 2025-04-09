const validateRegion = (region) => {
    if(!region) return false;
    return true
};

const validateComuna = (comuna) => {
    if(!comuna) return false;
    return true
};

const validateSector = (sector) => {
    if(!sector) return true;
    let lengthValidsi = sector.trim().length <= 100;

    return lengthValidsi;
};

const validateName = (name) => {
    if(!name) return false;
    let lengthValidmax = name.trim().length <= 200;
    let lengthValidmin = name.trim().length > 0;
    return lengthValidmax && lengthValidmin;
};

const validateEmail = (email) => {
    if (!email) return false;
    let lengthValid = email.trim().length <= 100;
  
    let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    let formatValid = re.test(email);
  
    return lengthValid && formatValid;
}

const validateNumero = (numero) => {
    if (!numero || numero.trim() == "") return true;
    const re = /^\+\d{3}\.\d{8}$/;

    let formatValid = re.test(numero.trim());
  
    return formatValid
};

const inputOtro = () => {
    let myForm = document.forms["myForm"];
    let otro = myForm["contacto"].value

    let viejoInput = document.getElementById("otroInput");
    if (viejoInput) {
        viejoInput.remove();
    }

    if (otro === "Otra" ){
        let div = document.createElement("div");
        div.id = "otroInput";

        let label = document.createElement("label");
        label.setAttribute("for", "otroInput");
        label.textContent = "Agregue su forma de contacto";

        let input = document.createElement("input");
        input.type = "text";
        input.id = "otroInput";
        input.name = "otroInput";
        input.minLength = 4;
        input.maxLength = 50;
        
        div.appendChild(label);
        div.appendChild(input);

        let contactoSelect = myForm["contacto"];
        contactoSelect.parentNode.insertBefore(div, contactoSelect.nextSibling);
    }
}

const validateContacto = (contacto) => {
    if(!contacto) return true;
    if (contacto != "Otra") return true;

    const validateOtra = (otra) => {
        if (!otra) return false;
        let lengthValidmax = otra.trim().length <= 50;
        let lengthValidmin = otra.trim().length >= 4;

        return lengthValidmax && lengthValidmin
    }

    if (contacto == "Otra"){
        otroInput = document.getElementById("otroInput");
        if (!otroInput) return false; 
        return validateOtra(otroInput.value);
    }
};

const validateInicio = (inicio) => {
    if (!inicio) return false; 

    const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;

    return regex.test(inicio);
};

const validateTermino = (termino, inicio) => {
    if (!termino) return true; 

    const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
    formatValid = regex.test(termino);
    if (!formatValid) return false;

    if (!inicio || !regex.test(inicio)) return false;

    const fechaInicio = new Date(inicio);
    const fechaTermino = new Date(termino);
    return fechaTermino > fechaInicio;
};

const validateDescripcion = (descripcion) => {
    if (!descripcion) return true; 
    let lengthValid = descripcion.trim().length >= 4;
    return lengthValid;
};

const inputTema = () => {
    let myForm = document.forms["myForm"];
    let otro = myForm["tema"].value

    let viejoInput = document.getElementById("otroTema");
    if (viejoInput) {
        viejoInput.remove();
    }

    if (otro === "Otro" ){
        let div = document.createElement("div");
        div.id = "otroTema";

        let label = document.createElement("label");
        label.setAttribute("for", "otroTema");
        label.textContent = "Descripción del tema";

        let input = document.createElement("input");
        input.type = "text";
        input.id = "otroTema";
        input.name = "otroTema";
        input.minLength = 3;
        input.maxLength = 15;
        
        div.appendChild(label);
        div.appendChild(input);

        let temaSelect = myForm["tema"];
        temaSelect.parentNode.insertBefore(div, temaSelect.nextSibling);
    }
}

const validateTema = (tema) => {
    if(!tema) return false;
    if (tema != "Otro") return true;

    const validateOtro = (otro) => {
        if (!otro) return false; 
        let lengthValidmax = otro.trim().length <= 15;
        let lengthValidmin = otro.trim().length >= 3;

        return lengthValidmax && lengthValidmin
    }

    if (tema == "Otro"){
        otroTema = document.getElementById("otroTema");
        if (!otroTema) return false; 

        return validateOtro(otroTema.value);
    }
};

const validatemyForm = () => {

    // obtener elementos del DOM usando el nombre del formulario.
    let myForm = document.forms["myForm"];
    let region = myForm["region"].value;
    let comuna = myForm["comuna"].value;
    let sector = myForm["sector"].value;
    let name = myForm["name"].value;
    let email = myForm["email"].value;
    let numero = myForm["numero"].value;
    let contacto = myForm["contacto"].value;
    let inicio = myForm["inicio"].value;
    let termino = myForm["termino"].value;
    let descripcion = myForm["descripcion"].value;
    let tema = myForm["tema"].value;
    let files = document.getElementById('files');

    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
      invalidInputs.push(inputName);
      isValid &&= false;
    };

    if (!validateRegion(region)) {
        setInvalidInput("Seleccione una region");
    }
    if (!validateComuna(comuna)) {
    setInvalidInput("Seleccione una comuna");
    }
    if (!validateSector(sector)) {
    setInvalidInput("El sector debe ser de máximo 100 carácteres");
    }
    if (!validateName(name)) {
    setInvalidInput("Falta el campo Nombre");
    }
    if (!validateEmail(email)) {
    setInvalidInput("Escriba un email válido");
    }
    if (!validateNumero(numero)) {
    setInvalidInput("Escriba un número válido");
    }
    if (!validateContacto(contacto)) {
    setInvalidInput("La foma de contácto debe ser de mínimo 4 caráctares");
    }
    if (!validateInicio(inicio)) {
    setInvalidInput("Ingrese una fecha de inicio válida");
    }
    if (!validateTermino(termino, inicio)) {
    setInvalidInput("Ingrese una fecha de término válida");
    }
    if (!validateDescripcion(descripcion)) {
        setInvalidInput("Ingrese una descripción de al menos 4 carácteres");
        }
    if (!validateTema(tema)) {
    setInvalidInput("Escriba un tema válido");
    }

      // finalmente mostrar la validación
    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");
    let formContainer = document.querySelector(".main-container");

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
        validationMessageElem.innerText = "¿Está seguro que desea agregar esta actividad?";
        validationListElem.textContent = "";
    
        // aplicar estilos de éxito
        validationBox.style.backgroundColor = "#ddffdd";
        validationBox.style.borderLeftColor = "#4CAF50";

        let submitButton = document.createElement("button");
        submitButton.innerText = "Sí, estoy seguro";
        submitButton.style.marginRight = "10px";
        submitButton.addEventListener("click", () => {
            // establecer mensaje de éxito
            validationMessageElem.innerText = "Hemos recibido su información, muchas gracias y suerte en su actividad";
            validationListElem.textContent = "";
    
            // aplicar estilos de éxito
            validationBox.style.backgroundColor = "#ddffdd";
            validationBox.style.borderLeftColor = "#4CAF50";
            let volver = document.createElement("button");
            volver.innerText = "Volver a la portada";
            volver.style.marginTop = "10px";
            volver.style.marginRight = "10px";
            volver.style.cursor = "pointer";
            volver.style.marginBottom = "10px";
            volver.addEventListener("click", () => {
            window.location.href = "./index.html"; 
            });
            validationBox.appendChild(volver);
        });
    
        let backButton = document.createElement("button");
        backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
        backButton.addEventListener("click", () => {
            // Mostrar el formulario nuevamente
            myForm.style.display = "block";
            validationBox.hidden = true;
        });

        validationListElem.appendChild(submitButton);
        validationListElem.appendChild(backButton);

        // hacer visible el mensaje de validación
        validationBox.hidden = false;

    }
}

window.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('inicio');
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');

    const localDateTime = `${year}-${month}-${day}T${hour}:${minute}`;
    input.value = localDateTime;
});

window.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('termino');
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hour = String(now.getHours()+3).padStart(2, '0');
    const minute = String(now.getMinutes()).padStart(2, '0');

    const localDateTime = `${year}-${month}-${day}T${hour}:${minute}`;
    input.value = localDateTime;
});

let agregarBtn = document.getElementById("envio");
agregarBtn.addEventListener("click", validatemyForm);

