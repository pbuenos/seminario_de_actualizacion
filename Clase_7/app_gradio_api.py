import gradio as gr

from logica import clasificar_api


def analizar(texto: str) -> tuple[str, str]:
    try:
        etiqueta, puntaje = clasificar_api(texto)
    except ValueError as error:
        raise gr.Error(str(error)) from error
    return etiqueta, f"{puntaje:.1%}"


with gr.Blocks(title="Sentimiento con Inference API") as demo:
    gr.Markdown(
        "# Análisis de sentimiento · Inference API\n"
        "La interfaz corre en esta computadora y Hugging Face procesa la frase. "
        "Está preparado para texto en inglés."
    )
    texto = gr.Textbox(label="Frase", placeholder="I love this product")
    boton = gr.Button("Analizar")
    etiqueta = gr.Textbox(label="Etiqueta", interactive=False)
    confianza = gr.Textbox(label="Puntaje del modelo", interactive=False)
    boton.click(analizar, inputs=texto, outputs=[etiqueta, confianza])


if __name__ == "__main__":
    demo.launch()
