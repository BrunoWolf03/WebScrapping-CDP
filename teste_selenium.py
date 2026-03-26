from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os

driver = webdriver.Chrome()
driver.get("https://cdp.anp.gov.br/ords/r/cdp_apex/consulta-dados-publicos-cdp/consulta-produ%C3%A7%C3%A3o-por-po%C3%A7o")

input("Resolve carregamento inicial e aperta ENTER...")

# pegar div do captcha
captcha_div = driver.find_element(By.ID, "anp_p54_captcha")

# pegar todas as imagens dentro dela
imgs = captcha_div.find_elements(By.TAG_NAME, "img")

# criar pasta
os.makedirs("captcha_imgs", exist_ok=True)

# pegar cookies do navegador (IMPORTANTE)
cookies = driver.get_cookies()
session = requests.Session()

for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# baixar imagens
for i, img in enumerate(imgs):
    src = img.get_attribute("src")

    # completar URL se vier relativa
    if src.startswith("www_flow"):
        src = "https://cdp.anp.gov.br/ords/" + src

    response = session.get(src)

    with open(f"captcha_imgs/img_{i}.png", "wb") as f:
        f.write(response.content)

    print(f"Imagem {i} salva:", src)