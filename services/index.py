import math

from bson import json_util
from flask import Response, request

from schema.index import articulos

limit_articulos = 12


def _json_response(data) -> Response:
    """Envuelve una lista de objetos Mongo en una Response JSON."""
    return Response(json_util.dumps(data), mimetype="application/json")


def recent_animes() -> Response:
    """Devuelve los 5 animes más recientes."""
    return Response(articulos.objects(tipo="anime").limit(5).to_json(), mimetype="application/json")


def recent_mangas() -> Response:
    """Devuelve los 5 mangas más recientes."""
    return Response(articulos.objects(tipo="manga").limit(5).to_json(), mimetype="application/json")


def recent_novelas() -> Response:
    """Devuelve las 5 novelas más recientes."""
    return Response(articulos.objects(tipo="novela").limit(5).to_json(), mimetype="application/json")


def _paged_articles(tipo: str, page: int = 0) -> list:
    """Devuelve los artículos de un tipo paginados junto con el número de páginas."""
    data = (
        articulos.objects(tipo=tipo)
        .skip(page * limit_articulos)
        .limit(limit_articulos)
    )
    data_count = math.ceil(data.count() / limit_articulos)
    return [json_util.loads(data.to_json()), {"count_pages": data_count}]


def get_animes_service(page: int = 0) -> Response:
    """Devuelve la página de animes indicada."""
    return _json_response(_paged_articles("anime", page))


def get_novelas_service(page: int = 0) -> Response:
    """Devuelve la página de novelas indicada."""
    return _json_response(_paged_articles("novela", page))


def get_mangas_service(page: int = 0) -> Response:
    """Devuelve la página de mangas indicada."""
    return _json_response(_paged_articles("manga", page))


# OBTENER ARTICULO
def _get_article_by_name(tipo: str, name: str) -> Response | None:
    """Busca un artículo por tipo y título; None si no existe."""
    data = articulos.objects(tipo=tipo, titulo=name).first()
    if data:
        return Response(data.to_json(), mimetype="application/json")
    return None


def get_article_anime_service(name: str) -> Response | None:
    return _get_article_by_name("anime", name)


def get_article_manga_service(name: str) -> Response | None:
    return _get_article_by_name("manga", name)


def get_article_novela_service(name: str) -> Response | None:
    return _get_article_by_name("novela", name)


# FILTRO DE ARTICULOS
def get_article_filter_service() -> Response:
    """Filtra artículos por tipo, estado y géneros desde un formulario POST."""
    generosFilter = request.form.get("generos").split(" - ")
    estadoFilter = request.form.get("estado")
    tipo = request.form.get("tipo")
    data = articulos.objects(tipo=tipo, estado=estadoFilter, generos__all=generosFilter)
    return Response(data.to_json(), mimetype="application/json")


def _get_filtered(tipo: str, page: int = 0) -> Response:
    """
    Devuelve artículos de un tipo aplicando filtros de género y estado desde query params.
    Incluye el total de páginas y los filtros aplicados en la respuesta.
    """
    generosFilter = request.args.get("generos")
    estadoFilter = request.args.get("estado")
    objFilter = {"tipo": tipo}

    if generosFilter:
        objFilter["generos__all"] = generosFilter.split(" - ")
    else:
        generosFilter = ""
    if not estadoFilter:
        estadoFilter = ""

    data = (
        articulos.objects(**objFilter)
        .skip(page * limit_articulos)
        .limit(limit_articulos)
    )
    data_count = math.ceil(data.count() / limit_articulos)

    payload = [
        json_util.loads(data.to_json()),
        {"count_pages": data_count},
        {"generos": generosFilter, "estado": estadoFilter},
    ]
    return _json_response(payload)


def get_animes_filter_service(page: int = 0) -> Response:
    return _get_filtered("anime", page)


def get_novelas_filter_service(page: int = 0) -> Response:
    return _get_filtered("novela", page)


def get_mangas_filter_service(page: int = 0) -> Response:
    return _get_filtered("manga", page)


#BUSQUEDA
def get_busqueda_service(busqueda: str, page: int = 0) -> Response:
    """Busca artículos por texto aplicando filtros opcionales de género y estado."""
    generosFilter = request.args.get("generos")
    estadoFilter = request.args.get("estado")
    objFilter = {}

    if generosFilter:
        objFilter["generos__all"] = generosFilter.split(" - ")
    else:
        generosFilter = ""
    if not estadoFilter:
        estadoFilter = ""

    data = (
        articulos.objects(**objFilter)
        .search_text(busqueda)
        .skip(page * limit_articulos)
        .limit(limit_articulos)
    )
    data_count = math.ceil(data.count() / limit_articulos)

    payload = [
        json_util.loads(data.to_json()),
        {"count_pages": data_count},
        {"generos": generosFilter, "estado": estadoFilter},
    ]
    return _json_response(payload)