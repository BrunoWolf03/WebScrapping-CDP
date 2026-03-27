from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytesseract 
from PIL import Image 
import cv2
import numpy as np
from time import sleep

from src.captcha.captchaExtractor import capturar_captcha

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
url = "https://cdp.anp.gov.br/ords/r/cdp_apex/consulta-dados-publicos-cdp/consulta-produ%C3%A7%C3%A3o-por-po%C3%A7o"
driver.get(url)

input("A página carregou completamente? Se sim, aperta ENTER para quebrar o CAPTCHA...")

print("Iniciando processo de quebra de CAPTCHA...")

try:
    caminhos_imagens = capturar_captcha(driver)

    texto_final_captcha = ""

    print(f"Detectadas {len(caminhos_imagens)} imagens de caracteres. Iniciando OCR...")

    # Configuração do Tesseract para este cenário:
    # --psm 10: Trata a imagem como um único caractere (fundamental aqui)
    # whitelist: Força a ler apenas letras (maiúsculas/minúsculas) e números, ignorando ruídos.
    tesseract_config = r'--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i, caminho in enumerate(caminhos_imagens):
        try:
            # 1. Lê a imagem com OpenCV preservando o canal Alpha (transparência)
            imagem_cv = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)
            
            # 2. Verifica se a imagem tem fundo transparente (4 canais: BGRA)
            if imagem_cv.shape[2] == 4:
                # Cria um fundo branco do mesmo tamanho da imagem
                fundo_branco = 255 * np.ones_like(imagem_cv[:, :, :3])
                
                # Extrai o canal alpha (transparência) como uma máscara
                alpha = imagem_cv[:, :, 3] / 255.0
                
                # Mescla a imagem com o fundo branco usando a máscara
                for c in range(3):
                    fundo_branco[:, :, c] = (alpha * imagem_cv[:, :, c] + (1 - alpha) * fundo_branco[:, :, c])
                
                # A imagem agora tem fundo branco sólido (3 canais: BGR)
                imagem_cv = fundo_branco.astype(np.uint8)

            # 3. Converte para escala de cinza
            imagem_cinza = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2GRAY)
            
            
            imagem_ampliada = cv2.resize(imagem_cinza, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            
            # 5. Binarização usando limiar de Otsu (Deixa totalmente em Preto e Branco)
            _, imagem_binarizada = cv2.threshold(imagem_ampliada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Passa a imagem tratada direto para o Tesseract
            caractere_extraido = pytesseract.image_to_string(imagem_binarizada, config=tesseract_config)
            
            # Limpa espaços e quebras de linha
            caractere_limpo = caractere_extraido.strip()
            
            # Pega sempre apenas 1 caractere. Como sabemos que a caixa da imagem é
            # de UMA única letra, evitamos as "alucinações" do Tesseract adicionando a mais
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
        print("Não consegui encontrar o campo de input do CAPTCHA para preencher automatically.")

    
    sleep(3)

except Exception as e:
    print(f"Ocorreu um erro geral: {e}")

finally:
    driver.quit()
    print("Navegador fechado.")