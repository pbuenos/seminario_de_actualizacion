import audioop
import sys

sys.modules.setdefault("pyaudioop", audioop)

import gradio as gr


def crear_saludo(nombre: str, estilo: str) -> str:
    nombre = nombre.strip()
    if not nombre:
        return "Escribí tu nombre para crear un saludo."

    if estilo == "Formal":
        return f"Buenos días, {nombre}. ¿Cómo está?"
    return f"¡Hola, {nombre}! ¿Cómo estás?"


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
    demo.launch()
