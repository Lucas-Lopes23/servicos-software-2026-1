import gradio as gr
import requests


def processa_audio(audio_path):
    if audio_path is None:
        return "Nenhum áudio recebido."

    # Lê o arquivo de áudio capturado pelo Gradio
    with open(audio_path, "rb") as f:
        files = {"file": ("audio.wav", f, "audio/wav")}

        # Faz a requisição para o container backend-json na porta 8080
        try:
            response = requests.post(
                "http://backend-json:8080/transcrever", files=files
            )
            if response.status_code == 200:
                return response.json().get("texto", "Erro ao extrair texto.")
            else:
                return f"Erro no servidor: {response.status_code}"
        except Exception as e:
            return f"Erro de conexão com o backend: {str(e)}"


# Interface atualizada para entrada de Áudio
demo = gr.Interface(
    fn=processa_audio,
    inputs=gr.Audio(type="filepath", label="Grave sua voz ou envie um áudio"),
    outputs=gr.Textbox(label="Texto Transcrito (Prompt para IA)"),
    title="🎙️ Assistente de Voz para IA",
    description="Grave seu áudio. O Gradio enviará para o Backend via API, que converterá para texto usando IA.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
