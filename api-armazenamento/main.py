import os
import sqlite3
import uuid
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

DIRETORIO_DADOS = "/dados"
DB_PATH = f"{DIRETORIO_DADOS}/banco.db"

# Garante que o diretório existe (será mapeado no volume do Docker)
os.makedirs(DIRETORIO_DADOS, exist_ok=True)


# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS imagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT,
            rotulo TEXT
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.post("/salvar")
async def salvar_dados(file: UploadFile = File(...), rotulo: str = Form(...)):
    # 1. Salva o arquivo físico da imagem
    nome_unico = f"{uuid.uuid4()}_{file.filename}"
    caminho_arquivo = os.path.join(DIRETORIO_DADOS, nome_unico)
    with open(caminho_arquivo, "wb") as f:
        f.write(await file.read())

    # 2. Salva o registro no banco de dados com o rótulo da IA
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO imagens (nome_arquivo, rotulo) VALUES (?, ?)",
        (nome_unico, rotulo),
    )
    conn.commit()
    conn.close()

    return {"mensagem": "Imagem e rótulo armazenados com sucesso"}
