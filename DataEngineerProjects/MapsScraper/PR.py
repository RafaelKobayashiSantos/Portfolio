import asyncio
from playwright.async_api import async_playwright
import time
import re


# ------------------------
# LIMPEZA INICIAL
# ------------------------
def limpar_texto(texto):

    texto = re.sub(r'[\ue000-\uf8ff]', '', texto)
    return texto.strip()


# ------------------------
# SCRAPER
# ------------------------
async def main(query):

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # abre maps
        await page.goto("https://www.google.com/maps?hl=pt-BR")

        # busca
        await page.fill('input[name="q"]', query)
        await page.press('input[name="q"]', "Enter")

        # espera resultados
        await page.wait_for_selector("div[role='feed']")

        # scroll
        feed = page.locator('div[role="feed"]')

        max_time = 30

        timer = time.time()

        for _ in range(20):

            await feed.evaluate("el => el.scrollTop = el.scrollHeight")
            await asyncio.sleep(1)

            places = page.locator("div.Nv2PK")
            count = await places.count()

            print("Resultados:", count)

            if count >=80:
                break

            if time.time() - timer > max_time:
                print("⏱️ Tempo limite atingido")
                break

            last_count = count

        print('Extração concluída')
        # pega os lugares
        places = page.locator("div[role='article']")

        dados = []

        count = await places.count()

        for i in range(count):

            texto = await places.nth(i).inner_text()

            texto = limpar_texto(texto)

            dados.append(texto)

        await browser.close()

        return dados
