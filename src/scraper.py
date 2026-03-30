from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


def scrapeData(driver):
    sleep(2)  # Espera 2 segundos para garantir que a página esteja carregada
    period_input = driver.find_element(By.ID, "P54_PERIODO")
    period_input.send_keys("01")
    period_input.send_keys("2023") 
    
    # O campo de ambiente é um dropdown, então precisamos clicar para abrir as opções e depois selecionar a desejada
    ambiente_input = driver.find_element(By.ID, "P54_AMBIENTE")
    ambiente_input.click()
    sleep(1)
    ambiente_option = driver.find_element(By.XPATH, "//option[@value='M']") 
    ambiente_option.click()

    botao_buscar = driver.find_element(By.ID, "B533104921457386864")
    botao_buscar.click()

    return