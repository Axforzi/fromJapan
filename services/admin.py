import datetime
from flask import request, Response, flash
from flask_login import login_user
from schema.index import articulos, users, generos, carrusel
from bson import ObjectId
from werkzeug.utils import secure_filename
import numpy as np
import math
import os
from bson import json_util

def login_service():
    data = request.form
    user = users.objects(username=data.get("username")).first()
    if user:
        if user.password == data.get("password"):
            login_user(user)
            return True
        else:
            flash("Contraseña incorrecta!!", "error")
            return False
    else:
        flash("Usuario incorrecto!!", "error")
        return False

#CRUD ARTICLES
limit_articulos = 10

def get_articulos_service(page = 0):
    data = articulos.objects().skip(page * limit_articulos).limit(limit_articulos)
    data_count = math.ceil(data.count() / limit_articulos)
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages": data_count})
    return Response(json_util.dumps(data), mimetype="application/json")

def get_articulo_service(id):
    data = articulos.objects(id=ObjectId(id))
    return Response(data.to_json(), mimetype="application/json")

def new_articulo_service():
    article = request.form.to_dict()
    article["generos"] = np.array(article["generos"].split(" - "))
    article["tipo"] = article["tipo"].lower()

    # GET FILE FOR COVER
    file = request.files["img"]
    extension = os.path.splitext(file.filename)[1]
    filename = secure_filename(datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + article["titulo"] + extension)
    path_name = "/static/img/portadas/" + filename
    article["portada"] = path_name

    if (extension == ".png") or (extension == ".jpg") or (extension == ".jpeg"):
        data = articulos(**article)
        created = data.save()
        file.save(os.path.join(os.getcwd(), "static\\img\\portadas", filename))

        return 1 if created else 2
    else:
        return 3

def edit_articulo_service(id):
    data = articulos.objects(id=ObjectId(id)).first()

    # CREATE OBJECT TO UPDATE
    article = request.form.to_dict()
    article.pop("id")
    article["generos"] = np.array(article["generos"].split(" - "))
    article["updatedAt"] = datetime.datetime.now
    article["tipo"] = article["tipo"].lower()

    # GET FILE FOR COVER
    file = request.files["img"]
    extension = os.path.splitext(file.filename)[1]
    filename = secure_filename(datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + article["titulo"] + extension)
    path_route = "/static/img/portadas/" + filename

    if file.filename != "":
        if (extension == ".png") or (extension == ".jpg") or (extension == ".jpeg"):
            article["portada"] = path_route
            updated = data.update(**article)

            os.remove(os.path.join(os.getcwd(), "static\\img\\portadas", data.portada.split("/")[-1]))
            file.save(os.path.join(os.getcwd(), "static\\img\\portadas", filename))

            return 1 if updated else 2
        else:
            return 3
    else:
        updated = data.update(**article)
        return updated

def delete_articulo_service(id):
    data = articulos.objects(id=ObjectId(id)).first()
    
    os.remove(os.path.join(os.getcwd(), "static\\img\\portadas", data.portada.split("/")[-1]))
    data.delete()
    return data

def search_articulo_service(page = 0):
    tipo = request.args.get("tipo").lower()
    buscar = request.args.get("buscar")

    if tipo == "todos":
        data = articulos
        if buscar != "":
            data = articulos.objects().search_text(buscar).skip(page * limit_articulos).limit(limit_articulos)
        else:
            data = articulos.objects().skip(page * limit_articulos).limit(limit_articulos)
        print(data.to_json())
        data_count = math.ceil(data.count()/limit_articulos)
        data = [json_util.loads(data.to_json())]
        data.append({"count_pages": data_count})
        data.append({"buscar": buscar, "tipo": tipo})
        return Response(json_util.dumps(data), mimetype="application/json")
    
    else:
        data = articulos
        if buscar != "":
            data = articulos.objects(tipo=tipo).search_text(buscar).skip(page * limit_articulos).limit(limit_articulos)
        else:
            data = articulos.objects(tipo=tipo).skip(page * limit_articulos).limit(limit_articulos)

        data_count = math.ceil(data.count()/limit_articulos)
        data = [json_util.loads(data.to_json())]
        data.append({"count_pages": data_count})
        data.append({"buscar": buscar, "tipo": tipo})
        return Response(json_util.dumps(data), mimetype="application/json")


#CRUD GENEROS
limit_generos = 10

def count_generos_service():
    data = generos.objects().count()
    data = math.ceil(data / limit_generos)
    return data

def get_generos_service(page = 0, all = False):
    if all:
        data = generos.objects()
        return Response(data.to_json(), mimetype="application/json")
    else:
        data = generos.objects().skip(limit_generos*page).limit(limit_generos)
        data_count = math.ceil(data.count()/limit_generos)
        data = [json_util.loads(data.to_json())]
        data.append({"count_pages": data_count})
        return Response(json_util.dumps(data), mimetype="application/json")

def get_genero_service(id):
    data = generos.objects(id=ObjectId(id)).first()
    return Response(data.to_json(), mimetype="application/json")

def new_genero_service():
    data = generos(nombre = request.form.get("nombre"))
    created = data.save()
    return created

def edit_genero_service(id):
    data = generos.objects(id=ObjectId(id)).first()
    updated = data.update(nombre = request.form.get("nombre"), updatedAt=datetime.datetime.now)
    return updated

def delete_genero_service(id):
    data = generos.objects(id=ObjectId(id)).first()
    data.delete()
    return data




#CRUD CARRUSEL
def get_carrusels_service():
    data = carrusel.objects()
    return Response(data.to_json(), mimetype="application/json")

def get_carrusel_service(id):
    data = carrusel.objects(id=ObjectId(id)).first()
    return Response(data.to_json(), mimetype="application/json")

def new_carrusel_service():
    file = request.files["img"]
    filename = secure_filename(datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + file.filename)
    extension = os.path.splitext(filename)[1]

    if (extension == ".png") or (extension == ".jpg") or (extension == ".jpeg"):
        path_name = "/static/img/carrusel/" + filename
        data = carrusel(titulo = request.form.get("titulo"), link = request.form.get("link"), ruta = path_name)
        file.save(os.path.join(os.getcwd(), "static\\img\\carrusel", filename))
        created = data.save()
        return 1 if created else 2
    else:
        return 3

def edit_carrusel_service(id):
    data = carrusel(id=ObjectId(id))

    file = request.files["img"]
    filename = secure_filename(datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + file.filename)
    extension = os.path.splitext(filename)[1]

    # VALIDATE IF THERE IS A FILE
    if file.filename != "":
        # VALIDATE EXTENSION
        if (extension == ".png") or (extension == ".jpg") or (extension == ".jpeg"):
            os.remove(os.path.join(os.getcwd(), "static\\img\\carrusel", request.form.get("last-file"))) # ELIMINAR ANTERIOR IMG
            path_name = "/static/img/carrusel/" + filename

            #SAVE FILE AND INFO ON THE DB
            updated = data.update(titulo = request.form.get("titulo"), link = request.form.get("link"), ruta = path_name, updatedAt = datetime.datetime.now)
            os.remove(os.path.join(os.getcwd(), "static\\img\\carrusel", data.ruta.split("/")[-1]))
            file.save(os.path.join(os.getcwd(), "static\\img\\carrusel", filename))
            
            return 1 if updated else 2
        else:
            return 3
    else:
        updated = data.update(titulo = request.form.get("titulo"), link = request.form.get("link"), updatedAt = datetime.datetime.now)
        return updated

def delete_carrusel_service(id):
    data = carrusel.objects(id=ObjectId(id)).first()
    os.remove(os.path.join(os.getcwd(), "static\\img\\carrusel",data.ruta.split("/")[-1]))
    data.delete()
    return data