//VARIABLES ANIME
const section = document.querySelector(".elements .container-fluid");
const template = document.querySelector(".template-elements").content;
const fragmentAnime = document.createDocumentFragment();

const pagina = document.querySelectorAll(".pagina");

const changePageAnime = async (object) => {
    try{
        const data = {};
        data["start"] = parseInt(object.dataset.start);

        const res = await fetch("/animes/selectAll", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        });
        const json = await res.json();

        section.innerHTML = "";
        json.forEach(e => {
            template.querySelector("a").href = "/animes/" + e.titulo;
            template.querySelector(".card-img").src = e.portada;
            template.querySelector(".card-title").innerHTML = e.titulo;
            template.querySelector(".card-descrip").innerHTML = e.sipnosis;

            const clone = document.importNode(template, true);
            fragmentAnime.appendChild(clone);
        });
        section.appendChild(fragmentAnime);

        //EFECTO DE CAMBIO
        pagina.forEach(page => {
            if(page.classList.contains("page-disabled")){
                page.classList.toggle("page-disabled");
                page.disabled = "";
            }
        });
        object.classList.toggle("page-disabled");
        object.disabled = "disabled";

    } catch(err){
        console.log(err);
    }
}

const changePageManga = async (object) => {
    try{
        const data = {};
        data["start"] = parseInt(object.dataset.start);

        const res = await fetch("/mangas/selectAll", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        });
        const json = await res.json();

        section.innerHTML = "";
        json.forEach(e => {
            template.querySelector("a").href = "/mangas/" + e.titulo;
            template.querySelector(".card-img").src = e.portada;
            template.querySelector(".card-title").innerHTML = e.titulo;
            template.querySelector(".card-descrip").innerHTML = e.sipnosis;

            const clone = document.importNode(template, true);
            fragmentAnime.appendChild(clone);
        });
        section.appendChild(fragmentAnime);

        //EFECTO DE CAMBIO
        pagina.forEach(page => {
            if(page.classList.contains("page-disabled")){
                page.classList.toggle("page-disabled");
                page.disabled = "";
            }
        });
        object.classList.toggle("page-disabled");
        object.disabled = "disabled";

    } catch(err){
        console.log(err);
    }
}

const changePageNovela = async (object) => {
    try{
        const data = {};
        data["start"] = parseInt(object.dataset.start);

        const res = await fetch("/novelas/selectAll", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        });
        const json = await res.json();

        section.innerHTML = "";
        json.forEach(e => {
            template.querySelector("a").href = "/novelas/" + e.titulo;
            template.querySelector(".card-img").src = e.portada;
            template.querySelector(".card-title").innerHTML = e.titulo;
            template.querySelector(".card-descrip").innerHTML = e.sipnosis;

            const clone = document.importNode(template, true);
            fragmentAnime.appendChild(clone);
        });
        section.appendChild(fragmentAnime);

        //EFECTO DE CAMBIO
        pagina.forEach(page => {
            if(page.classList.contains("page-disabled")){
                page.classList.toggle("page-disabled");
                page.disabled = "";
            }
        });
        object.classList.toggle("page-disabled");
        object.disabled = "disabled";

    } catch(err){
        console.log(err);
    }
}

//BUSQUEDA
const changePageS = async (object) => {
    try{
        const data = {};
        data["start"] = parseInt(object.dataset.start);
        data["articulo"] = object.dataset.busq;

        const res = await fetch("/search/select", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        });
        const json = await res.json();

        section.innerHTML = "";
        json.forEach(e => {
            if(e.tipo === "anime"){
                template.querySelector("a").href = "/animes/" + e.titulo;
            }
            else if(e.tipo === "manga"){
                template.querySelector("a").href = "/mangas/" + e.titulo;
            }
            else{
                template.querySelector("a").href = "/novelas/" + e.titulo;
            }
            template.querySelector(".card-img").src = e.portada;
            template.querySelector(".card-title").innerHTML = e.titulo;
            template.querySelector(".card-descrip").innerHTML = e.sipnosis;

            const clone = document.importNode(template, true);
            fragmentAnime.appendChild(clone);
        });
        section.appendChild(fragmentAnime);

        //EFECTO DE CAMBIO
        pagina.forEach(page => {
            if(page.classList.contains("page-disabled")){
                page.classList.toggle("page-disabled");
                page.disabled = "";
            }
        });
        object.classList.toggle("page-disabled");
        object.disabled = "disabled";

    } catch(err){
        console.log(err);
    }
}