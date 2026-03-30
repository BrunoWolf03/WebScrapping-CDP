from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from src.scraper import scrapeData

# Inicia o driver com as opções configuradas
driver = webdriver.Chrome()
driver.get("https://cdp.anp.gov.br/ords/r/cdp_apex/consulta-dados-publicos-cdp/consulta-produ%C3%A7%C3%A3o-por-po%C3%A7o")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "anp_p54_captcha"))
)

lista_periodos = ["012023", "022023", "032023", "042023", "052023", "062023", "072023", "082023", "092023", "102023", "112023", "122023",
                    "012024", "022024", "032024", "042024", "052024", "062024", "072024", "082024", "092024", "102024", "112024", "122024",
                    "012025", "022025", "032025", "042025", "052025", "062025", "072025", "082025", "092025", "102025", "112025", "122025"]

sleep(2)
scrapeData(driver, lista_periodos)
sleep(5) 