from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

navegador = webdriver.Chrome()

sleep(2)

navegador.maximize_window()
navegador.get('https://cdp.anp.gov.br/ords/r/cdp_apex/consulta-dados-publicos-cdp/consulta-produção-por-poço')


navegador.quit()