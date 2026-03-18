import google_colab_selenium as gs
import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ------------------------
# DRIVER
# ------------------------
def func_driver():

    driver = gs.Chrome()
    driver.get("https://www.google.com/maps?hl=pt-BR")

    return driver


# ------------------------
# BUSCA
# ------------------------
def func_search(driver, query):

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput"))
    )

    search_box.clear()
    search_box.send_keys(query)

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#searchbox-searchbutton"))
    )

    search_button.click()


# ------------------------
# SCROLL
# ------------------------
def func_scroll(driver, n=10):

    scroll = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
    )

    for _ in range(n):
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", scroll
        )
        time.sleep(2)


# ------------------------
# LIMPEZA TEXTO
# ------------------------
def limpar_texto(texto):

    # remove unicode privado (ícones)
    texto = re.sub(r'[\ue000-\uf8ff]', '', texto)

    # remove padrão "· ícone ·"
    texto = re.sub(r"·\s*·", "·", texto)

    return texto.strip()


# ------------------------
# EXTRAÇÃO
# ------------------------
def func_scrapping(driver):

    places = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Nv2PK"))
    )

    dados = []

    for p in places:

        texto = limpar_texto(p.text)

        partes = re.split(r"\s*·\s*", texto)

        # fallback seguro
        nome = partes[0] if len(partes) > 0 else None
        rating = None
        endereco = None
        status = None

        # tentativa simples de parsing
        for parte in partes:
            if "⭐" in parte or "." in parte:
                rating = parte
            elif "Rua" in parte or "Av" in parte:
                endereco = parte
            elif "Fechado" in parte or "Aberto" in parte:
                status = parte

        dados.append({
            "nome": nome,
            "rating": rating,
            "endereco": endereco,
            "status": status
        })

    return dados


# ------------------------
# MAIN
# ------------------------
def main(query="salão de beleza em Cotia SP"):

    driver = func_driver()

    func_search(driver, query)

    time.sleep(3)

    func_scroll(driver, n=10)

    dados = func_scrapping(driver)

    return dados