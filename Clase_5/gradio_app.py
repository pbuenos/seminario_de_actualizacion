import audioop
import os
import sys

sys.modules.setdefault("pyaudioop", audioop)

import gradio as gr

from logica import crear_saludo


with gr.Blocks(title="Creador de saludos") as demo:
    gr.Markdown("# Creador de saludos\nEscribí un nombre y elegí el estilo.")

    nombre = gr.Textbox(label="Nombre", placeholder="Por ejemplo: Alex")
    estilo = gr.Dropdown(
        choices=["Informal", "Formal"],
        value="Informal",
        label="Estilo del saludo",
    )
    boton = gr.Button("Crear saludo")
    resultado = gr.Textbox(label="Resultado", interactive=False)

    boton.click(
        fn=crear_saludo,
        inputs=[nombre, estilo],
        outputs=resultado,
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
    )
