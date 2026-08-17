"""Tests para From Japan.

Dos capas:
  * Unit tests de lógica pura (seed/tokenización) — corren siempre, sin BD.
  * Integration tests (rutas, servicios, búsqueda y flujo admin) — requieren
    MongoDB; si no hay una instancia disponible se omiten.

Los tests apuntan a la base ``fromjapan_test`` y NUNCA tocan ``MONGO_URI`` de
producción (se fuerza a falso/atlas test antes de importar la app).

Uso con MongoDB (docker):
    docker run -p 27017:27017 mongo:7
    uv run pytest -q
"""
import os

# Fuerza la conexión a una base de test ANTES de importar app/seed, para no
# tocar jamás la URI de producción (p. ej. la del .env).
TEST_DB = "fromjapan_test"
MONGO_URI_TEST = os.environ.get("MONGO_URI_TEST", "mongodb://localhost:27017")
os.environ["MONGO_URI"] = os.environ.get(
    "MONGO_URI_TEST", f"{MONGO_URI_TEST}/{TEST_DB}"
)

import pytest
from mongoengine import connect, connection

import app as app_module
import seed
import services.index as svc
from schema.index import articulos, carrusel, generos, users


# --------------------------------------------------------------------------- #
# Fixtures de MongoDB (solo los tests que las pidan se ven afectados)
# --------------------------------------------------------------------------- #
def _drop() -> None:
    for doc in (articulos, generos, users, carrusel):
        doc.drop_collection()


def _ensure_indexes() -> None:
    articulos.ensure_indexes()


@pytest.fixture(scope="session")
def mongo():
    try:
        connect(
            db=TEST_DB,
            host=MONGO_URI_TEST,
            serverSelectionTimeoutMS=3000,
            uuidRepresentation="standard",
        )
        connection.get_connection().admin.command("ping")
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"MongoDB no disponible: {exc}")
    yield
    connection.disconnect()


@pytest.fixture
def clean_db(mongo):
    """Colecciones vacías e índices creados antes y después de cada test."""
    _drop()
    _ensure_indexes()
    yield
    _drop()


@pytest.fixture
def client(clean_db):
    """Test client de Flask con BD limpia."""
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def _make_article(titulo: str, tipo: str = "anime", generos=None, **extra) -> None:
    articulos(
        titulo=titulo,
        sipnosis=extra.pop("sipnosis", "Sinopsis de prueba"),
        tipo=tipo,
        estado=extra.pop("estado", "Finalizado"),
        generos=generos or ["Acción"],
        **extra,
    ).save()


def _make_user(username="admin", password="secret") -> None:
    u = users(username=username)
    u.set_password(password)
    u.save()


# --------------------------------------------------------------------------- #
# Unit tests — seed / lógica pura (no requieren BD)
# --------------------------------------------------------------------------- #
def test_limpiar_descripcion_quita_html():
    limpia = seed.limpiar_descripcion("<p>Hola   <b>mundo</b></p>")
    assert limpia == "Hola mundo"


def test_limpiar_descripcion_recorta_a_2000():
    largo = "palabra " * 500  # > 2000 chars
    resultado = seed.limpiar_descripcion(largo)
    assert len(resultado) <= 2000


def test_recortar_no_parte_palabras():
    texto = "texto " * 600
    resultado = seed.recortar_por_palabra(texto, 2000)
    assert len(resultado) <= 2000
    assert resultado.endswith("texto")


def test_estado_to_es():
    assert seed.estado_to_es("FINISHED") == "Finalizado"
    assert seed.estado_to_es("CANCELLED") == "Finalizado"
    assert seed.estado_to_es("RELEASING") == "En emisión"


def test_traducir_generos_mantiene_no_conocidos():
    assert seed.traducir_generos(["Action", "Desconocido"]) == ["Acción", "Desconocido"]


def test_slug_plataforma():
    assert seed._slug_plataforma("Google Play Books") == "google_play_books"
    assert seed._slug_plataforma("!!") == "plataforma"


def test_descargar_logo_local_usa_existente(monkeypatch):
    # "local:" solo copia de un archivo ya presente en el repo; no toca red.
    ruta = seed.descargar_logo("Crunchyroll")
    assert ruta.startswith("/static/img/")
    assert ruta.endswith(".png")


def test_extraer_links_filtra_whitelist_idioma_y_social(monkeypatch):
    media = {
        "externalLinks": [
            {"site": "Crunchyroll", "type": "STREAMING", "url": "https://www.crunchyroll.com/solo"},
            {"site": "Netflix", "type": "STREAMING", "url": "https://www.netflix.com/fr/title/123"},
            {"site": "Facebook", "type": "SOCIAL", "url": "https://facebook.com/x"},
            {"site": "Store Raro", "type": "STREAMING", "url": "https://storefare.com/x"},
        ]
    }
    monkeypatch.setattr(seed, "descargar_logo", lambda site: f"/logo/{site}.png")
    enlaces = seed.extraer_links(media, "anime")
    sitios = [e["site"] for e in enlaces]
    assert sitios == ["Crunchyroll"]
    assert enlaces[0]["logo"] == "/logo/Crunchyroll.png"


def test_extraer_links_dedupe_y_limite(monkeypatch):
    media = {"externalLinks": [
        {"site": "Netflix", "type": "STREAMING", "url": f"https://netflix.com/{i}"} for i in range(20)
    ]}
    monkeypatch.setattr(seed, "descargar_logo", lambda site: "")
    enlaces = seed.extraer_links(media, "anime")
    assert len(enlaces) == 1  # dedupe por sitio


def test_build_articulo_anime(monkeypatch):
    media = {
        "title": {"romaji": "One Piece", "english": None},
        "coverImage": {"extraLarge": "https://example.com/cov.jpg?v=1"},
        "genres": ["Action"],
        "description": "<b>Gran</b> serie de piratas.",
        "status": "FINISHED",
        "studios": {"nodes": [{"name": "Toei Animation"}]},
        "externalLinks": [{"site": "Crunchyroll", "type": "STREAMING", "url": "https://crunchyroll.com/op"}],
        "siteUrl": "https://anilist.co/anime/21",
    }
    monkeypatch.setattr(seed, "descargar_imagen", lambda *a, **k: None)
    monkeypatch.setattr(seed, "descargar_logo", lambda site: "")
    monkeypatch.setattr(seed, "traducir_texto", lambda t, *a, **k: "Gran serie de piratas.")
    articulo = seed.build_articulo(media, "anime", 1)
    assert articulo["titulo"] == "One Piece"
    assert articulo["autor"] == "Toei Animation"
    assert articulo["estado"] == "Finalizado"
    assert articulo["sipnosis"] == "Gran serie de piratas."
    assert articulo["link"] == "https://crunchyroll.com/op"
    assert len(articulo["links"]) == 1


# --------------------------------------------------------------------------- #
# Integration tests — rutas públicas (requieren MongoDB)
# --------------------------------------------------------------------------- #
def test_home_200(client):
    assert client.get("/").status_code == 200


def test_listados_200(client):
    for ruta in ("/animes/", "/mangas/", "/novelas/"):
        assert client.get(ruta).status_code == 200


def test_articulo_detalle_200_y_404(client):
    _make_article("Solo Leveling", "manga")
    ok = client.get("/mangas/Solo%20Leveling")
    assert ok.status_code == 200
    assert b"Solo Leveling" in ok.data
    assert client.get("/mangas/no-existe").status_code == 404


def test_busqueda_fulltext(client):
    _make_article("Blue Lock", "anime", sipnosis="Un delantero genio en Japón.")
    r = client.get("/buscar/Blue")
    assert r.status_code == 200
    assert b"Blue Lock" in r.data


def test_paginacion_reporta_paginas(client):
    for i in range(13):
        _make_article(f"Anime {i}", "anime")
    payload = svc.get_animes_service(0).json
    datos, meta = payload[0], payload[1]
    assert meta["count_pages"] == 2
    assert len(datos) == 12


def test_filtros_json(client):
    _make_article("Fantasía Uno", "anime", generos=["Fantasía"], estado="En emisión")
    _make_article("Fantasía Dos", "anime", generos=["Fantasía"], estado="En emisión")
    with app_module.app.test_request_context(
        "/animes/filtros?generos=Fantasía&estado=En emisión"
    ):
        r = svc.get_animes_filter_service()
        assert r.status_code == 200
        assert len(r.json[0]) == 2


# --------------------------------------------------------------------------- #
# Integration tests — flujo admin (requieren MongoDB)
# --------------------------------------------------------------------------- #
def test_admin_ruta_protegida_redirige(client):
    r = client.get("/admin/", follow_redirects=False)
    assert r.status_code == 302


def test_login_flujo_completo(client):
    _make_user("admin", "secret")

    assert client.post("/login", data={"username": "admin", "password": "mala"}).status_code == 200

    r = client.post("/login", data={"username": "admin", "password": "secret"})
    assert r.status_code == 302
    assert r.headers.get("Location", "").endswith("/admin")

    assert client.get("/admin/").status_code == 200
    assert client.get("/admin/generos").status_code == 200


def test_admin_crud_generos(client):
    _make_user("admin", "secret")
    client.post("/login", data={"username": "admin", "password": "secret"})

    r = client.post("/admin/generos/new", data={"nombre": "Acción"})
    assert r.status_code == 302

    assert b"Acci\xc3\xb3n" in client.get("/admin/generos").data

    genero = generos.objects(nombre="Acción").first()
    assert genero is not None
    r = client.post("/admin/generos/delete", data={"id": str(genero.id)})
    assert r.status_code == 302
    assert generos.objects(nombre="Acción").count() == 0


def test_admin_rechaza_subida_no_imagen(client):
    _make_user("admin", "secret")
    client.post("/login", data={"username": "admin", "password": "secret"})
    r = client.post(
        "/admin/articulos/new",
        data={"titulo": "X", "generos": "Acción", "tipo": "anime"},
        content_type="multipart/form-data",
        files={"img": (b"not-an-image", "mal.txt")},
    )
    assert r.status_code == 302
    assert articulos.objects(titulo="X").count() == 0


def test_logout(client):
    _make_user("admin", "secret")
    client.post("/login", data={"username": "admin", "password": "secret"})
    r = client.get("/logout")
    assert r.status_code == 302
    assert client.get("/admin/", follow_redirects=False).status_code == 302