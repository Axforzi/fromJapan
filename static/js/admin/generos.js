// CHARGE DATA ON FORM EDIT
const btnEdit = document.querySelectorAll(".btn-edit");

btnEdit.forEach( e => {
e.onclick = async () => {
    const res = await fetch(`/admin/generos/${e.dataset.id}`)
    const json = await res.json()
    const editInput = document.querySelector(".form-edit-generos .edit-input").value = json.nombre
    const idInput = document.querySelector(".form-edit-generos .genero-id").value = e.dataset.id
}
});

// CHARGE DATA ON FORM DELETE
const btnDelete = document.querySelectorAll(".btn-delete");

btnDelete.forEach( e => {
e.onclick = async () => {
    const idInput = document.querySelector(".form-delete-generos .genero-id").value = e.dataset.id
}
});

// MESSAGES FOR CRUD
try {
    const message = document.querySelector(".toast");
    new bootstrap.Toast(message).show() 
} catch (err) {
    console.log(err)
}