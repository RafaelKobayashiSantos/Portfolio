# -*- coding: utf-8 -*-
"""ProjetoTrade.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18qpOAItoFM0b23hlC4hVKcXkmlt6aJ9c
"""


import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

# Configuração da página
st.set_page_config(page_title="🏡 Extrator de Imobiliárias", page_icon="🏠", layout="wide")

# Cabeçalho com imagem e título
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEfWkz0vJws3MqB-P9u4BSatDgUZvDDUdG6Q&s", width=200)
st.title("🏡 Extrator de Imobiliárias")
st.write("Cole o código HTML de uma página e extraia automaticamente as informações das imobiliárias, incluindo e-mails dos sites!")

# Regex para e-mails
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Função para extrair e-mails
def extrair_emails(url):
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        emails_encontrados = set()

        for tag in soup.find_all(text=re.compile(email_pattern)):
            emails = re.findall(email_pattern, tag)
            emails_encontrados.update(email.strip() for email in emails)

        return ", ".join(emails_encontrados) if emails_encontrados else None
    except requests.exceptions.RequestException:
        return None

# Input para o código HTML
html = st.text_area("📜 Cole o código HTML aqui", height=200)

if st.button("🚀 Extrair Dados"):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        lista = {'Nome': [], 'Telefone': [], 'Avaliação': [], 'Qtd Avaliações': [], 'Link': [], 'E-mail': []}
        imobiliarias = soup.find_all('div', class_=re.compile('Nv2PK tH5CWc THOPZb'))

        for imobiliaria in imobiliarias:
            nome = imobiliaria.find('div', class_='qBF1Pd fontHeadlineSmall')
            tel = imobiliaria.find('span', class_='UsdlK')
            rate = imobiliaria.find('span', class_='MW4etd')
            qtdrate = imobiliaria.find('span', class_='UY7F9')
            link = imobiliaria.find('a', class_='lcr4fd S9kvJb')

            lista['Nome'].append(nome.text.strip() if nome else None)
            lista['Telefone'].append(tel.text.strip() if tel else None)
            lista['Avaliação'].append(rate.text.strip() if rate else None)
            lista['Qtd Avaliações'].append(qtdrate.text.strip() if qtdrate else None)
            lista['Link'].append(link.get('href') if link else None)

        # Extrai os e-mails dos sites das imobiliárias
        lista['E-mail'] = [extrair_emails(link) if link else None for link in lista['Link']]

        df = pd.DataFrame(lista)

        # Exibe os resultados na tela
        st.write("### 📊 Resultados")
        st.dataframe(df)

        # Permite baixar o Excel
        file_path = "imobiliarias.xlsx"
        df.to_excel(file_path, index=False)
        st.download_button(label="📥 Baixar Excel", data=open(file_path, "rb"), file_name="Imobiliarias.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("⚠️ Cole um código HTML antes de extrair os dados.")
