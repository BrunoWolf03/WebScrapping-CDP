from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from src.captcha.captchaExtractor import capturar_captcha
from src.captcha.captchaDecoder import enviar_captcha

def identificar_erro_captcha(driver):
    try:
        error_element = driver.find_element(By.ID, "APEX_ERROR_MESSAGE")
        classes = error_element.get_attribute("class")
        
        if "u-hidden" not in classes:
            print("Captcha incorreto detectado.")
            return True
        else:
            print("Captcha correto! Sem mensagem de erro.")
            return False
    except Exception as e:
        print("Elemento de erro não encontrado. Busca bem sucedida.")
        return False


def scrapeData(driver, lista_periodos):

    for periodo in lista_periodos:
        sleep(2)

        period_input = driver.find_element(By.ID, "P54_PERIODO")
        period_input.clear()
        period_input.send_keys(periodo)

        # O campo de ambiente é um dropdown, então precisamos clicar para abrir as opções e depois selecionar a desejada
        ambiente_input = driver.find_element(By.ID, "P54_AMBIENTE")
        ambiente_input.click()
        sleep(1)
        ambiente_option = driver.find_element(By.XPATH, "//option[@value='M']") 
        ambiente_option.click()

        erros = 0
        while erros < 3:
            imgs = capturar_captcha(driver)

            print("Imagens capturadas:", imgs)

            enviar_captcha(driver)

            botao_buscar = driver.find_element(By.ID, "B533104921457386864")
            botao_buscar.click()
            
            sleep(3)
            
            if identificar_erro_captcha(driver):
                erros += 1
                sleep(2)
                continue
            else:
                break
        if erros >= 3:
            return
        # A partir daqui, extraímos os dados da página clicando no botão de exportar para csv
        sleep(2)
        erros = 0
        while erros < 3:
            imgs = capturar_captcha(driver)
            print("Imagens capturadas (Exportação):", imgs)

            enviar_captcha(driver)

            botao_exportar_csv = driver.find_element(By.ID, "B356223574253737337")
            botao_exportar_csv.click()
            
            sleep(3)
            
            if identificar_erro_captcha(driver):
                erros += 1
                sleep(2)
                continue
            else:
                print("Iniciando o download do CSV...")
                sleep(5)
                break
        if erros >= 3:
            return
        
    return