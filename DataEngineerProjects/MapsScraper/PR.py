

from playwright.sync_api import sync_playwright
import time
import re


# ------------------------
# LIMPEZA (igual você já fazia)
# ------------------------
def limpar_texto(texto):

    texto = re.sub(r'[\ue000-\uf8ff]', '', texto)
    texto = texto.strip()

    return texto


# ------------------------
# SCRAPER
# ------------------------
def main(query="salão de beleza em Cotia SP"):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # abre maps
        page.goto("https://www.google.com/maps")

        # busca (bem mais simples que selenium)
        page.fill('input[name="q"]', query)
        page.press('input[name="q"]', "Enter")

        # espera resultados carregarem
        page.wait_for_selector("div[role='feed']")

        # scroll
        for _ in range(10):
            page.mouse.wheel(0, 3000)
            time.sleep(1)

        # pega os lugares
        places = page.locator("div.Nv2PK")

        dados = []

        for i in range(places.count()):

            texto = places.nth(i).inner_text()

            texto = limpar_texto(texto)

            dados.append(texto)

        browser.close()

        return dados