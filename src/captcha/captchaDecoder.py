from selenium.webdriver.common.by import By
from collections import Counter
from PIL import Image, ImageEnhance
import ddddocr
import io
from time import sleep

from src.captcha.captchaExtractor import capturar_captcha

CHARSET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

def preprocessar_imagem(caminho: str) -> bytes:
    img = Image.open(caminho).convert("L")
    img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(2.5)
    img = img.point(lambda x: 0 if x < 140 else 255, '1').convert("L")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def ocr_com_votacao(ocr, img_bytes: bytes, tentativas: int = 3) -> str:
    resultados = []
    for _ in range(tentativas):
        resultado = ocr.classification(img_bytes)
        limpo = ''.join(c for c in resultado.upper() if c in CHARSET)
        if limpo:
            resultados.append(limpo[0])
    
    if not resultados:
        return "I"
    
    return Counter(resultados).most_common(1)[0][0]

def enviar_captcha(driver):
    print("Iniciando processo de quebra de CAPTCHA...")

    try:
        caminhos_imagens = capturar_captcha(driver)
        texto_final_captcha = ""

        print(f"Detectadas {len(caminhos_imagens)} imagens de caracteres. Iniciando OCR com ddddocr...")

        ocr = ddddocr.DdddOcr(show_ad=False)

        for i, caminho in enumerate(caminhos_imagens):
            try:
                img_bytes = preprocessar_imagem(caminho)
                caractere = ocr_com_votacao(ocr, img_bytes)
                texto_final_captcha += caractere
                print(f"  Caractere {i+1}: '{caractere}'")

            except Exception as e_ocr:
                print(f"Erro ao ler caractere {i}: {e_ocr}")
                texto_final_captcha += "I"

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