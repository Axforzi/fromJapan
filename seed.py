"""
Script de inicialización de la base de datos para From Japan.

Puebla la base de datos consultando la API pública de AniList
(https://anilist.co) y descargando las portadas reales de los títulos.

Crea:
  - Un usuario administrador (contraseña encriptada con Werkzeug).
  - Géneros base (derivados de los artículos).
  - 15 animes, 15 mangas y 15 novelas ligeras (portadas reales).
  - Entradas de carrusel para la portada.

Uso:
    uv run python seed.py
    uv run python seed.py --admin-pass 1234
"""
import argparse
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv
from mongoengine import connect

from schema.index import articulos, carrusel, generos, users

load_dotenv()

connect(host=os.getenv("MONGO_URI"), uuidRepresentation="standard")

DEFAULT_ADMIN = "admin"
DEFAULT_PASSWORD = "fromjapan-admin"

ANILIST_ENDPOINT = "https://graphql.anilist.co"
ARTICULOS_POR_TIPO = 15
MAX_LINKS_POR_ARTICULO = 6

# Solo se guardan enlaces a tiendas/plataformas confiables donde comprar o ver el material.
# (J-Novel Club se excluye: AniList solo enlaza a su tienda EU en francés.)
PLATAFORMAS_CONFIABLES = {
    "anime": {"Crunchyroll", "Netflix", "Hulu", "Amazon Prime Video"},
    "manga": {"VIZ", "Yen Press", "Kodansha USA", "Seven Seas Entertainment", "MANGA Plus", "Amazon", "Google Play Books", "Kobo"},
    "novela": {"VIZ", "Yen Press", "Kodansha USA", "Seven Seas Entertainment", "MANGA Plus", "Amazon", "Google Play Books", "Kobo"},
}

# Segmentos de idioma en el path de una URL que no son inglés ni español (se descartan).
IDIOMAS_NO_PERMITIDOS = ("/fr/", "/de/", "/ja/", "/ko/", "/zh/", "/it/", "/pt/", "/ru/", "/nl/")

# Fuente de logo fiable por plataforma (se descargan a static/img/logos/).
LOGO_POR_PLATAFORMA = {
    "Crunchyroll": "local:crunchyroll.png",
    "Amazon Prime Video": "local:Amazon-Logo.png",
    "Netflix": "https://www.netflix.com/favicon.ico",
    "Hulu": "https://www.google.com/s2/favicons?domain=www.hulu.com&sz=128",
    "VIZ": "https://www.viz.com/favicon.ico",
    "Yen Press": "https://yenpress.com/favicon.ico",
    "Kodansha USA": "https://kodansha.us/favicon.ico",
    "Seven Seas Entertainment": "https://sevenseasentertainment.com/favicon.ico",
    "MANGA Plus": "https://www.google.com/s2/favicons?domain=mangaplus.shueisha.co.jp&sz=128",
    "Amazon": "local:Amazon-Logo.png",
    "Google Play Books": "https://www.google.com/s2/favicons?domain=play.google.com&sz=128",
    "Kobo": "https://www.google.com/s2/favicons?domain=kobo.com&sz=128",
}

# Traducción de géneros de AniList (inglés) al catálogo (español).
GENRES_TRADUCCION = {
    "Action": "Acción", "Adventure": "Aventura", "Comedy": "Comedia",
    "Drama": "Drama", "Fantasy": "Fantasía", "Romance": "Romance",
    "Sci-Fi": "Sci-Fi", "Seinen": "Seinen", "Horror": "Terror",
    "Slice of Life": "Slice of life", "Mystery": "Misterio",
    "Thriller": "Thriller", "Psychological": "Psicológico",
    "Supernatural": "Sobrenatural", "Sports": "Deportes", "Music": "Música",
    "School": "Escolar", "Mecha": "Mecha", "Magic": "Magia",
    "Ecchi": "Ecchi", "Historical": "Histórico", "Military": "Militar",
    "Space": "Espacio", "Crime": "Crimen", "Parody": "Parodia",
    "Isekai": "Isekai", "Shounen": "Shōnen", "Shoujo": "Shōjo",
}

QUERY = """
query ($type: MediaType, $format: MediaFormat, $perPage: Int) {
  Page(page: 1, perPage: $perPage) {
    media(type: $type, format: $format, sort: POPULARITY_DESC) {
      title { romaji english }
      coverImage { extraLarge }
      genres
      description(asHtml: false)
      status
      studios(isMain: true) { nodes { name } }
      staff(perPage: 1, sort: RELEVANCE) { nodes { name { full } } }
      externalLinks { site type url }
      siteUrl
    }
  }
}
"""


def fetch_from_anilist(tipo: str, format_filter: str | None = None) -> list:
    """Obtiene títulos desde AniList para un tipo (y formato opcional)."""
    variables = {
        "type": tipo,
        "perPage": ARTICULOS_POR_TIPO,
    }
    if format_filter:
        variables["format"] = format_filter

    payload = json.dumps({"query": QUERY, "variables": variables})

    req = urllib.request.Request(
        ANILIST_ENDPOINT,
        data=payload.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "fromJapan/1.0 (portfolio project)",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")
    return json.loads(data)["data"]["Page"]["media"]


def recortar_por_palabra(texto: str, limite: int) -> str:
    """Recorta un texto al último espacio antes de `limite` sin partir palabras."""
    if len(texto) <= limite:
        return texto
    corte = texto.rfind(" ", 0, limite)
    if corte == -1:
        corte = limite
    return texto[:corte]


def _fragmentar(texto: str, limite: int = 450) -> list[str]:
    """Divide un texto en trozos por límite de palabra, sin partir palabras."""
    if len(texto) <= limite:
        return [texto]
    trozos = []
    while texto:
        corte = texto.rfind(" ", 0, limite)
        if corte == -1:
            corte = min(len(texto), limite)
        trozos.append(texto[:corte].strip())
        texto = texto[corte:].strip()
    return [t for t in trozos if t]


def _traducir_gtx(texto: str, source: str, target: str) -> str | None:
    """Traduce con Google Translate (endpoint libre, sin clave)."""
    url = "https://translate.googleapis.com/translate_a/single"
    params = urllib.parse.urlencode({
        "client": "gtx", "sl": source, "tl": target,
        "dt": "t", "q": texto,
    })
    req = urllib.request.Request(f"{url}?{params}", headers={"User-Agent": "fromJapan/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    traduccion = "".join(segmento[0] for segmento in data[0] if segmento[0])
    return traduccion.strip() if traduccion else None


def _traducir_mymemory(texto: str, source: str, target: str) -> str | None:
    """Traduce con MyMemory (gratis, ~500 chars por petición)."""
    query = urllib.parse.urlencode({"q": texto, "langpair": f"{source}|{target}"})
    url = f"https://api.mymemory.translated.net/get?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": "fromJapan/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    traduccion = (data.get("responseData") or {}).get("translatedText") or ""
    if traduccion and data.get("responseStatus") == 200:
        return traduccion.strip()
    return None


def traducir_texto(texto: str, source: str = "en", target: str = "es") -> str:
    """
    Traduce texto con Google Translate (maneja textos largos) y, si falla,
    con MyMemory fragmentando en trozos. Devuelve el texto original si ambas fallan.
    """
    texto = texto.strip()
    if not texto:
        return ""

    # Google Translate traduce el texto completo en una sola llamada.
    try:
        traduccion = _traducir_gtx(texto, source, target)
        if traduccion:
            return traduccion
    except (urllib.error.URLError, ValueError, IndexError):
        pass

    # MyMemory free limita a ~500 chars por petición: se fragmenta y concatena.
    try:
        partes = [_traducir_mymemory(trozo, source, target) for trozo in _fragmentar(texto)]
        if all(partes):
            return " ".join(p.strip() for p in partes)
    except (urllib.error.URLError, ValueError, KeyError):
        pass

    return texto


def traducir_generos(genres: list[str]) -> list[str]:
    """Traduce los géneros de AniList a español, omitiendo los no mapeados."""
    return [GENRES_TRADUCCION.get(g, g) for g in genres]


def limpiar_descripcion(descripcion: str | None) -> str:
    """Limpia HTML de la descripción y la recorta a un párrafo razonable."""
    if not descripcion:
        return ""
    texto = html.unescape(re.sub(r"<[^>]+>", " ", descripcion))
    texto = re.sub(r"\s+", " ", texto).strip()
    return recortar_por_palabra(texto, 2000)


def estado_to_es(estado: str) -> str:
    """Mapea el estado de AniList a los valores usados en el catálogo."""
    if estado in ("FINISHED", "CANCELLED"):
        return "Finalizado"
    return "En emisión"


def descargar_imagen(url: str, destino: str) -> None:
    """Descarga una imagen desde una URL y la guarda en `destino`."""
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if os.path.exists(destino):
        return
    req = urllib.request.Request(url, headers={"User-Agent": "fromJapan/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(destino, "wb") as f:
            f.write(resp.read())


def _slug_plataforma(site: str) -> str:
    """Convierte el nombre de una plataforma en un slug de archivo seguro."""
    base = re.sub(r"[^a-z0-9]+", "_", site.lower()).strip("_")
    return base or "plataforma"


def descargar_logo(site: str) -> str:
    """
    Descarga/copia el logo de una plataforma a static/img/logos/ y
    devuelve su ruta estática. Devuelve "" si no hay fuente disponible.
    """
    fuente = LOGO_POR_PLATAFORMA.get(site)
    if fuente and fuente.startswith("local:"):
        archivo = fuente.split(":", 1)[1]
        ruta = f"static/img/{archivo}"
        if os.path.exists(ruta):
            return f"/static/img/{archivo}"
        return ""

    slug = _slug_plataforma(site)
    if not fuente:
        return ""

    for ext in (".png", ".ico", ".jpg", ".webp"):
        ruta_existente = f"static/img/logos/{slug}{ext}"
        if os.path.exists(ruta_existente):
            return f"/static/img/logos/{slug}{ext}"

    try:
        req = urllib.request.Request(fuente, headers={"User-Agent": "fromJapan/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            contenido = resp.read()
        if resp.status != 200 or not contenido:
            return ""

        content_type = resp.headers.get("Content-Type", "").lower()
        if "x-icon" in content_type or "microsoft.icon" in content_type:
            ext = ".ico"
        elif "jpeg" in content_type or "jpg" in content_type:
            ext = ".jpg"
        elif "webp" in content_type:
            ext = ".webp"
        else:
            ext = ".png"

        destino = f"static/img/logos/{slug}{ext}"
        ruta_estatica = f"/static/img/logos/{slug}{ext}"
        if os.path.exists(destino):
            return ruta_estatica
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "wb") as f:
            f.write(contenido)
        return ruta_estatica
    except (urllib.error.URLError, ValueError):
        return ""


def extraer_links(media: dict, tipo: str) -> list[dict]:
    """
    Extrae los enlaces de tiendas/plataformas confiables para un título de AniList.
    Filtra por la whitelist por tipo, descarta URLs en idiomas no en/es,
    añade el logo local y limita a MAX_LINKS_POR_ARTICULO.
    """
    confiables = PLATAFORMAS_CONFIABLES.get(tipo, set())
    enlaces = []
    vistos = set()
    for link in media.get("externalLinks") or []:
        site = link.get("site")
        tipo_link = link.get("type")
        url = link.get("url")
        if tipo_link == "SOCIAL" or not site or not url:
            continue
        if site not in confiables:
            continue
        if any(seg in url.lower() for seg in IDIOMAS_NO_PERMITIDOS):
            continue
        if site in vistos:
            continue
        vistos.add(site)
        enlaces.append({"site": site, "url": url, "logo": descargar_logo(site)})
        if len(enlaces) >= MAX_LINKS_POR_ARTICULO:
            break
    return enlaces


def nombre_seguro(titulo: str, idx: int) -> str:
    """Convierte el título en un nombre de archivo seguro."""
    base = re.sub(r"[^a-z0-9]+", "_", titulo.lower()).strip("_")
    return f"cover_{idx:02d}_{base[:40] or 'untitled'}"


def build_articulo(media: dict, tipo: str, idx: int) -> dict:
    """Convierte un objeto de AniList en un documento de `articulos`."""
    titulo = media["title"]["romaji"] or media["title"]["english"]
    filename = nombre_seguro(f"{tipo}_{titulo}", idx)
    ext = os.path.splitext(media["coverImage"]["extraLarge"].split("?")[0])[1] or ".jpg"

    if tipo == "anime":
        studios = media.get("studios", {}).get("nodes") or []
        autor = studios[0]["name"] if studios else "Desconocido"
    else:
        staff = media.get("staff", {}).get("nodes") or []
        autor = staff[0]["name"]["full"] if staff else "Desconocido"

    portada = f"/static/img/portadas/{filename}{ext}"
    descargar_imagen(media["coverImage"]["extraLarge"], os.path.join("static", "img", "portadas", f"{filename}{ext}"))

    sinopsis_en = limpiar_descripcion(media.get("description"))
    sinopsis = traducir_texto(sinopsis_en) or sinopsis_en
    sinopsis = recortar_por_palabra(sinopsis, 2000)
    links = extraer_links(media, tipo)

    return {
        "titulo": titulo,
        "sipnosis": sinopsis,
        "tipo": tipo,
        "estado": estado_to_es(media["status"]),
        "generos": traducir_generos(media.get("genres") or []),
        "autor": autor,
        "link": (links[0]["url"] if links else media.get("siteUrl") or ""),
        "links": links,
        "portada": portada,
    }


def create_admin(admin: str, password: str) -> None:
    if users.objects(username=admin).first():
        print(f"[skip] Admin '{admin}' ya existe.")
        return
    user = users(username=admin)
    user.set_password(password)
    user.save()
    print(f"[ok] Admin creado: '{admin}' / password: {password}")


def create_articles() -> None:
    """Consulta AniList y guarda animes, mangas y novelas con sus portadas."""
    tipos = [("anime", "ANIME", None), ("manga", "MANGA", "MANGA"), ("novela", "MANGA", "NOVEL")]
    generos_en_uso = set()

    for tipo, api_tipo, api_format in tipos:
        print(f"[..] Consultando {tipo} en AniList...")
        media_list = fetch_from_anilist(api_tipo, api_format)

        for idx, media in enumerate(media_list):
            titulo = media["title"]["romaji"] or media["title"]["english"]
            if articulos.objects(titulo=titulo, tipo=tipo).first():
                print(f"[skip] Artículo '{titulo}' ya existe.")
                continue

            articulo = build_articulo(media, tipo, idx)
            articulos(**articulo).save()
            generos_en_uso.update(articulo["generos"])
            print(f"[ok] Artículo creado: '{titulo}'")

        time.sleep(1)

    # Géneros derivados de los artículos reales.
    for nombre in sorted(generos_en_uso):
        if not generos.objects(nombre=nombre).first():
            generos(nombre=nombre).save()
            print(f"[ok] Género: '{nombre}'")


def create_carrusel() -> None:
    """Toma 3 portadas reales ya guardadas como carrusel de la portada."""
    top = articulos.objects(tipo="anime").order_by("-createdAt").limit(3)
    for i, a in enumerate(top):
        if carrusel.objects(titulo=a.titulo).first():
            print(f"[skip] Carrusel '{a.titulo}' ya existe.")
            continue
        carrusel(titulo=a.titulo, link=a.link or "https://anilist.co", ruta=a.portada).save()
        print(f"[ok] Carrusel creado: '{a.titulo}'")


def wipe_db() -> None:
    """Elimina todos los documentos de la base de datos (se usa en --clean)."""
    for doc in (articulos, carrusel, generos, users):
        count = doc.objects.count()
        doc.drop_collection()
        print(f"[ok] Colección '{doc._meta['collection']}' vaciada ({count} documentos).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inicializa la BD de From Japan con contenido real de AniList.")
    parser.add_argument("--admin", default=DEFAULT_ADMIN, help="Nombre del usuario admin.")
    parser.add_argument("--admin-pass", default=DEFAULT_PASSWORD, help="Contraseña del admin.")
    parser.add_argument("--clean", action="store_true", help="Vaciar la BD antes de poblar.")
    parser.add_argument("--no-admin", action="store_true", help="Omitir creación del admin.")
    args = parser.parse_args()

    if args.clean:
        wipe_db()

    if not args.no_admin:
        create_admin(args.admin, args.admin_pass)

    create_articles()
    create_carrusel()
    print("Seed completado.")


if __name__ == "__main__":
    main()