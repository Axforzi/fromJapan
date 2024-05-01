// CHARGE DATA ON FORM EDIT
const btnEdit = document.querySelectorAll(".btn-edit");

btnEdit.forEach( e => {
e.onclick = async () => {
    const res = await fetch(`/admin/articulos/${e.dataset.id}`)
    const json = await res.json()

    // FILL FORM SELECT GENEROS
    const formSelect = document.querySelectorAll(".form-edit-articulos #generosEdit .option");

    // DELETE CLASS FROM PREVIOUS CHARGE
    selectedOption["generosEdit"] = []
    formSelect.forEach( option => {
        if(option.classList.contains("selected-option")){
            option.classList.toggle("selected-option");
        }
    });
    //CHARGE DATA
    formSelect.forEach( option => {
        if(json[0].generos.includes(option.textContent.trim())){
            option.classList.toggle("selected-option");
            selectedOption["generosEdit"].push(option.textContent.trim())
        }
    });
    if(selectedOption["generosEdit"].length > 0){
        document.querySelector(".form-edit-articulos #generos").value = selectedOption["generosEdit"].join(" - ")
    }

    // FILL FORM SELECT TIPO
    if(json[0].tipo === "anime"){
        document.querySelector(".form-edit-articulos #tipo").value = "Anime";
    } else if (json[0].tipo === "novela"){
        document.querySelector(".form-edit-articulos #tipo").value = "Novela";
    } else {
        document.querySelector(".form-edit-articulos #tipo").value = "Manga";
    }

    // FILL FORM SELECT ESTADO
    if(json[0].estado === "En emisión"){
        document.querySelector(".form-edit-articulos #estado").value = "En emisión";
    }
    else{
        document.querySelector(".form-edit-articulos #estado").value = "Finalizado";
    }

    document.querySelector(".form-edit-articulos .file-preview").src = json[0].portada;
    document.querySelector(".form-edit-articulos .file-preview").style.display = "flex";
    document.querySelector(".form-edit-articulos #titulo").value = json[0].titulo;
    document.querySelector(".form-edit-articulos #sipnosis").value = json[0].sipnosis;
    document.querySelector(".form-edit-articulos #autor").value = json[0].autor;
    document.querySelector(".form-edit-articulos #link").value = json[0].link;
    document.querySelector(".form-edit-articulos .articulo-id").value = e.dataset.id
}
});

//CHARGE DATA ON FORM DELETE
const btnDelete = document.querySelectorAll(".btn-delete");
btnDelete.forEach( btn => {
    btn.onclick = () => {
        document.querySelector(".form-delete-articulo .articulo-id").value = btn.dataset.id;
    };
});

// MESSAGES FOR CRUD
try {
    const message = document.querySelector(".toast");
    new bootstrap.Toast(message).show() 
} catch (err) {
    console.log(err)
}

//PREVIEW IMG
const showPreviewNew = (event) => {
    if(event.target.files.length > 0){
        let src = URL.createObjectURL(event.target.files[0]);
        let preview = document.querySelector(".form-new-articulo .file-preview");
        preview.src = src;
        preview.style.display = "flex"
    }
}

const showPreviewEdit = (event) => {
    if(event.target.files.length > 0){
        let src = URL.createObjectURL(event.target.files[0]);
        let preview = document.querySelector(".form-edit-articulos .file-preview");
        preview.src = src;
        preview.style.display = "flex"
    }
}