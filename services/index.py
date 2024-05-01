from schema.index import articulos
from flask import request, Response
from bson import json_util, ObjectId
import math


# ARTICULOS RECIENTES
def recent_animes():
    data = articulos.objects(tipo="anime").limit(5)
    return Response(data.to_json(), mimetype="application/json")

def recent_mangas():
    data = articulos.objects(tipo="manga").limit(5)
    return Response(data.to_json(), mimetype="application/json")

def recent_novelas():
    data = articulos.objects(tipo="novela").limit(5)
    return Response(data.to_json(), mimetype="application/json")

# ARTICULOS POR TIPO
limit_articulos = 12

def get_busqueda_service(busqueda, page = 0):
    generosFilter = request.args.get("generos")
    estadoFilter = request.args.get("estado")
    objFilter = {}

    # VALIDATION FOR FILTERS
    if bool(generosFilter):
        objFilter["generos__all"] = generosFilter.split(" - ")
    else: 
        generosFilter = ""
    if bool(estadoFilter):
        objFilter["estado"] = estadoFilter
    else:
        estadoFilter = ""

    data = articulos.objects(**objFilter).search_text(busqueda).skip(page * limit_articulos).limit(limit_articulos)

    #ADD COUNT PAGES AND FILTERS
    data_count = math.ceil(data.count() / limit_articulos)
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages":data_count})
    data.append({"generos": generosFilter, "estado": estadoFilter})
    data = json_util.dumps(data)

    return Response(data, mimetype="application/json")

def get_animes_service(page = 0):
    data = articulos.objects(tipo = "anime").skip(page * limit_articulos).limit(limit_articulos)
    data_count = math.ceil(data.count() / limit_articulos)

    #ADD COUNT OF PAGES
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages": data_count})
    data = json_util.dumps(data)
    
    return Response(data, mimetype="application/json")

def get_novelas_service(page = 0):
    data = articulos.objects(tipo="novela").skip(page * limit_articulos).limit(limit_articulos)
    data_count = math.ceil(data.count() / limit_articulos)
    
    #ADD COUNT OF PAGES
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages": data_count})
    data = json_util.dumps(data)
    
    return Response(data, mimetype="application/json")

def get_mangas_service(page = 0):
    data = articulos.objects(tipo="manga").skip(page * limit_articulos).limit(limit_articulos)
    data_count = math.ceil(data.count() / limit_articulos)
    
    #ADD COUNT OF PAGES
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages": data_count})
    data = json_util.dumps(data)
    
    return Response(data, mimetype="application/json")

# OBTENER ARTICULO
def get_article_service(id):
    data = articulos.objects(id=ObjectId(id))
    return Response(data.to_json(), mimetype="application/json")

def get_article_anime_service(name):
    data = articulos.objects(titulo = name).first()
    print(data, name)
    if data:
        return Response(data.to_json(), mimetype="application/json")
    else:
        return data

def get_article_manga_service(name):
    data = articulos.objects(titulo = name).first()
    if data:
        return Response(data.to_json(), mimetype="application/json")
    else:
        return data

def get_article_novela_service(name):
    data = articulos.objects(titulo = name).first()
    if data:
        return Response(data.to_json(), mimetype="application/json")
    else:
        return data

# FILTRO DE ARTICULOS
def get_article_filter_service():
    generosFilter = request.form.get("generos").split(" - ")
    estadoFilter = request.form.get("estado")
    tipo = request.form.get("tipo")
    data = articulos.objects(tipo=tipo, estado = estadoFilter, generos__all = generosFilter)
    return Response(data.to_json(), mimetype="application/json")

def get_animes_filter_service(page = 0):
    generosFilter = request.args.get("generos")
    estadoFilter = request.args.get("estado")
    objFilter = {"tipo": "anime"}

    # VALIDATION FOR FILTERS
    if bool(generosFilter):
        objFilter["generos__all"] = generosFilter.split(" - ")
    else: 
        generosFilter = ""
    if bool(estadoFilter):
        objFilter["estado"] = estadoFilter
    else:
        estadoFilter = ""

    data = articulos.objects(**objFilter).skip(page * limit_articulos).limit(limit_articulos)

    #ADD COUNT PAGES AND FILTERS
    data_count = math.ceil(data.count() / limit_articulos)
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages":data_count})
    data.append({"generos": generosFilter, "estado": estadoFilter})
    data = json_util.dumps(data)

    return Response(data, mimetype="application/json")

def get_novelas_filter_service(page = 0):
    generosFilter = request.args.get("generos")
    estadoFilter = request.args.get("estado")
    objFilter = {"tipo": "novela"}

    # VALIDATION FOR FILTERS
    if bool(generosFilter):
        objFilter["generos__all"] = generosFilter.split(" - ")
    else: 
        generosFilter = ""
    if bool(estadoFilter):
        objFilter["estado"] = estadoFilter
    else:
        estadoFilter = ""

    data = articulos.objects(**objFilter).skip(page * limit_articulos).limit(limit_articulos)

    #ADD COUNT PAGES AND FILTERS
    data_count = math.ceil(data.count() / limit_articulos)
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages":data_count})
    data.append({"generos": generosFilter, "estado": estadoFilter})
    data = json_util.dumps(data)

    return Response(data, mimetype="application/json")

def get_mangas_filter_service(page = 0):
    generosFilter = request.args.get("generos")
    estadoFilter = request.args.get("estado")
    objFilter = {"tipo": "manga"}

    # VALIDATION FOR FILTERS
    if bool(generosFilter):
        objFilter["generos__all"] = generosFilter.split(" - ")
    else: 
        generosFilter = ""
    if bool(estadoFilter):
        objFilter["estado"] = estadoFilter
    else:
        estadoFilter = ""

    data = articulos.objects(**objFilter).skip(page * limit_articulos).limit(limit_articulos)

    #ADD COUNT PAGES AND FILTERS
    data_count = math.ceil(data.count() / limit_articulos)
    data = [json_util.loads(data.to_json())]
    data.append({"count_pages":data_count})
    data.append({"generos": generosFilter, "estado": estadoFilter})
    data = json_util.dumps(data)

    return Response(data, mimetype="application/json")