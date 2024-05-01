// CHARGE DATA ON FORM EDIT
const btnEdit = document.querySelectorAll(".btn-edit");

btnEdit.forEach( e => {
e.onclick = async () => {
    const res = await fetch(`/admin/carrusel/${e.dataset.id}`)
    const json = await res.json()
    document.querySelector(".form-edit-carrusel .file-preview").src = json.ruta
    document.querySelector(".form-edit-carrusel .file-preview").style.display = "flex"
    document.querySelector(".form-edit-carrusel .edit-input").value = json.titulo
    document.querySelector(".form-edit-carrusel .link-input").value = json.link
    document.querySelector(".form-edit-carrusel .carrusel-id").value = e.dataset.id
    document.querySelector(".form-edit-carrusel .last-file").value = json.ruta.split("/").pop()
}
});

// CHARGE DATA ON FORM DELETE
const btnDelete = document.querySelectorAll(".btn-delete");

btnDelete.forEach( e => {
e.onclick = async () => {
    document.querySelector(".form-delete-carrusel .carrusel-id").value = e.dataset.id
}
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
        let preview = document.querySelector(".form-new-carrusel .file-preview");
        preview.src = src;
        preview.style.display = "flex"
    }
}

const showPreviewEdit = (event) => {
    if(event.target.files.length > 0){
        let src = URL.createObjectURL(event.target.files[0]);
        let preview = document.querySelector(".form-edit-carrusel .file-preview");
        preview.src = src;
        preview.style.display = "flex"
    }
}