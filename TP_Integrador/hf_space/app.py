import gradio as gr
import spaces
from transformers import pipeline


MODEL_ID = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
clasificador = pipeline(
    "text-classification",
    model=MODEL_ID,
    device=0,
    use_fast=False,
)


@spaces.GPU(duration=30)
def clasificar(texto: str) -> list[dict[str, str | float]]:
    texto = texto.strip()
    if not texto:
        raise gr.Error("Escribí una reseña antes de analizarla.")
    if len(texto) > 2000:
        raise gr.Error("La reseña no puede superar los 2000 caracteres.")

    resultados = clasificador(texto, top_k=None, truncation=True)
    return [
        {"label": str(resultado["label"]), "score": float(resultado["score"])}
        for resultado in resultados
    ]


demo = gr.Interface(
    fn=clasificar,
    inputs=gr.Textbox(
        label="Reseña",
        placeholder="Escribí una reseña breve en español.",
        lines=4,
        max_lines=8,
        max_length=2000,
    ),
    outputs=gr.JSON(label="Sentimiento y puntajes"),
    title="Semáforo de reseñas",
    description="Clasificación de sentimiento con un modelo ya entrenado.",
    api_name="clasificar",
)


if __name__ == "__main__":
    demo.launch()
