import io
import requests
from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
from PIL import Image, ImageFilter
import pytesseract
from deep_translator import GoogleTranslator

app = FastAPI()

print("Carregando modelo de descrição de imagem...")
gerador_descricao = pipeline(
    "image-to-text",
    model="Salesforce/blip-image-captioning-base"
)

@app.post("/analisar")
async def analisar_imagem(file: UploadFile = File(...)):
    # Lê a imagem
    conteudo = await file.read()
    imagem = Image.open(io.BytesIO(conteudo)).convert("RGB")

    resultado = gerador_descricao(imagem)
    descricao_en = resultado[0]["generated_text"]

    descricao = GoogleTranslator(
    source='auto',
    target='pt'
    ).translate(descricao_en)

    # Informações da imagem
    largura, altura = imagem.size
    formato = imagem.format
    tamanho_kb = round(len(conteudo) / 1024, 2)

    # OCR
    imagem_ocr = imagem.convert("L")
    imagem_ocr = imagem_ocr.point(lambda x: 0 if x < 140 else 255)
    imagem_ocr = imagem_ocr.filter(ImageFilter.MedianFilter())

    texto_extraido = pytesseract.image_to_string(
        imagem_ocr,
        lang="por",
        config="--oem 3 --psm 6"
    )

    texto_extraido = texto_extraido.strip()

    linhas = texto_extraido.split("\n")

    linhas_filtradas = []
    for l in linhas:
        l = l.strip()

        if len(l) < 5:
            continue

        if sum(c.isalpha() for c in l) < len(l) * 0.6:
            continue

        linhas_filtradas.append(l)
        texto_extraido = "\n".join(linhas_filtradas)

    # limpeza final
    texto_extraido = (
        texto_extraido
        .replace("|", "")
        .replace("#", "")
        .replace("~", "")
    )

    files = {"file": (file.filename, conteudo, file.content_type)}
    data = {"rotulo": descricao}

    try:
        res_db = requests.post(
            "http://api-armazenamento:8082/salvar",
            files=files,
            data=data
        )
        status_db = f"{res_db.status_code} - {res_db.text}"
    except Exception as e:
        status_db = f"Erro: {str(e)}"

    response = {
    "descricao": descricao,
    "status_db": status_db
    }
    if texto_extraido:
        response["ocr"] = texto_extraido

    return response