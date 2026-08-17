"""
Captura screenshots del sitio para el portafolio.

Uso:
    1. Arranca la app (con la BD poblada):
        uv run python app.py
    2. Instala el navegador si no lo has hecho:
        uv run playwright install chromium
    3. Ejecuta este script:
        uv run python tools/screenshots.py [--base http://127.0.0.1:5000]

Guarda las capturas en docs/screenshots/.
Si quieres capturar el dashboard admin autenticado, pasa las credenciales:
        uv run python tools/screenshots.py --admin-user admin --admin-pass "tu-pass"
"""
import argparse
import os
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout, sync_playwright

OUT_DIR = Path("docs/screenshots")
VIEWPORT = {"width": 1440, "height": 900}


def shot(page, name: str) -> None:
    path = OUT_DIR / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"[ok] {path}")


def visit(page, url: str) -> None:
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:5000", help="URL de la app.")
    parser.add_argument("--admin-user", default="")
    parser.add_argument("--admin-pass", default="")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport=VIEWPORT, device_scale_factor=1, locale="es-ES"
        )
        page = context.new_page()

        visit(page, f"{args.base}/")
        shot(page, "home")

        visit(page, f"{args.base}/animes/")
        shot(page, "animes")

        try:
            link = page.locator("a[href*='/animes/']").first
            link.click(timeout=15000)
            page.wait_for_load_state("networkidle", timeout=15000)
            page.wait_for_timeout(600)
            shot(page, "article")
        except PlaywrightTimeout:
            print("[warn] No se encontró un enlace de artículo; se omite la ficha.")

        visit(page, f"{args.base}/login")
        shot(page, "admin-login")

        if args.admin_user and args.admin_pass:
            page.locator('input[name="username"]').fill(args.admin_user)
            page.locator('input[name="password"]').fill(args.admin_pass)
            page.locator('input[type="submit"]').click()
            page.wait_for_url("**/admin/**", timeout=15000)
            page.wait_for_timeout(600)
            shot(page, "admin-dashboard")

        browser.close()


if __name__ == "__main__":
    main()