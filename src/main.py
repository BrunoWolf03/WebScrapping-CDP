from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.captcha.captchaExtractor import capturar_captcha
from src.captcha.captchaDecoder import enviar_captcha

driver = webdriver.Chrome()
driver.get("https://cdp.anp.gov.br/ords/r/cdp_apex/consulta-dados-publicos-cdp/consulta-produ%C3%A7%C3%A3o-por-po%C3%A7o")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "anp_p54_captcha"))
)

imgs = capturar_captcha(driver)

print("Imagens capturadas:", imgs)

enviar_captcha(driver)