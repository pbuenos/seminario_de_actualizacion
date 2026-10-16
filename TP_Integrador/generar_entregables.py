"""Generate editable-first PDF and PowerPoint drafts for the integrative project."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "TP_Apellido_Nombre.pdf"
PPTX_PATH = ROOT / "TP_Apellido_Nombre.pptx"

NAVY = "#14213D"
TEAL = "#008C95"
ORANGE = "#FCA311"
PALE = "#F2F6F8"
INK = "#263238"
MUTED = "#5F6B73"
PENDING = "PENDIENTE DE COMPLETAR"


def make_pdf() -> None:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCustom",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor(NAVY),
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionCustom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=colors.HexColor(TEAL),
            spaceBefore=3,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubCustom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor(NAVY),
            spaceBefore=5,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.3,
            textColor=colors.HexColor(INK),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor(MUTED),
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8.3,
            leading=12,
            backColor=colors.HexColor(PALE),
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=5,
        )
    )

    def p(text: str, style: str = "BodyCustom") -> Paragraph:
        return Paragraph(text, styles[style])

    def table(rows, widths, header=True):
        commands = [
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CAD4D9")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
        if header:
            commands.extend(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ]
            )
        result = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
        result.setStyle(TableStyle(commands))
        return result

    story = [
        Spacer(1, 12 * mm),
        p("Semáforo de reseñas", "TitleCustom"),
        p("Clasificación de sentimiento en español con modelos de lenguaje", "SubCustom"),
        Spacer(1, 4 * mm),
        p(
            f"<b>{PENDING}:</b> este archivo es un borrador de trabajo. Antes de entregar, "
            "completar los datos marcados, ejecutar el notebook, desplegar y probar la app, "
            "agregar una captura real y revisar las fuentes.",
            "BodyCustom",
        ),
        p("<b>Estudiante:</b> Apellido, Nombre &nbsp;&nbsp; <b>Curso:</b> IFTS N.º 18 "
          "&nbsp;&nbsp; <b>Fecha:</b> completar"),
        p("A. El problema", "SectionCustom"),
        p(
            "Las reseñas expresan opiniones, pero leerlas una por una dificulta resumir "
            "rápidamente la experiencia de muchas personas. Esta aplicación recibe una reseña "
            "en español y estima si su tono es positivo, neutral o negativo. El resultado es "
            "una orientación automática, no una verdad objetiva ni una decisión sobre el autor."
        ),
        p("B. Modelos: búsqueda, elección y comparación", "SectionCustom"),
        p("1. ¿Qué modelos se evaluaron y qué diferencias importaron?", "SubCustom"),
        table(
            [
                [p("<b>Modelo</b>"), p("<b>Características relevantes</b>")],
                [
                    p("cardiffnlp/twitter-xlm-roberta-base-sentiment"),
                    p("Clasificador multilingüe (incluye español); etiquetas POSITIVE, "
                      "NEUTRAL y NEGATIVE. Pesos publicados de alrededor de 1,11 GB."),
                ],
                [
                    p("pysentimiento/robertuito-sentiment-analysis"),
                    p("Modelo orientado al español y a texto de redes sociales; etiquetas "
                      "POS, NEU y NEG. Pesos publicados de alrededor de 435 MB. "
                      "La ficha indica restricciones de uso no comercial."),
                ],
            ],
            [65 * mm, 110 * mm],
        ),
        p(
            "Candidato inicial para el despliegue: Cardiff, por su cobertura multilingüe "
            "y una ruta de inferencia que puede demostrarse con la Space elegida. La elección "
            "final debe contrastarse con los ejemplos etiquetados del notebook; aquí no se "
            "declara una superioridad de exactitud sin medirla."
        ),
        p("Fuentes de modelos: fichas enlazadas al final. Confirmar licencias y disponibilidad "
          "en la fecha de entrega."),
        PageBreak(),
        p("B. Modelos y resultados", "SectionCustom"),
        p("2. ¿Cómo se prepararon los datos y se compararon los modelos?", "SubCustom"),
        p(
            "Se prepararon diez frases cortas en español con una etiqueta de referencia "
            "asignada manualmente (positiva, neutral o negativa). Se incluyeron expresiones "
            "claras, casos neutrales, negación y formulaciones mixtas. Cada frase se procesó "
            "con ambos modelos. El notebook muestra la etiqueta predicha, el puntaje y si "
            "coincide con la referencia. La muestra es pequeña y didáctica: no representa "
            "una evaluación estadística generalizable."
        ),
        p("Resumen medido — reemplazar con los valores que genere el notebook:", "SubCustom"),
        table(
            [
                [p("<b>Método/modelo</b>"), p("<b>Aciertos / 10</b>"), p("<b>Exactitud</b>"),
                 p("<b>Tiempo real</b>")],
                [p("pipeline — Cardiff"), p(PENDING), p(PENDING), p(PENDING)],
                [p("gradio_client — Cardiff / Space"), p(PENDING), p(PENDING), p(PENDING)],
                [p("pipeline — RoBERTuito"), p(PENDING), p(PENDING), p(PENDING)],
            ],
            [55 * mm, 37 * mm, 35 * mm, 48 * mm],
        ),
        p(
            "Anotar si el tiempo remoto incluye arranque en frío, latencia de red o cola. "
            "La Space usa Gradio nativo porque ZeroGPU requiere una función Gradio marcada "
            "con @spaces.GPU; por eso la llamada remota se hace con gradio_client y no con "
            "InferenceClient. La salida de pipeline y la respuesta de gradio_client pueden tener tipos "
            "diferentes; el notebook los inspecciona y normaliza para compararlos."
        ),
        p("3. Errores de clasificación observados", "SubCustom"),
        table(
            [
                [p("<b>Frase / modelo</b>"), p("<b>Referencia</b>"), p("<b>Predicción</b>"),
                 p("<b>Interpretación</b>")],
                [p(PENDING), p(PENDING), p(PENDING), p("Copiar un error real de la tabla.")],
                [p(PENDING), p(PENDING), p(PENDING), p("Copiar un segundo error real.")],
            ],
            [47 * mm, 30 * mm, 33 * mm, 65 * mm],
        ),
        p(
            "Completar esta tabla solo después de ejecutar el notebook. Un puntaje alto "
            "representa confianza del modelo en su etiqueta, no probabilidad garantizada "
            "de que la interpretación humana sea correcta."
        ),
        PageBreak(),
        p("C. Arquitectura, inferencia y costos", "SectionCustom"),
        p("4. ¿Qué función cumple la inferencia?", "SubCustom"),
        p(
            "La inferencia consiste en aplicar un modelo ya entrenado a una entrada nueva. "
            "La persona ingresa una reseña; el modelo devuelve una clase de sentimiento y "
            "un puntaje. En este proyecto, los pesos se descargan en el entorno que ejecuta "
            "la inferencia; no se reentrena el modelo al recibir cada consulta."
        ),
        p("5. ¿Dónde vive y se ejecuta cada parte?", "SubCustom"),
        table(
            [
                [p("<b>Etapa</b>"), p("<b>Servicio / responsabilidad</b>")],
                [p("Interfaz y lógica"), p("Repositorio GitHub; Render ejecuta app.py y muestra "
                  "la interfaz Gradio.")],
                [p("Solicitud de clasificación"), p("La app de Render usa gradio_client y "
                  "envía la reseña a la API Gradio configurada.")],
                [p("Modelo"), p("Una Hugging Face Space con ZeroGPU recibe la solicitud, carga "
                  "el clasificador y devuelve etiquetas y puntajes.")],
                [p("Usuario"), p("Navegador → Render → Space de Hugging Face → Render → "
                  "resultado visible.")],
            ],
            [47 * mm, 128 * mm],
        ),
        p("6. Límites, recursos y medidas", "SubCustom"),
        p(
            "Los archivos de pesos publicados son aproximadamente 1,11 GB para Cardiff "
            "y 435 MB para RoBERTuito; deben confirmarse en las fichas del modelo. Render "
            "Free puede suspender servicios inactivos y volver a iniciarlos con demora; "
            "ZeroGPU es un recurso compartido sujeto a cuotas y disponibilidad. El uso "
            "gratuito no equivale a disponibilidad garantizada y puede haber latencia de "
            "red o espera en la cola."
        ),
        p(
            "Las mediciones válidas son las obtenidas en el notebook ejecutado. La app limita "
            "el endpoint a HTTPS bajo el dominio .hf.space y el token se configura como "
            "secreto en Render; nunca debe subirse al repositorio."
        ),
        p("D. Alternativa de despliegue", "SectionCustom"),
        p("7. ¿Por qué Render frente a otras opciones?", "SubCustom"),
        p(
            "Render se eligió para publicar la interfaz desde un repositorio y configurar "
            "comandos y variables de entorno sin administrar un servidor virtual. Una VPS "
            "ofrece más control, pero requiere mantener sistema operativo, seguridad y "
            "proceso del servidor. Un entorno local facilita pruebas, pero no ofrece por sí "
            "solo un enlace público persistente. La arquitectura separa la interfaz en "
            "Render del cómputo del modelo en Hugging Face, para evitar descargar y mantener "
            "pesos grandes en el servicio web gratuito."
        ),
        PageBreak(),
        p("E. Pruebas, errores y revisión", "SectionCustom"),
        p("8. Errores reales durante el desarrollo y cómo se resolvieron", "SubCustom"),
        table(
            [
                [p("<b>Error</b>"), p("<b>Causa</b>"), p("<b>Corrección</b>")],
                [
                    p("No @spaces.GPU function detected during startup"),
                    p("ZeroGPU no detectaba la función GPU en la app FastAPI que montaba Gradio."),
                    p("Cambiar a Gradio nativo y conectar directamente la función marcada "
                      "con @spaces.GPU."),
                ],
                [
                    p("ModuleNotFoundError: No module named 'app'"),
                    p("Se lanzó unittest desde la raíz, aunque la importación app pertenece "
                      "al directorio TP_Integrador."),
                    p("Ejecutar la suite desde TP_Integrador, donde se encuentra app.py."),
                ],
            ],
            [58 * mm, 59 * mm, 58 * mm],
        ),
        p(
            "Estos son errores de desarrollo observados en el trabajo. Para la versión final, "
            "ejecutar nuevamente las pruebas y agregar cualquier error funcional real que "
            "surja al publicar o probar la inferencia; no reemplazarlo por un caso supuesto."
        ),
        p("9. ¿Qué es y qué no es un modelo generativo?", "SubCustom"),
        p(
            "El clasificador usado es discriminativo: estima una categoría para un texto "
            "existente. Un modelo generativo produce texto nuevo, como una explicación o un "
            "resumen. Aunque ambos se basan en redes neuronales y lenguaje, la tarea y la "
            "salida son distintas. Esta app no genera reseñas ni justificaciones."
        ),
        p("10. Cinco líneas de app.py y vocabulario de programación", "SubCustom"),
        p(
            "<font name='Courier'>L21  def clasificar_resena(texto: str) -&gt; tuple[str, str]:<br/>"
            "L49      cliente = Client(<br/>"
            "L50          src=endpoint_url,<br/>"
            'L55      predicciones = cliente.predict(texto, api_name="/clasificar")<br/>'
            "L73      return etiqueta, f&quot;{mejor['score']:.1%}&quot;</font>",
            "CodeCustom",
        ),
        p(
            "<b>Clase:</b> Client. <b>Instancia:</b> cliente. "
            "<b>Método:</b> predict. <b>Atributo/clave:</b> mejor[&quot;score&quot;]. "
            "<b>Parámetro:</b> src; <b>argumento:</b> endpoint_url. "
            "<b>Parámetro de función:</b> texto; <b>argumento en la llamada:</b> texto. "
            "<b>Retorno:</b> la tupla etiqueta y puntaje formateado."
        ),
        PageBreak(),
        p("F. Publicación y fuentes", "SectionCustom"),
        p("Publicación — completar después del deploy", "SubCustom"),
        table(
            [
                [p("<b>Elemento</b>"), p("<b>URL / evidencia</b>")],
                [p("Aplicación pública de Render"), p(PENDING)],
                [p("Space ZeroGPU de Hugging Face"), p(PENDING)],
                [p("Repositorio con código y notebook"), p(PENDING)],
                [p("Captura de la app clasificando una reseña real"), p(PENDING)],
            ],
            [68 * mm, 107 * mm],
        ),
        Spacer(1, 5 * mm),
        p("Fuentes consultadas", "SubCustom"),
        p(
            "• Modelo Cardiff: https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment<br/>"
            "• Modelo RoBERTuito: https://huggingface.co/pysentimiento/robertuito-sentiment-analysis<br/>"
            "• Hugging Face Spaces: https://huggingface.co/docs/hub/spaces-overview<br/>"
            "• Gradio Python Client: https://www.gradio.app/docs/python-client/introduction<br/>"
            "• Render: https://render.com/docs/free<br/>"
            "Revisar licencias y condiciones vigentes antes de entregar."
        ),
        p(
            "<b>Uso de IA:</b> se utilizó un asistente de IA para apoyar la estructura del "
            "código y la redacción inicial. La persona autora debe revisar, ejecutar, "
            "comprender y adaptar el trabajo, y declarar el uso de herramientas según las "
            "normas de la materia.",
            "BodyCustom",
        ),
        p(
            "Control final: completar apellido/nombre, ejecutar el notebook, reemplazar "
            "marcadores por resultados, desplegar y verificar ambas URLs, agregar captura, "
            "revisar ortografía y renombrar los archivos con los datos solicitados.",
            "SmallCustom",
        ),
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D6E0E4"))
        canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawString(18 * mm, 9 * mm, "TP Integrador | BORRADOR")
        canvas.drawRightString(192 * mm, 9 * mm, f"Página {doc.page}")
        canvas.restoreState()

    document = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=20 * mm,
        title="Semáforo de reseñas — TP Integrador",
        author="Apellido Nombre (completar)",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)


def make_presentation() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    navy = RGBColor(20, 33, 61)
    teal = RGBColor(0, 140, 149)
    orange = RGBColor(252, 163, 17)
    ink = RGBColor(38, 50, 56)
    muted = RGBColor(95, 107, 115)
    pale = RGBColor(242, 246, 248)
    white = RGBColor(255, 255, 255)

    def textbox(slide, x, y, w, h, text, size=20, color=ink, bold=False,
                align=PP_ALIGN.LEFT):
        shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        frame = shape.text_frame
        frame.clear()
        frame.word_wrap = True
        frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        for idx, line in enumerate(text.split("\n")):
            para = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
            para.text = line
            para.font.name = "Aptos"
            para.font.size = Pt(size)
            para.font.bold = bold
            para.font.color.rgb = color
            para.alignment = align
            para.space_after = Pt(8)
        return shape

    def rect(slide, x, y, w, h, fill, rounded=True):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
        shape = slide.shapes.add_shape(
            kind, Inches(x), Inches(y), Inches(w), Inches(h)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
        shape.line.fill.background()
        return shape

    def base(title, number):
        slide = prs.slides.add_slide(blank)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = white
        rect(slide, 0, 0, 13.333, 0.16, teal, rounded=False)
        textbox(slide, 0.6, 0.35, 11.8, 0.65, title, 27, navy, True)
        textbox(slide, 0.65, 7.08, 9.5, 0.2, "TP Integrador · BORRADOR · completar evidencias", 9, muted)
        textbox(slide, 12.1, 7.04, 0.6, 0.25, str(number), 10, muted, align=PP_ALIGN.RIGHT)
        return slide

    slide = prs.slides.add_slide(blank)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = navy
    rect(slide, 0.65, 0.7, 0.16, 5.8, teal, rounded=False)
    textbox(slide, 1.2, 1.2, 10.8, 1.2, "Semáforo de reseñas", 36, white, True)
    textbox(slide, 1.2, 2.5, 10.8, 1.0,
            "Clasificación de sentimiento en español\ncon modelos de lenguaje", 24, white)
    rect(slide, 1.2, 4.5, 4.7, 0.65, orange)
    textbox(slide, 1.35, 4.58, 4.4, 0.42, "BORRADOR — falta validar y desplegar", 15, navy, True)
    textbox(slide, 1.2, 5.65, 10, 0.6, "Apellido, Nombre · IFTS N.º 18 · Fecha: completar", 16, white)

    slide = base("1 · Problema y objetivo", 2)
    rect(slide, 0.8, 1.4, 5.6, 4.7, pale)
    textbox(slide, 1.1, 1.7, 5.0, 0.5, "El problema", 23, teal, True)
    textbox(slide, 1.1, 2.35, 5.0, 2.8,
            "Leer muchas reseñas una por una dificulta resumir la experiencia de clientes.\n\n"
            "Objetivo: recibir una frase y estimar su tono como positivo, neutral o negativo.",
            18, ink)
    rect(slide, 6.9, 1.4, 5.6, 4.7, navy)
    textbox(slide, 7.25, 1.75, 5.0, 0.5, "Alcance responsable", 23, orange, True)
    textbox(slide, 7.25, 2.4, 4.9, 2.8,
            "• Clasificación, no generación de texto.\n"
            "• El puntaje no garantiza verdad.\n"
            "• Frases ambiguas, ironía y contexto pueden causar errores.\n"
            "• Muestra de evaluación pequeña y didáctica.",
            17, white)

    slide = base("2 · Modelos y evaluación", 3)
    rect(slide, 0.8, 1.35, 5.8, 2.2, pale)
    textbox(slide, 1.1, 1.55, 5.1, 0.55, "Cardiff XLM-R", 22, teal, True)
    textbox(slide, 1.1, 2.15, 5.0, 1.0,
            "Multilingüe; incluye español.\n3 clases · pesos ≈ 1,11 GB.", 17, ink)
    rect(slide, 6.8, 1.35, 5.8, 2.2, pale)
    textbox(slide, 7.1, 1.55, 5.1, 0.55, "RoBERTuito", 22, teal, True)
    textbox(slide, 7.1, 2.15, 5.0, 1.0,
            "Orientado a español/redes sociales.\n3 clases · pesos ≈ 435 MB.", 17, ink)
    rect(slide, 0.8, 3.95, 11.8, 2.15, navy)
    textbox(slide, 1.15, 4.15, 10.9, 0.55, "Resultados auténticos del notebook", 21, orange, True)
    textbox(slide, 1.15, 4.85, 10.9, 0.9,
            "Cardiff: aciertos PENDIENTE/10 · tiempo PENDIENTE\n"
            "RoBERTuito: aciertos PENDIENTE/10 · tiempo PENDIENTE\n"
            "No afirmar cuál es mejor hasta ejecutar y revisar las diez frases.",
            16, white)

    slide = base("3 · ¿Qué es inferir?", 4)
    textbox(slide, 0.9, 1.35, 11.7, 0.9,
            "Aplicar un modelo ya entrenado a una entrada nueva para obtener una predicción.",
            22, ink)
    boxes = [
        (0.8, "Entrada\nreseña"),
        (3.25, "Render\ninterfaz"),
        (5.7, "gradio_client\nHTTPS"),
        (8.15, "HF Space\nZeroGPU"),
        (10.6, "Clase +\npuntaje"),
    ]
    for x, label in boxes:
        rect(slide, x, 3.0, 1.9, 1.4, pale)
        textbox(slide, x + 0.1, 3.15, 1.7, 1.0, label, 16, navy, True, PP_ALIGN.CENTER)
    for x in [2.75, 5.2, 7.65, 10.1]:
        textbox(slide, x, 3.25, 0.45, 0.5, "→", 22, teal, True, PP_ALIGN.CENTER)
    textbox(slide, 1.0, 5.0, 11.1, 0.8,
            "UI/código: Render · inferencia y pesos: Space · notebook: compara pipeline y gradio_client",
            18, muted, align=PP_ALIGN.CENTER)

    slide = base("4 · Despliegue y alternativas", 5)
    rect(slide, 0.8, 1.35, 5.7, 4.8, pale)
    textbox(slide, 1.1, 1.65, 5.0, 0.5, "Por qué separar servicios", 22, teal, True)
    textbox(slide, 1.1, 2.25, 4.9, 3.2,
            "Render publica la interfaz desde GitHub y configura secretos.\n\n"
            "La Space aloja el modelo pesado y recibe la llamada de clasificación.\n\n"
            "La opción gratuita puede dormir, tener cuota o latencia; verificar condiciones actuales.",
            17, ink)
    rect(slide, 6.8, 1.35, 5.7, 4.8, pale)
    textbox(slide, 7.1, 1.65, 5.0, 0.5, "Evidencia de la app", 22, teal, True)
    rect(slide, 7.15, 2.35, 5.0, 2.65, white)
    textbox(slide, 7.45, 2.7, 4.4, 1.9,
            "INSERTAR CAPTURA REAL\n"
            "App publicada clasificando\n"
            "una reseña de prueba",
            18, muted, True, PP_ALIGN.CENTER)
    textbox(slide, 7.1, 5.25, 5.0, 0.55, "Render: PENDIENTE · Space: PENDIENTE", 14, ink)

    slide = base("5 · Errores y aprendizajes", 6)
    errors = [
        ("IndentationError", "Sangría incompleta en una edición.", "Corregir bloque y compilar."),
        ("ModuleNotFoundError: app", "Unittest desde la raíz incorrecta.", "Ejecutar desde TP_Integrador."),
    ]
    for idx, (name, cause, fix) in enumerate(errors):
        y = 1.55 + idx * 2.0
        rect(slide, 0.9, y, 11.5, 1.45, pale)
        textbox(slide, 1.2, y + 0.12, 3.0, 0.45, name, 19, teal, True)
        textbox(slide, 4.0, y + 0.12, 3.7, 1.0, "Causa:\n" + cause, 15, ink)
        textbox(slide, 8.0, y + 0.12, 4.0, 1.0, "Resolución:\n" + fix, 15, ink)
    textbox(slide, 1.0, 5.9, 11.3, 0.5,
            "Agregar fallas de inferencia o deploy solo si ocurrieron realmente.", 16, muted)

    slide = base("6 · Cierre, enlaces y revisión", 7)
    rect(slide, 0.8, 1.35, 5.7, 4.9, navy)
    textbox(slide, 1.15, 1.7, 4.9, 0.55, "Enlaces para la defensa", 22, orange, True)
    textbox(slide, 1.15, 2.4, 4.8, 2.8,
            "App Render: PENDIENTE\n"
            "Space Hugging Face: PENDIENTE\n"
            "Repositorio/notebook: PENDIENTE\n"
            "Captura: insertar evidencia real",
            17, white)
    rect(slide, 6.8, 1.35, 5.7, 4.9, pale)
    textbox(slide, 7.15, 1.7, 4.9, 0.55, "Antes de entregar", 22, teal, True)
    textbox(slide, 7.15, 2.4, 4.8, 2.8,
            "• Ejecutar notebook y revisar errores.\n"
            "• Completar métricas y enlaces.\n"
            "• Probar ambos servicios.\n"
            "• Declarar el uso de IA según la materia.\n"
            "• Reemplazar Apellido_Nombre.",
            17, ink)

    prs.save(PPTX_PATH)


if __name__ == "__main__":
    make_pdf()
    make_presentation()
    print(f"PDF: {PDF_PATH}")
    print(f"PPTX: {PPTX_PATH}")
