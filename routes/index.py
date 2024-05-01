from flask import Blueprint
from flask import render_template, redirect, abort, request
from services.index import recent_animes, recent_mangas, recent_novelas, get_busqueda_service, get_animes_service, get_mangas_service, get_novelas_service, get_article_anime_service, get_article_novela_service, get_article_manga_service, get_article_service, get_animes_filter_service, get_mangas_filter_service, get_novelas_filter_service
from services.admin import get_carrusels_service, get_generos_service
index = Blueprint('index', __name__)

@index.route('/')
def first_page():
    dataAnimes = recent_animes()
    dataMangas = recent_mangas()
    dataNovelas = recent_novelas()
    dataCarrusel = get_carrusels_service()
    return render_template('pages/index.html', 
                           carrusel = dataCarrusel.json,
                           articlesAnimes = dataAnimes.json, 
                           articlesMangas = dataMangas.json, 
                           articlesNovelas = dataNovelas.json)

# SHOW ALL ARTICLES BY TYPE
@index.route("/animes/")
def get_animes():
    data = get_animes_service()
    generosData = get_generos_service(all=True)
    return render_template("pages/animes.html", 
                           articles = data.json, 
                           generos= generosData.json,
                           current_page = 1)

@index.route("/animes/page/<number>")
def get_animes_page(number):
    data = get_animes_service(int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("pages/animes.html", 
                           articles = data.json, 
                           generos = generosData.json,
                           current_page = int(number))

@index.route("/mangas/")
def get_mangas():
    data = get_mangas_service()
    generosData = get_generos_service(all=True)
    return render_template("/pages/mangas.html", 
                           articles = data.json, 
                           generos=generosData.json, 
                           current_page = 1)

@index.route("/mangas/page/<number>")
def get_mangas_page(number):
    data = get_mangas_service(int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("/pages/mangas.html", 
                           articles = data.json, 
                           generos=generosData.json, 
                           current_page = int(number))

@index.route("/novelas/")
def get_novelas():
    data = get_novelas_service()
    generosData = get_generos_service(all=True)
    return render_template("/pages/novelas.html", 
                           articles = data.json, 
                           generos = generosData.json, 
                           current_page = 1)

@index.route("/novelas/page/<number>")
def get_novelas_page(number):
    data = get_novelas_service(int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("/pages/novelas.html", 
                           articles = data.json, 
                           generos = generosData.json, 
                           current_page = int(number))

# GET ARTICLE FILTER
@index.route("/animes/filtros")
def get_animes_filter():
    data = get_animes_filter_service()
    generosData = get_generos_service(all=True)
    return render_template("pages/animes.html", 
                           articles = data.json, 
                           generos = generosData.json,
                           current_page = 1)

@index.route("/animes/filtros/page/<number>")
def get_animes_filter_page(number):
    data = get_animes_filter_service(int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("pages/animes.html", 
                           articles = data.json, 
                           generos = generosData.json, 
                           current_page = int(number))

@index.route("/novelas/filtros")
def get_novelas_filter():
    data = get_novelas_filter_service()
    generosData = get_generos_service(all=True)
    return render_template("pages/novelas.html", 
                           articles = data.json, 
                           generos = generosData.json,
                           current_page = 1)

@index.route("/novelas/filtros/page/<number>")
def get_novelas_filter_page(number):
    data = get_novelas_filter_service(int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("pages/novelas.html", 
                           articles = data.json, 
                           generos = generosData.json, 
                           current_page = int(number))

@index.route("/mangas/filtros")
def get_mangas_filter():
    data = get_mangas_filter_service()
    generosData = get_generos_service(all=True)
    return render_template("pages/mangas.html", 
                           articles = data.json, 
                           generos = generosData.json,
                           current_page = 1)

@index.route("/mangas/filtros/page/<number>")
def get_mangas_filter_page(number):
    data = get_mangas_filter_service(int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("pages/mangas.html", 
                           articles = data.json,
                           generos = generosData.json,
                           current_page = int(number))

# GET ARTICLE
@index.route("/article/<id>", methods=["POST"])
def get_article(id):
    data = get_article_service(id)
    return data

@index.route("/animes/<name>")
def get_anime(name):
    data = get_article_anime_service(name)
    if data:
        return render_template("pages/article.html", info = data.json)
    else:
        abort(404)

@index.route("/mangas/<name>")
def get_manga(name):
    data = get_article_manga_service(name)
    if data:
        return render_template("pages/article.html", info = data.json)
    else:
        abort(404)

@index.route("/novelas/<name>")
def get_novela(name):
    data = get_article_novela_service(name)
    if data:
        return render_template("pages/article.html", info = data.json)
    else:
        abort(404)

#BUSQUEDA
@index.route("/buscar/<name>")
def get_busqueda(name):
    data = get_busqueda_service(name)
    generosData = get_generos_service(all=True)
    return render_template("pages/busqueda.html",
                           busqueda = name, 
                           articles = data.json,
                           generos = generosData.json,
                           current_page = 1)

@index.route("/buscar/<name>/page/<number>")
def get_busqueda_page(name, number):
    data = get_busqueda_service(name, int(number) - 1)
    generosData = get_generos_service(all=True)
    return render_template("pages/busqueda.html", 
                           busqueda = name,
                           articles = data.json,
                           generos = generosData.json,
                           current_page = int(number))

@index.app_errorhandler(404)
def not_found(e):
    return render_template("pages/404.html"), 404