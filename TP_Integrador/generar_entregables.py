"""Generate the PDF report and PowerPoint presentation for the integrative project."""

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
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.platypus import (
    Image as ReportImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
PDF_PATH = ROOT / "TP_Bueno_Pereyra_Pedro.pdf"
PPTX_PATH = ROOT / "TP_Bueno_Pereyra_Pedro.pptx"
EVIDENCE_DIR = ROOT / "evidencias"

NAVY = "#14213D"
TEAL = "#008C95"
ORANGE = "#FCA311"
PALE = "#F2F6F8"
INK = "#263238"
MUTED = "#5F6B73"
STUDENT = "Pedro Bueno Pereyra"
DELIVERY_DATE = "16/10/2026"
RENDER_URL = "https://semaforo-de-resenas.onrender.com/"
SPACE_URL = "https://huggingface.co/spaces/Pbueno467/TP-integrador"
REPOSITORY_URL = "https://github.com/pbuenos/seminario_de_actualizacion/tree/main/TP_Integrador"


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

    def architecture_diagram():
        drawing = Drawing(492, 124)
        drawing.add(String(0, 112, "Publicación del código", fontName="Helvetica-Bold",
                           fontSize=8, fillColor=colors.HexColor(NAVY)))
        drawing.add(String(0, 54, "Uso de la app: viaja la reseña y vuelve la predicción",
                           fontName="Helvetica-Bold", fontSize=8,
                           fillColor=colors.HexColor(NAVY)))

        def add_row(labels, y, box_width, gap, font_size):
            box_height = 36
            for index, label in enumerate(labels):
                x = index * (box_width + gap)
                drawing.add(
                    Rect(
                        x, y, box_width, box_height,
                        fillColor=colors.HexColor(PALE),
                        strokeColor=colors.HexColor(TEAL),
                        strokeWidth=1,
                        rx=4, ry=4,
                    )
                )
                for line_index, line in enumerate(label.split("\n")):
                    drawing.add(
                        String(
                            x + box_width / 2,
                            y + 22 - line_index * 11,
                            line,
                            fontName="Helvetica",
                            fontSize=font_size,
                            fillColor=colors.HexColor(NAVY),
                            textAnchor="middle",
                        )
                    )
                if index < len(labels) - 1:
                    start_x = x + box_width + 2
                    end_x = x + box_width + gap - 3
                    mid_y = y + box_height / 2
                    drawing.add(Line(start_x, mid_y, end_x, mid_y,
                                     strokeColor=colors.HexColor(TEAL), strokeWidth=1))
                    drawing.add(
                        Polygon(
                            [end_x, mid_y, end_x - 4, mid_y + 3, end_x - 4, mid_y - 3],
                            fillColor=colors.HexColor(TEAL),
                            strokeColor=colors.HexColor(TEAL),
                        )
                    )

        add_row(["PC\ncódigo fuente", "GitHub\nrepositorio", "Render\nejecuta app.py"],
                68, 112, 54, 8)
        add_row(["Navegador\nreseña", "Render\napp.py", "gradio_client\nAPI HTTPS",
                 "HF Space\nZeroGPU + pesos", "Navegador\nresultado"],
                5, 78, 22, 7.5)
        return drawing

    story = [
        Spacer(1, 12 * mm),
        p("Semáforo de reseñas", "TitleCustom"),
        p("Clasificación de sentimiento en español con modelos de lenguaje", "SubCustom"),
        Spacer(1, 4 * mm),
        p(f"<b>Estudiante:</b> {STUDENT} &nbsp;&nbsp; <b>Curso:</b> IFTS N.º 18 "
          f"&nbsp;&nbsp; <b>Fecha:</b> {DELIVERY_DATE}"),
        p("A. El problema", "SectionCustom"),
        p(
            "1. ¿Qué problema querés resolver y para quién? ¿Por qué un modelo de IA "
            "y no unas reglas escritas a mano (un if con palabras clave)?",
            "SubCustom",
        ),
        p(
            "El problema es revisar muchas opiniones de clientes para detectar rápidamente "
            "si el tono de una reseña parece positivo, neutral o negativo. La herramienta "
            "está pensada como apoyo exploratorio para quien gestiona un comercio; no toma "
            "decisiones sobre clientes. Un conjunto pequeño de reglas por palabras clave "
            "podría servir para vocabulario fijo, pero falla con negaciones, ironía, contexto "
            "y expresiones como “Genial, otra vez me cancelaron...”. Un modelo preentrenado "
            "aporta patrones lingüísticos aprendidos, aunque también puede equivocarse; por "
            "eso su salida se presenta como orientación y no como verdad."
        ),
        p("B. El modelo", "SectionCustom"),
        p(
            "2. ¿Qué modelos consideraste y por qué te quedaste con uno? Citá lo que "
            "leíste en su model card: tarea, etiquetas, idiomas, datos de entrenamiento, "
            "tamaño de los pesos.",
            "SubCustom",
        ),
        table(
            [
                [p("<b>Modelo</b>"), p("<b>Model card y tamaño informado</b>")],
                [
                    p("cardiffnlp/twitter-xlm-roberta-base-sentiment"),
                    p("Clasificación de sentimiento; POSITIVE, NEUTRAL, NEGATIVE; ocho "
                      "idiomas, incluido español. La tarjeta describe preentrenamiento con "
                      "unos 198 millones de tweets y ajuste multilingüe de sentimiento. "
                      "Pesos: 1.112.271.561 bytes (≈1,04 GiB)."),
                ],
                [
                    p("pysentimiento/robertuito-sentiment-analysis"),
                    p("Clasificación de sentimiento en español; POS, NEU, NEG. La tarjeta "
                      "describe preentrenamiento de RoBERTuito con más de 500 millones de "
                      "tweets en español y ajuste con TASS 2020 (aprox. 5.000 tweets). "
                      "Pesos: 435.189.428 bytes (≈415 MiB); uso no comercial indicado."),
                ],
            ],
            [65 * mm, 110 * mm],
        ),
        p(
            "Se eligió Cardiff para la app porque admite español y se integró con la Space "
            "ZeroGPU disponible. La prueba didáctica dio 8/10 aciertos para cada modelo; "
            "esa muestra pequeña no demuestra que Cardiff sea más exacto. Se priorizaron "
            "compatibilidad de despliegue y tamaño frente a afirmar una superioridad medida."
        ),
        p(
            "Fuentes: model cards enlazadas al final. Las tarjetas no describen con el "
            "mismo detalle todos los corpus de ajuste; no se atribuyen datos no publicados "
            "por sus autores."
        ),
        PageBreak(),
        p("B. El modelo", "SectionCustom"),
        p(
            "3. ¿Dónde se equivoca? Mostrá ejemplos reales de tu notebook y explicá por "
            "qué creés que se equivoca, relacionándolo con los datos con los que fue entrenado.",
            "SubCustom",
        ),
        p(
            "Se probaron diez frases con etiquetas manuales: ejemplos claros, neutralidad, "
            "negación, ironía, una reseña en inglés, texto muy corto y jerga rioplatense. "
            "La tabla del notebook muestra frase, etiqueta esperada y predicha, puntaje y "
            "acierto. Es una muestra pequeña, didáctica y no generalizable."
        ),
        p("Resultados medidos en diez frases:", "SubCustom"),
        table(
            [
                [p("<b>Método/modelo</b>"), p("<b>Aciertos / 10</b>"), p("<b>Exactitud</b>"),
                 p("<b>Tiempo</b>")],
                [p("Cardiff XLM-R"), p("8 / 10"), p("80 %"), p("0,569 s / 10")],
                [p("RoBERTuito"), p("8 / 10"), p("80 %"), p("0,529 s / 10")],
            ],
            [49 * mm, 30 * mm, 28 * mm, 68 * mm],
        ),
        p(
            "La carga/descarga medida fue 110,840 s para Cardiff y 92,619 s para "
            "RoBERTuito; depende de equipo, conexión y caché."
        ),
        p(
            "En una prueba separada con la frase “No me respondieron el reclamo y nadie se "
            "hizo cargo”, pipeline clasificó como negative (puntaje 0,7448) en 0,0593 s; "
            "la Space devolvió la misma etiqueta (0,7448) en 2,2485 s. El tiempo remoto "
            "incluye la llamada por red y no es directamente comparable con la inferencia "
            "local ya cargada. "
            "La Space usa Gradio nativo porque ZeroGPU requiere una función Gradio marcada "
            "con @spaces.GPU; por eso la llamada remota se hace con gradio_client y no con "
            "InferenceClient. La salida de pipeline y la respuesta de gradio_client pueden tener tipos "
            "diferentes; el notebook los inspecciona y normaliza para compararlos."
        ),
        table(
            [
                [p("<b>Frase / modelo</b>"), p("<b>Referencia</b>"), p("<b>Predicción</b>"),
                 p("<b>Interpretación</b>")],
                [p("Cardiff: “Esperé una hora y me entregaron el pedido frío.”"),
                 p("Negativo"), p("Neutro"), p("No detectó el sentimiento negativo.")],
                [p("RoBERTuito: “La comida estaba bien, sin nada especial.”"),
                 p("Neutro"), p("Positivo"), p("Interpretó una valoración tenue como positiva.")],
            ],
            [47 * mm, 30 * mm, 33 * mm, 65 * mm],
        ),
        p(
            "Cardiff puede confundir una reseña de comercio con patrones de tweets "
            "multilingües: la queja “pedido frío” expresa el problema por su consecuencia "
            "sin una palabra negativa directa. RoBERTuito fue preentrenado con tweets en "
            "español y ajustado con TASS, pero “bien, sin nada especial” es una valoración "
            "tenue que puede quedar fuera de sus patrones aprendidos. En ambos casos, el "
            "puntaje expresa confianza del modelo, no garantía de acierto."
        ),
        p(
            "4. Tu app, ¿está entrenando o infiriendo? Explicá la diferencia con tu propio caso.",
            "SubCustom",
        ),
        p(
            "La app infiere: aplica los pesos ya entrenados de Cardiff a una reseña nueva "
            "y devuelve una etiqueta y un puntaje. No ajusta sus parámetros con cada texto. "
            "Entrenar implicaría actualizar esos parámetros mediante datos y optimización, "
            "algo que no sucede al presionar “Analizar reseña”."
        ),
        PageBreak(),
        p("C. Dónde corre cada cosa", "SectionCustom"),
        p(
            "5. ¿Dónde vive el código y dónde vive el modelo? Hacé un esquema simple "
            "(cajas y flechas, a mano o en cualquier herramienta) con los lugares que "
            "intervienen en tu app: tu compu, GitHub, la plataforma de deploy y Hugging Face. "
            "En cada caja anotá qué hay ahí, y marcá con flechas qué viaja de un lugar a "
            "otro cuando alguien usa la app. Tiene que quedar claro: ¿dónde está guardado "
            "tu código? ¿Dónde se ejecuta? ¿Dónde están los pesos del modelo y dónde se "
            "hace la inferencia?",
            "SubCustom",
        ),
        table(
            [
                [p("<b>Etapa</b>"), p("<b>Servicio / responsabilidad</b>")],
                [p("Código fuente"), p("GitHub conserva app.py y dependencias; el deploy toma "
                  "el código del repositorio.")],
                [p("Interfaz"), p("Render ejecuta app.py y sirve Gradio desde un proceso web.")],
                [p("Pesos e inferencia"), p("La Space de Hugging Face aloja Cardiff; ZeroGPU "
                  "asigna la GPU durante la función de clasificación.")],
                [p("Flujo"), p("Navegador → Render → API Gradio/gradio_client → Space "
                  "ZeroGPU → etiqueta y puntaje → Render → navegador.")],
            ],
            [47 * mm, 128 * mm],
        ),
        p(
            "El navegador envía el texto; los pesos no se trasladan: la Space procesa "
            "la solicitud y devuelve solo la predicción.",
            "SmallCustom",
        ),
        architecture_diagram(),
        p(
            "6. ¿Usaste pipeline o InferenceClient en la app publicada? Justificalo con "
            "números (memoria del plan gratuito, peso del modelo, tiempo de respuesta). "
            "¿Qué pasaría si hubieras elegido la otra?",
            "SubCustom",
        ),
        p(
            "La app publicada no usa pipeline ni InferenceClient: Render llama con "
            "gradio_client a la API Gradio de la Space. Se eligió porque ZeroGPU requiere "
            "un handler Gradio decorado con @spaces.GPU; InferenceClient no invoca "
            "directamente ese endpoint Gradio. No se presentan ambos clientes como "
            "equivalentes."
        ),
        p(
            "Cardiff pesa 1.112.271.561 bytes (≈1,04 GiB); la instancia Free de Render "
            "dispone de 512 MB RAM según la configuración consultada, menos que los pesos "
            "sin contar Python y Gradio. La carga local de Cardiff tomó 110,840 s; luego "
            "una inferencia ya cargada tardó 0,0593 s. La llamada a la Space tardó 2,2485 s "
            "incluyendo red/cola. Estos tiempos no comparan hardware equivalente. Si se "
            "usara pipeline en Render, el modelo no cabría en esa memoria. InferenceClient "
            "requeriría publicar en un endpoint/proveedor compatible; no llamaría a esta "
            "Space Gradio y sus créditos/costos dependerían de ese servicio."
        ),
        p(
            "La app valida HTTPS y el dominio .hf.space; el token de lectura se configura "
            "como secreto en Render, nunca en el repositorio."
        ),
        p("D. El deploy", "SectionCustom"),
        p(
            "7. ¿Dónde deployaste y por qué ahí? Compará tu elección con al menos otras dos "
            "opciones vistas en clase (hosting compartido, VPS, PaaS, serverless, nubes "
            "elásticas) y explicá por qué las descartaste. ¿Por qué tu app necesita un "
            "servidor que quede encendido?",
            "SubCustom",
        ),
        p(
            "Render es un PaaS: construye desde GitHub y ejecuta el servidor web sin que "
            "tenga que administrar un sistema operativo. Una VPS se descartó porque requiere "
            "mantener sistema, actualizaciones, seguridad y escalado. Ejecutarla solo en la "
            "computadora local no ofrece un enlace público persistente y deja de responder "
            "cuando se apaga. Serverless podría atender funciones puntuales, pero sumaría "
            "límites de ejecución y otra integración para una interfaz web que llama a un "
            "modelo remoto."
        ),
        p(
            "El navegador necesita que un proceso web reciba HTTP en la URL pública; ese "
            "proceso, a su vez, llama a la Space para inferir. El servicio Free de Render "
            "se suspende tras 15 minutos sin tráfico y puede tardar alrededor de un minuto "
            "en despertar, por lo que no queda siempre encendido. Para disponibilidad "
            "garantizada habría que pagar un servicio siempre activo y dimensionarlo."
        ),
        PageBreak(),
        p("E. Lo que se rompió", "SectionCustom"),
        p(
            "8. Documentá al menos dos errores reales que te aparecieron durante el trabajo. "
            "Para cada uno: el mensaje de error completo; dónde apareció; qué lo causaba; "
            "y cómo lo resolviste, paso a paso.",
            "SubCustom",
        ),
        p(
            "<b>Error 1 — Hugging Face Space, al iniciar:</b><br/>"
            "<font name='Courier'>No @spaces.GPU function detected during startup</font>.<br/>"
            "<b>Causa:</b> ZeroGPU no reconocía la función GPU cuando Gradio estaba montado "
            "en una app FastAPI/Uvicorn personalizada.<br/>"
            "<b>Resolución:</b> 1) pasar la Space a Gradio nativo; 2) conectar directamente "
            "la función decorada con <font name='Courier'>@spaces.GPU</font>; 3) publicar "
            "los archivos y revisar los logs de arranque."
        ),
        p(
            "<b>Error 2 — Render, durante el inicio:</b><br/>"
            "<font name='Courier'>ValueError: When localhost is not accessible, a shareable "
            "link must be created. Please set share=True or check your proxy settings to "
            "allow access to localhost.</font><br/>"
            "<b>Causa:</b> <font name='Courier'>demo.launch()</font> intentaba servir Gradio "
            "directamente detrás del proxy.<br/>"
            "<b>Resolución:</b> 1) no activar <font name='Courier'>share=True</font>; "
            "2) montar Gradio en FastAPI; 3) iniciar Uvicorn en "
            "<font name='Courier'>0.0.0.0</font> y en el puerto de Render "
            "<font name='Courier'>PORT</font>; 4) volver a desplegar y probar la URL."
        ),
        p(
            "<b>Error 3 — Render, al servir la página:</b><br/>"
            "<font name='Courier'>TypeError: cannot use 'tuple' as a dict key "
            "(unhashable type: 'dict')</font>.<br/>"
            "<b>Causa:</b> incompatibilidad de versiones web al ejecutar con Python 3.14."
            "<br/><b>Resolución:</b> fijar Python 3.13.4 y versiones compatibles de "
            "FastAPI/Starlette/Uvicorn; reconstruir y verificar que la página responda."
        ),
        p(
            "9. Límites de tu solución: ¿qué pasa si la usan 1000 personas a la vez? ¿Si "
            "Hugging Face cambia las condiciones del plan gratuito (como ya pasó con los "
            "Spaces)? ¿Qué cambiarías para que fuera un producto real?",
            "SubCustom",
        ),
        p(
            "Con 1.000 solicitudes simultáneas no se puede garantizar respuesta: Render "
            "puede saturarse y ZeroGPU es compartido, con cuota y cola; se pueden acumular "
            "esperas y vencer los timeouts. Hoy no hay pruebas de carga, cola propia, escalado "
            "ni SLA. Si Hugging Face cambia o retira el plan gratuito, la Space podría "
            "suspenderse o requerir pago; habría que migrar a un endpoint o servidor con "
            "presupuesto y repetir las pruebas. Para un producto real agregaría pruebas de "
            "carga, rate limits, métricas/alertas, colas, capacidad escalable, política de "
            "privacidad y presupuesto. El puntaje no está calibrado y no debe usarse para "
            "decisiones automáticas sobre personas."
        ),
        p("F. Vocabulario", "SectionCustom"),
        p(
            "10. Tomá 5 líneas de tu app.py y señalá en ellas: una clase, una instancia, "
            "un método, un atributo, un parámetro y su argumento, y un valor de retorno.",
            "SubCustom",
        ),
        p(
            "<font name='Courier'>L23  def clasificar_resena(texto: str) -&gt; tuple[str, str]:<br/>"
            "L51      cliente = Client(<br/>"
            "L52          src=endpoint_url,<br/>"
            'L57      predicciones = cliente.predict(texto, api_name="/clasificar")<br/>'
            "L75      return etiqueta, f&quot;{mejor['score']:.1%}&quot;</font>",
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
        p("Enlaces y declaración de uso de IA", "SubCustom"),
        table(
            [
                [p("<b>Elemento</b>"), p("<b>URL / evidencia</b>")],
                [p("Aplicación pública de Render"),
                 p(f'<link href="{RENDER_URL}">Abrir app de Render</link>')],
                [p("Space ZeroGPU de Hugging Face"),
                 p(f'<link href="{SPACE_URL}">Abrir Space en Hugging Face</link>')],
                [p("Repositorio con código y notebook"),
                 p(f'<link href="{REPOSITORY_URL}">Abrir carpeta TP_Integrador en GitHub</link>')],
                [p("Capturas de clasificación positiva y negativa"),
                 p("Incluidas en la sección de evidencias.")],
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
            "• Render Free: https://render.com/docs/free<br/>"
            "• Render compute plans: https://render.com/docs/compute-plans<br/>"
            "Revisar licencias y condiciones vigentes antes de entregar."
        ),
        PageBreak(),
        p("G. Evidencia de la aplicación publicada", "SectionCustom"),
        p(
            "Las siguientes capturas muestran dos pruebas reales realizadas en la app "
            "publicada: una reseña positiva y otra negativa. También se probó el envío "
            "vacío; la interfaz respondió con un aviso para escribir una reseña antes "
            "de analizarla.",
            "BodyCustom",
        ),
        p("Prueba positiva: “la comida estaba rica” → Positivo (83,4 %)", "SubCustom"),
        ReportImage(
            str(EVIDENCE_DIR / "app-resena-positiva.png"),
            width=174 * mm,
            height=78.7 * mm,
        ),
        Spacer(1, 3 * mm),
        p("Prueba negativa: “se tardaron en atenderme” → Negativo (83,5 %)", "SubCustom"),
        ReportImage(
            str(EVIDENCE_DIR / "app-resena-negativa.png"),
            width=174 * mm,
            height=78.7 * mm,
        ),
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D6E0E4"))
        canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawString(18 * mm, 9 * mm, f"TP Integrador | {STUDENT}")
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
        author=STUDENT,
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
        textbox(slide, 0.65, 7.08, 9.5, 0.2, "TP Integrador · revisión final de evidencias", 9, muted)
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
    textbox(slide, 1.35, 4.58, 4.4, 0.42, "TP Integrador · resultados medidos", 15, navy, True)
    textbox(slide, 1.2, 5.65, 10, 0.6, f"{STUDENT} · IFTS N.º 18 · {DELIVERY_DATE}", 16, white)

    slide = base("1 · Problema y objetivo", 2)
    rect(slide, 0.8, 1.4, 5.6, 4.7, pale)
    textbox(slide, 1.1, 1.7, 5.0, 0.5, "El problema", 23, teal, True)
    textbox(slide, 1.1, 2.35, 5.0, 3.2,
            "Leer muchas reseñas una por una dificulta resumir la experiencia de clientes.\n\n"
            "Objetivo: estimar si cada reseña es positiva, neutral o negativa.\n\n"
            "Un modelo aprovecha contexto y negación mejor que reglas por palabras clave; "
            "aun así puede equivocarse.",
            16, ink)
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
    textbox(slide, 1.1, 2.15, 5.0, 1.15,
            "8 idiomas, incluido español · POS/NEU/NEG\n"
            "≈198 M tweets según la ficha · 1,04 GiB.",
            15, ink)
    rect(slide, 6.8, 1.35, 5.8, 2.2, pale)
    textbox(slide, 7.1, 1.55, 5.1, 0.55, "RoBERTuito", 22, teal, True)
    textbox(slide, 7.1, 2.15, 5.0, 1.15,
            "Español · POS/NEU/NEG · TASS 2020\n"
            ">500 M tweets preentrenamiento · 415 MiB.",
            15, ink)
    rect(slide, 0.8, 3.95, 11.8, 2.15, navy)
    textbox(slide, 1.15, 4.15, 10.9, 0.55, "Resultados auténticos del notebook", 21, orange, True)
    textbox(slide, 1.15, 4.75, 10.9, 1.3,
            "Cardiff y RoBERTuito: 8/10 aciertos (80 %) cada uno.\n"
            "Frase de prueba: etiqueta negative, puntaje 0,7448.\n"
            "Tiempo: local 0,0593 s · Space 2,2485 s (incluye red).\n"
            "Se despliega Cardiff por compatibilidad; la muestra no demuestra superioridad.",
            14, white)

    slide = base("3 · Dónde viven el código y el modelo", 4)
    textbox(slide, 0.9, 1.35, 11.7, 0.9,
            "Aplicar un modelo ya entrenado a una entrada nueva para obtener una predicción.",
            22, ink)
    boxes = [
        (0.8, "Entrada\nreseña"),
        (3.25, "Render\napp.py"),
        (5.7, "API Gradio\nHTTPS"),
        (8.15, "HF Space\nZeroGPU"),
        (10.6, "Clase +\npuntaje"),
    ]
    for x, label in boxes:
        rect(slide, x, 3.0, 1.9, 1.4, pale)
        textbox(slide, x + 0.1, 3.15, 1.7, 1.0, label, 16, navy, True, PP_ALIGN.CENTER)
    for x in [2.75, 5.2, 7.65, 10.1]:
        textbox(slide, x, 3.25, 0.45, 0.5, "→", 22, teal, True, PP_ALIGN.CENTER)
    textbox(slide, 1.0, 4.85, 11.1, 0.55,
            "El código vive en GitHub y Render ejecuta app.py; los pesos viven en Hugging Face.",
            17, muted, align=PP_ALIGN.CENTER)
    textbox(slide, 1.0, 5.55, 11.1, 0.8,
            "Decisión: pipeline cargado ≈1,04 GiB; Render Free ≈512 MB RAM. "
            "La llamada remota medida fue 2,2485 s con gradio_client. "
            "InferenceClient no llama directamente a la API Gradio de esta Space ZeroGPU.",
            15, ink, align=PP_ALIGN.CENTER)

    slide = base("4 · Despliegue y alternativas", 5)
    rect(slide, 0.8, 1.35, 5.7, 4.8, pale)
    textbox(slide, 1.1, 1.65, 5.0, 0.5, "Por qué separar servicios", 22, teal, True)
    textbox(slide, 1.1, 2.25, 4.9, 3.55,
            "Render es PaaS: despliega desde GitHub sin administrar el SO.\n\n"
            "VPS: más control, más tareas de seguridad y mantenimiento.\n\n"
            "Local: no da URL pública persistente ni servicio al apagar la PC.\n\n"
            "Render Free duerme tras 15 min sin tráfico; al despertar tarda aprox. 1 min.",
            15, ink)
    rect(slide, 6.8, 1.35, 5.7, 4.8, pale)
    textbox(slide, 7.1, 1.65, 5.0, 0.5, "Evidencia de la app", 22, teal, True)
    slide.shapes.add_picture(
        str(EVIDENCE_DIR / "app-resena-positiva.png"),
        Inches(7.15),
        Inches(2.35),
        width=Inches(5.0),
        height=Inches(2.26),
    )
    textbox(slide, 7.1, 4.75, 5.0, 0.9,
            "Prueba positiva: “la comida estaba rica”\n"
            "Predicción: Positivo · puntaje: 83,4 %\n"
            "Render: semaforo-de-resenas.onrender.com",
            13, ink)

    slide = base("5 · Capturas de la aplicación funcionando", 6)
    slide.shapes.add_picture(
        str(EVIDENCE_DIR / "app-resena-negativa.png"),
        Inches(0.8),
        Inches(1.6),
        width=Inches(5.7),
        height=Inches(2.58),
    )
    slide.shapes.add_picture(
        str(EVIDENCE_DIR / "validacion-resena-vacia.png"),
        Inches(6.8),
        Inches(1.6),
        width=Inches(5.7),
        height=Inches(2.58),
    )
    textbox(slide, 0.9, 4.4, 5.5, 1.0,
            "Reseña: “se tardaron en atenderme”\n"
            "Resultado: Negativo · puntaje: 83,5 %",
            17, ink)
    textbox(slide, 6.9, 4.4, 5.5, 1.0,
            "Entrada vacía: la interfaz muestra el aviso\n"
            "“Escribí una reseña antes de analizarla”.",
            17, ink)

    slide = base("6 · Errores reales y aprendizajes", 7)
    rect(slide, 0.8, 1.35, 11.8, 2.2, pale)
    textbox(slide, 1.1, 1.55, 10.9, 0.65,
            "Hugging Face Space: “No @spaces.GPU function detected during startup”",
            18, teal, True)
    textbox(slide, 1.1, 2.25, 10.9, 1.05,
            "ZeroGPU no detectaba el callback dentro de FastAPI. Se cambió a Gradio nativo "
            "y se conectó directamente el handler decorado con @spaces.GPU.",
            16, ink)
    rect(slide, 0.8, 3.85, 11.8, 2.35, pale)
    textbox(slide, 1.1, 4.05, 10.9, 0.65,
            "Render: “When localhost is not accessible, a shareable link must be created”",
            18, teal, True)
    textbox(slide, 1.1, 4.75, 10.9, 1.1,
            "Gradio intentaba abrir localhost detrás del proxy. Se resolvió montando Gradio "
            "en FastAPI/Uvicorn, escuchando en 0.0.0.0 y en el puerto PORT, sin share=True.",
            16, ink)

    slide = base("7 · Límites y próximo paso", 8)
    rect(slide, 0.8, 1.35, 5.7, 4.9, navy)
    textbox(slide, 1.15, 1.7, 4.9, 0.55, "Límites", 22, orange, True)
    textbox(slide, 1.15, 2.4, 4.8, 3.3,
            "• 1.000 personas a la vez: no hay capacidad ni SLA garantizados.\n"
            "• Cola y cuota compartida ZeroGPU; Render Free duerme.\n"
            "• Cambios del plan gratis pueden requerir migración o pago.\n"
            "• El puntaje no es certeza ni debe decidir sobre personas.",
            16, white)
    rect(slide, 6.8, 1.35, 5.7, 4.9, pale)
    textbox(slide, 7.15, 1.7, 4.9, 0.55, "Próximo paso para un producto real", 20, teal, True)
    textbox(slide, 7.15, 2.4, 4.8, 3.3,
            "Probar carga, poner límites y observabilidad, gestionar colas, revisar privacidad "
            "y presupuestar un endpoint escalable. Medir errores con más reseñas etiquetadas.",
            17, ink)

    slide = base("8 · Enlaces para probar y revisar", 9)
    rect(slide, 0.8, 1.35, 5.7, 4.9, navy)
    textbox(slide, 1.15, 1.7, 4.9, 0.55, "Enlaces para la defensa", 22, orange, True)
    textbox(slide, 1.15, 2.4, 4.8, 3.5,
            f"App Render: {RENDER_URL}\n"
            f"Space Hugging Face: {SPACE_URL}\n"
            f"Repositorio: {REPOSITORY_URL}",
            13, white)
    rect(slide, 6.8, 1.35, 5.7, 4.9, pale)
    textbox(slide, 7.15, 1.7, 4.9, 0.55, "Antes de entregar", 22, teal, True)
    textbox(slide, 7.15, 2.4, 4.8, 2.8,
            "Cardiff y RoBERTuito: 8/10 aciertos cada uno.\n"
            "La app infiere; no entrena.\n"
            "La asistencia de IA se declara en el informe.",
            17, ink)

    prs.save(PPTX_PATH)


if __name__ == "__main__":
    make_pdf()
    make_presentation()
    print(f"PDF: {PDF_PATH}")
    print(f"PPTX: {PPTX_PATH}")
