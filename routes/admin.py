from flask import Blueprint
from flask import render_template, flash, redirect, request
from flask_login import login_required
from services.admin import get_generos_service, get_genero_service, new_genero_service, edit_genero_service, delete_genero_service, search_articulo_service
from services.admin import get_articulos_service, get_articulo_service, new_articulo_service, edit_articulo_service, delete_articulo_service, count_generos_service
from services.admin import get_carrusel_service, get_carrusels_service, new_carrusel_service, edit_carrusel_service, delete_carrusel_service

admin = Blueprint("admin", __name__)

@admin.route("/")
@login_required
def admin_page():
    return render_template("pages/admin/admin.html")

#ARTICULOS
@admin.route("/articulos")
@login_required
def admin_articulos():
    data_articulos = get_articulos_service()
    data_generos = get_generos_service(all=True)
    return render_template("pages/admin/articulos.html", 
                           articulos = data_articulos.json, 
                           generos = data_generos.json,
                           current_page = 1)

@admin.route("/articulos/page/<number>")
@login_required
def admin_articulos_page(number):
    data_articulos = get_articulos_service(int(number)-1)
    data_generos = get_generos_service(all=True)
    return render_template("pages/admin/articulos.html", 
                           articulos = data_articulos.json, 
                           generos = data_generos.json,
                           current_page = int(number))

@admin.route("/articulos/<id>")
@login_required
def get_articulo(id):
    data = get_articulo_service(id)
    return data

@admin.route("/articulos/new", methods=["POST"])
@login_required
def new_articulo():
    created = new_articulo_service()
    if created == 1:
        flash("Se ha guardado el articulo", "success")
        return redirect("/admin/articulos")
    elif created == 2:
        flash("Ha ocurrido un error al añadir el articulo", "error")
        return redirect("/admin/articulos")
    else:
        flash("Solo se pueden agregar imagenes!", "error")
        return redirect("/admin/articulos")

@admin.route("/articulos/edit", methods=["POST"])
@login_required
def edit_articulo():
    updated = edit_articulo_service(request.form.get("id"))
    if updated == 1:
        flash("Se ha actualizado el articulo", "success")
        return redirect("/admin/articulos")
    elif updated == 2:
        flash("Ha ocurrido un error al actualizar el articulo", "error")
        return redirect("/admin/articulos")
    else:
        flash("Solo se pueden agregar imagenes!", "error")
        return redirect("/admin/articulos")

@admin.route("/articulos/delete", methods=["POST"])
@login_required
def delete_articulo():
    deleted = delete_articulo_service(request.form.get("id"))
    if str(deleted.id) == request.form.get("id"):
        flash("Se ha eliminado el articulo", "success")
        return redirect("/admin/articulos")
    else: 
        flash("Ha ocurrido un error al eliminar el articulo", "error")

@admin.route("/articulos/buscar")
@login_required
def search_articulo():
    search = search_articulo_service()
    generos = get_generos_service(all=True)
    return render_template("/pages/admin/articulos.html", 
                           articulos = search.json,
                           generos = generos.json,
                           busqueda = True,
                           current_page = 1)

@admin.route("/articulos/buscar/page/<number>")
@login_required
def search_articulo_page(number):
    search = search_articulo_service(int(number) - 1)
    generos = get_generos_service(all=True)
    return render_template("/pages/admin/articulos.html", 
                           articulos = search.json,
                           generos = generos.json,
                           busqueda = True,
                           current_page = int(number))




# GENEROS
@admin.route("/generos")
@login_required
def admin_generos():
    data = get_generos_service()
    return render_template("pages/admin/generos.html", generos = data.json, current_page = 1)

@admin.route("/generos/page/<number>")
def admin_generos_page(number):
    data = get_generos_service(int(number)-1)
    return render_template("pages/admin/generos.html", generos = data.json, current_page = int(number))
    
@admin.route("/generos/<id>")
@login_required
def admin_genero(id):
    data = get_genero_service(id)
    return data

@admin.route("/generos/new", methods=["POST"])
@login_required
def new_genero():
    created = new_genero_service()
    if created:
        flash("Se ha guardado el genero", "success")
        return redirect("/admin/generos")
    else:
        flash("Ha ocurrido un error al añadir el genero", "error")

@admin.route("/generos/edit", methods=["POST"])
@login_required
def edit_genero():
    updated = edit_genero_service(request.form.get("id"))
    if updated:
        flash("El genero se ha actualizado", "success")
        return redirect("/admin/generos")
    else:
        flash("Ha ocurrido un error al actualizar", "error")
        return redirect("/admin/generos")
    
@admin.route("/generos/delete", methods=["POST"])
@login_required
def delete_genero():
    deleted = delete_genero_service(request.form.get("id"))
    if str(deleted.id) == request.form.get("id"):
        flash("El genero se ha eliminado", "success")
        return redirect("/admin/generos")
    else:
        flash("Ha ocurrido un error al eliminar", "error")
        return redirect("/admin/generos")



# CARRUSEL
@admin.route("/carrusel")
def get_carrusel_config():
    data = get_carrusels_service()
    return render_template("/pages/admin/carrusel.html", imgs = data.json)

@admin.route("/carrusel/<id>")
def get_carrusel(id):
    data = get_carrusel_service(id)
    return data

@admin.route("/carrusel/new", methods=["POST"])
def new_carrusel():
    created = new_carrusel_service()
    if created == 1:
        flash("Se ha agregado el elemento", "success")
        return redirect("/admin/carrusel")
    elif created == 2:
        flash("Ha ocurrido un error al agregar el elemento", "error")
        return redirect("/admin/carrusel")
    else:
        flash("Solo se pueden agregar imagenes!", "error")
        return redirect("/admin/carrusel")
    
@admin.route("/carrusel/edit", methods=["POST"])
def edit_carrusel():
    updated = edit_carrusel_service(request.form.get("id"))
    if updated == 1:
        flash("Se ha actualizado el elemento", "success")
        return redirect("/admin/carrusel")
    elif updated == 2:
        flash("Ha ocurrido un error al actualizar el elemento", "error")
        return redirect("/admin/carrusel")
    else:
        flash("Solo se pueden agregar imagenes!", "error")
        return redirect("/admin/carrusel")

@admin.route("/carrusel/delete", methods=["POST"])
def delete_carrusel():
    deleted = delete_carrusel_service(request.form.get("id"))
    if str(deleted.id) == request.form.get("id"):
        flash("Se ha eliminado el elemento", "success")
        return redirect("/admin/carrusel")
    else:
        flash("Ha ocurrido un error al eliminar", "error")
        return redirect("/admin/carrusel")