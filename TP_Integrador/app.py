import os
import sys
from urllib.parse import urlparse

if sys.version_info >= (3, 13):
    import audioop

    sys.modules.setdefault("pyaudioop", audioop)

import gradio as gr
from gradio_client import Client


LABELS = {
    "negative": "Negativo",
    "neutral": "Neutro",
    "positive": "Positivo",
}


def clasificar_resena(texto: str) -> tuple[str, str]:
    texto = texto.strip()
    if not texto:
        raise gr.Error("Escribí una reseña antes de analizarla.")

    endpoint_url = os.getenv("INFERENCE_ENDPOINT_URL")
    if not endpoint_url:
        raise gr.Error(
            "Falta configurar INFERENCE_ENDPOINT_URL con la URL pública "
            "de la Space de inferencia."
        )

    parsed_endpoint = urlparse(endpoint_url)
    if parsed_endpoint.scheme != "https" or not (
        parsed_endpoint.hostname or ""
    ).endswith(".hf.space"):
        raise gr.Error(
            "INFERENCE_ENDPOINT_URL debe ser una URL HTTPS pública de "
            "Hugging Face que termine en .hf.space."
        )

    token = os.getenv("HF_TOKEN")
    if not token:
        raise gr.Error(
            "Falta configurar HF_TOKEN con un token de lectura de Hugging Face. "
            "Guardalo como secreto; no lo compartas."
        )

    cliente = Client(
        src=endpoint_url,
        hf_token=token,
        httpx_kwargs={"timeout": 120},
        verbose=False,
    )
    predicciones = cliente.predict(texto, api_name="/clasificar")

    if not predicciones:
        raise gr.Error("El modelo no devolvió ninguna predicción.")

    if not isinstance(predicciones, list) or not all(
        isinstance(prediccion, dict)
        and isinstance(prediccion.get("label"), str)
        and isinstance(prediccion.get("score"), (int, float))
        for prediccion in predicciones
    ):
        raise gr.Error("La Space devolvió una respuesta con formato inesperado.")

    mejor = max(predicciones, key=lambda prediccion: prediccion["score"])
    etiqueta = LABELS.get(mejor["label"].lower())
    if etiqueta is None:
        raise gr.Error(f"El modelo devolvió una etiqueta desconocida: {mejor['label']}")

    return etiqueta, f"{mejor['score']:.1%}"


with gr.Blocks(title="Semáforo de reseñas") as demo:
    gr.Markdown(
        "# Semáforo de reseñas\n"
        "Explorá si el tono de una reseña parece positivo, neutro o negativo. "
        "La predicción es automática y puede equivocarse."
    )
    reseña = gr.Textbox(
        label="Reseña",
        placeholder="Por ejemplo: La comida llegó fría y tardaron una hora.",
        lines=4,
        max_lines=8,
    )
    boton = gr.Button("Analizar reseña", variant="primary")
    etiqueta = gr.Textbox(label="Sentimiento estimado", interactive=False)
    confianza = gr.Textbox(label="Puntaje del modelo", interactive=False)
    boton.click(
        fn=clasificar_resena,
        inputs=reseña,
        outputs=[etiqueta, confianza],
    )
    gr.Markdown(
        "No ingreses datos personales ni uses esta herramienta como única base "
        "para tomar decisiones sobre clientes."
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", "7860")),
    )
