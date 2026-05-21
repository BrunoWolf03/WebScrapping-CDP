from selenium.webdriver.common.by import By
import requests
import os

def capturar_captcha(driver, output_dir="captcha_imgs"):
    # pegar div do captcha
    captcha_div = driver.find_element(By.ID, "anp_p54_captcha")

    # pegar imagens
    imgs = captcha_div.find_elements(By.TAG_NAME, "img")

    os.makedirs(output_dir, exist_ok=True)

    # sessão com cookies do Selenium
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    caminhos = []

    for i, img in enumerate(imgs):
        src = img.get_attribute("src")

        if src.startswith("www_flow"):
            src = "https://cdp.anp.gov.br/ords/" + src

        response = session.get(src)

        path = os.path.join(output_dir, f"img_{i}.png")

        with open(path, "wb") as f:
            f.write(response.content)

        caminhos.append(path)

    return caminhos