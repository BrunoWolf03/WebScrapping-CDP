from selenium.webdriver.common.by import By
import ddddocr
from time import sleep

from src.captcha.captchaExtractor import capturar_captcha

def enviar_captcha(driver):

    print("Iniciando processo de quebra de CAPTCHA...")

    try:
        caminhos_imagens = capturar_captcha(driver)

        texto_final_captcha = ""

        print(f"Detectadas {len(caminhos_imagens)} imagens de caracteres. Iniciando OCR com ddddocr...")

        # Inicializa o ddddocr (show_ad=False esconde a propaganda da biblioteca no console)
        ocr = ddddocr.DdddOcr(show_ad=False)

        for i, caminho in enumerate(caminhos_imagens):
            try:
                # O ddddocr não precisa de tratamento com OpenCV. 
                # Ele lê a imagem crua (bruta) diretamente em formato de bytes.
                with open(caminho, "rb") as f:
                    img_bytes = f.read()

                # Chama a rede neural para inferir o caractere
                caractere_extraido = ocr.classification(img_bytes)
                
                caractere_limpo = caractere_extraido.strip()
                
                # Caso a IA ache mais de uma letra, forçamos o limitador de 1
                if caractere_limpo:
                    texto_final_captcha += caractere_limpo[0]
                else:
                    texto_final_captcha += "?"
            except Exception as e_ocr:
                print(f"Erro ao ler caractere {i}: {e_ocr}")
                texto_final_captcha += "?"

        print("-" * 30)
        print(f"RESULTADO DO CAPTCHA: '{texto_final_captcha}'")
        print("-" * 30)

        try:
            input_captcha_page = driver.find_element(By.ID, 'P54_CAPTCHA')
            input_captcha_page.send_keys(texto_final_captcha)
            print("Campo do CAPTCHA preenchido na página!")
        except:
            print("Não consegui encontrar o campo de input do CAPTCHA para preencher automaticamente.")
        sleep(3)

    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")

    return