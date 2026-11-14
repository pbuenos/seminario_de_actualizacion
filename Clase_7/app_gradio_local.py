import gradio as gr

from logica import clasificar_local


def analizar(texto: str) -> tuple[str, str]:
    try:
        etiqueta, puntaje = clasificar_local(texto)
    except ValueError as error:
        raise gr.Error(str(error)) from error
    return etiqueta, f"{puntaje:.1%}"


with gr.Blocks(title="Sentimiento con pipeline local") as demo:
    gr.Markdown(
        "# Análisis de sentimiento · pipeline local\n"
        "El modelo se descarga y se ejecuta en esta computadora. "
        "Está preparado para texto en inglés."
    )
    texto = gr.Textbox(label="Frase", placeholder="I love this product")
    boton = gr.Button("Analizar")
    etiqueta = gr.Textbox(label="Etiqueta", interactive=False)
    confianza = gr.Textbox(label="Puntaje del modelo", interactive=False)
    boton.click(analizar, inputs=texto, outputs=[etiqueta, confianza])


if __name__ == "__main__":
    demo.launch()
