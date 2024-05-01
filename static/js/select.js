const select = document.querySelectorAll(".select");

//ELEMENTOS ORIGINALES
const originalOptions = {};

//ELEMENTOS SELECCIONADOS
const selectedOption = {};

// FUNCIONALIDAD DEL BOTON SELECT | MOSTRAR Y OCULTAR
addEventListener("click", (e) => {
    if (e.target.matches(".select")) {
        e.target.classList.toggle("show-select");
    }
})

addEventListener("focusout", (e) => {
    const element = e.target.closest(".select");
    if ((element !== null) && element.classList.contains("show-select")) {
        if (!element.contains(e.relatedTarget)) {
            element.classList.toggle("show-select");
        }
    }
})

select.forEach(select => {
    originalOptions[select.id] = [];
    selectedOption[select.id] = [];
    
    const options = select.querySelectorAll(".option");
    options.forEach(option => {
        option.onclick = () => {
            select.querySelector(".select-element").value = option.textContent.trim();
            select.classList.toggle("show-select");
        }

        originalOptions[select.id].push(option.textContent.trim());
    });
})

//ACTIVAR SELECCION MULTIPLE EN LOS SELECTBOX
const activeMultiple = (select, busq) => {
    options = select.querySelectorAll(".option");
    options.forEach(e => {
        e.onclick = () => {
            if (!selectedOption[select.id].includes(e.textContent.trim())) {
                selectedOption[select.id].push(e.textContent.trim());
                e.classList.toggle("selected-option");

                //AGREGAR AL INPUT
                select.querySelector(".select-element").value = selectedOption[select.id].join(" - ");
            }
            else{
                selectedOption[select.id] = selectedOption[select.id].filter(item =>  item !== e.textContent.trim());
                e.classList.toggle("selected-option");

                // ELIMINAR DEL INPUT 
                select.querySelector(".select-element").value = selectedOption[select.id].join(" - ");
            }
        }
    });
};

// COMPROBAR SELECCION MULTIPLE EN SELECTBOX
select.forEach(select => {
    if(select.classList.contains("select-multiple")){
        activeMultiple(select, false);
    }
});

//BUSQUEDA
select.forEach(select => {
    const buscador = select.querySelector(".select-search");
    if (buscador) {
        buscador.onkeyup = () => {
            const busq = originalOptions[select.id].filter((e) => {
                const elementSearch = select.querySelector(".select-search");
                const cadena = elementSearch.value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
                return e.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().match(`.*${cadena}.*`);
            });

            //LISTAR ELEMENTOS
            const elementOptions = select.querySelector(".group-options");
            elementOptions.innerHTML = "";

            if(busq.length === 0){
                const div = document.createElement("div");
                div.style.display = "flex";
                div.style.justifyContent = "center";
                div.innerHTML = "No hay resultados!";
                elementOptions.innerHTML = div.outerHTML;
            }
            else if (busq.length >= 0){
                busq.forEach(e => {
                    const div = document.createElement("div");
                    div.classList.add("option");
                    div.innerHTML = e;
                    if (selectedOption[select.id].includes(e)) {
                        div.classList.add("selected-option");
                    }
                    elementOptions.innerHTML += div.outerHTML;
                });
            } 
            else {
                originalOptions[select.id].forEach(e => {
                    const div = document.createElement("div");
                    div.classList.add("option");
                    div.innerHTML = e;
                    elementOptions.innerHTML += div.outerHTML;
                });
            }

            if(select.classList.contains("select-multiple")){
                activeMultiple(select, true);
            }
            else{
                const options = select.querySelectorAll(".option");
                options.forEach(option => {
                    option.onclick = () => {
                        select.querySelector(".select-element").value = option.textContent.trim();
                        select.classList.toggle("show-select");
                    }
                });
            }
        };
    }
});

const updateOptionsSelect = () => {
    select.forEach( e => {
        options = e.querySelectorAll(".selected-option");
        selectedOption[e.id] = Array.from(options).map( e => e.textContent.trim())
    });
};