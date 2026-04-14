import gradio as gr
import requests

def analisar_imagem(imagem_path):
    if imagem_path is None:
        return "", "", ""

    try:
        with open(imagem_path, "rb") as f:
            files = {"file": f}
            response = requests.post("http://api-visao:8081/analisar", files=files)

        if response.status_code == 200:
            dados = response.json()

            descricao = dados.get("descricao", "")
            status = dados.get("status_db", "")
            ocr = dados.get("ocr") or ""

            return descricao, ocr, status

        return "", "", f"Erro: {response.status_code}"

    except Exception as e:
        return "", "", f"Erro: {str(e)}"


with gr.Blocks() as demo:

    gr.Markdown("AI 👁️ DESCRIPTION", elem_classes="titulo")

    with gr.Column(elem_classes="container"):

        # CARD DA IMAGEM
        with gr.Column(elem_classes="card"):
            imagem_input = gr.Image(type="filepath", show_label=False)

        botao = gr.Button("Analisar")

        descricao_output = gr.Markdown(elem_classes="descricao")
        ocr_output = gr.Markdown(elem_classes="ocr")
        status_output = gr.Markdown(elem_classes="status")

    def atualizar(imagem):
        desc, ocr, status = analisar_imagem(imagem)

        desc_md = f"Descrição AI: {desc}" if desc else ""
        ocr_md = f"Texto extraído: {ocr}" if ocr else ""
        status_md = f"{status}" if status else ""

        return desc_md, ocr_md, status_md

    botao.click(
        fn=atualizar,
        inputs=imagem_input,
        outputs=[descricao_output, ocr_output, status_output]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=7861,
    css="""
    .gradio-container {
    background: linear-gradient(180deg, #760DBE 0%, #210E2E 100%) !important;
    min-height: 100vh;
}

.titulo * {
    font-size: 38px !important;
    font-weight: 800 !important;
    text-align: center;
    color: white !important;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.25);
}

.container {
    max-width: 420px;
    margin: auto;
    margin-top: 40px;
}

.card {
    background: white;
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

button {
    border-radius: 12px !important;
    font-weight: 600;
}

.descricao* {
    margin-top: 12px;
    color: white !important;
    font-size: 15px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.20);
}

.ocr* {
    margin-top: 10px;
    color: white !important;
    font-size: 15px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.20);
}

.status {
    margin-top: 8px;
    color: white !important;
    font-size: 10px;
}
"""
)