"""Genera el informe PDF y la presentacion PPT del trabajo final."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
STUDENT_NAME = "Pedro Bueno Pereyra"
PDF_PATH = ROOT / "TPF_Bueno_Pereyra_Pedro.pdf"
PPT_PATH = ROOT / "TPF_Bueno_Pereyra_Pedro.pptx"
APP_URL = "https://tp-final-deb0.onrender.com/"
GITHUB_URL = "https://github.com/pbuenos/seminario_de_actualizacion"

NAVY = colors.HexColor("#17233C")
TEAL = colors.HexColor("#008C95")
INK = colors.HexColor("#263238")
MUTED = colors.HexColor("#5F6B73")


def crear_pdf() -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TituloTP", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=22, leading=26, textColor=NAVY, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="SeccionTP", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=15, leading=18, textColor=TEAL, spaceBefore=10,
    ))
    styles.add(ParagraphStyle(
        name="PreguntaTP", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=7,
    ))
    styles.add(ParagraphStyle(
        name="CuerpoTP", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=13, textColor=INK, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="CodeTP", parent=styles["Code"], fontName="Courier",
        fontSize=8, leading=11, textColor=INK, backColor=colors.HexColor("#EEF3F7"),
        borderPadding=6, spaceBefore=4, spaceAfter=6,
    ))

    def p(texto: str, estilo: str = "CuerpoTP") -> Paragraph:
        return Paragraph(texto, styles[estilo])

    def architecture_diagram():
        drawing = Drawing(490, 140)
        drawing.add(String(4, 126, "PUBLICACION DEL CODIGO", fontName="Helvetica-Bold",
                           fontSize=8, fillColor=NAVY))

        def box(x, y, width, label):
            drawing.add(Rect(
                x, y, width, 34, rx=4, ry=4,
                fillColor=colors.HexColor("#F2F6F8"),
                strokeColor=TEAL,
                strokeWidth=1,
            ))
            for index, line in enumerate(label.split("\n")):
                drawing.add(String(
                    x + width / 2, y + 21 - index * 10, line,
                    fontName="Helvetica", fontSize=7.5,
                    fillColor=NAVY, textAnchor="middle",
                ))

        def arrow(x1, y, x2, label):
            drawing.add(Line(x1, y, x2 - 4, y,
                             strokeColor=TEAL, strokeWidth=1))
            drawing.add(Polygon(
                [x2 - 4, y, x2 - 8, y + 3, x2 - 8, y - 3],
                fillColor=TEAL,
                strokeColor=TEAL,
            ))
            drawing.add(String(
                (x1 + x2) / 2, y + 6, label,
                fontName="Helvetica", fontSize=6,
                fillColor=MUTED, textAnchor="middle",
            ))

        box(4, 82, 100, "PC local\nCSV + entrenamiento")
        box(197, 82, 100, "GitHub\ncodigo + modelo.joblib")
        box(390, 82, 96, "Render\nAPI + frontend")
        arrow(107, 99, 194, "push")
        arrow(300, 99, 387, "deploy")

        drawing.add(String(4, 64, "USO DE LA APLICACION: JSON DE ENTRADA Y PREDICCION", fontName="Helvetica-Bold",
                           fontSize=8, fillColor=NAVY))
        runtime = [
            (4, 68, "Navegador\nformulario"),
            (126, 80, "FastAPI\nvalida JSON"),
            (261, 80, "modelo.joblib\npredice en Render"),
            (396, 90, "Navegador\nrecibe JSON"),
        ]
        for x, width, label in runtime:
            box(x, 12, width, label)
        arrow(73, 29, 123, "POST")
        arrow(208, 29, 258, "features")
        arrow(343, 29, 393, "resultado")
        return drawing

    story = [
        Spacer(1, 15 * mm),
        p("TPF_Bueno_Pereyra_Pedro", "TituloTP"),
        p("Riesgo de abandono de empleados", "TituloTP"),
        Spacer(1, 8 * mm),
        p(f"<b>Alumno:</b> {STUDENT_NAME}"),
        p("<b>Institucion:</b> IFTS N.º 18"),
        p("<b>Materia:</b> Seminario de Actualizacion"),
        p("<b>Fecha:</b> 20/11/2026"),
        p(f'<b>Aplicacion:</b> <link href="{APP_URL}">{APP_URL}</link>'),
        p(f'<b>Repositorio:</b> <link href="{GITHUB_URL}">{GITHUB_URL}</link>'),
        PageBreak(),

        p("A. La arquitectura", "SeccionTP"),
        p("1. Esquema de cajas y flechas", "PreguntaTP"),
        p(
            "La computadora ejecuta el entrenamiento y genera <b>modelo.joblib</b>. "
            "GitHub guarda el codigo y el modelo. Render ejecuta FastAPI y carga el "
            "modelo una sola vez al iniciar. GitHub Pages o el mismo servidor sirve "
            "el frontend. El navegador envia el JSON de entrada y recibe el JSON de "
            "prediccion."
        ),
        p(
            "<b>Entrada:</b> edad, departamento, rol, salario mensual, satisfaccion "
            "laboral, anos en la empresa, horas extras, distancia al hogar, "
            "equilibrio vida-trabajo y anos desde el ultimo ascenso."
        ),
        p(
            "<b>Salida:</b> prediccion, probabilidad y nivel de riesgo."
        ),
        p(
            "<b>Codigo fuente:</b> usuario -> GitHub -> plataforma de deploy; "
            "<b>uso:</b> navegador -> POST /predecir -> FastAPI -> modelo.joblib "
            "-> respuesta JSON -> navegador."
        ),
        architecture_diagram(),

        p("2. Contrato de la API", "PreguntaTP"),
        p("GET /health", "PreguntaTP"),
        p('Entrada: sin cuerpo. Salida 200: {"estado":"ok","modelo":"random_forest",'
          '"scikit_learn":"1.8.0","dataset":"WA_Fn-UseC_-HR-Employee-Attrition.csv"}'),
        p("POST /predecir", "PreguntaTP"),
        p(
            "Ejemplo de entrada:",
            "CuerpoTP",
        ),
        p(
            '{"edad":29,"departamento":"Sales","rol":"Sales Executive",'
            '"salario_mensual":3200,"satisfaccion_laboral":3,'
            '"anos_en_la_empresa":2,"horas_extras":"Yes",'
            '"distancia_al_hogar":15,"equilibrio_vida_trabajo":3,'
            '"anos_desde_ultimo_ascenso":1}',
            "CodeTP",
        ),
        p(
            'Salida 200: {"prediccion":"Probable abandono","probabilidad":0.6606,'
            '"riesgo":"Medio"}'
        ),
        p(
            "Codigos posibles: 200 para una prediccion valida; 422 para campos "
            "faltantes, tipos incorrectos o valores fuera de rango; 500 si falla "
            "el servidor o el modelo."
        ),

        p("3. CORS", "PreguntaTP"),
        p(
            "CORS no aparecio durante la publicacion porque el frontend y el backend "
            "se sirven desde el mismo dominio de Render. De todos modos se configuro "
            "CORSMiddleware para GET y POST por si se separan en el futuro."
        ),
        p(
            "Para frontend separado se debe completar api-base-url en index.html "
            "con la URL HTTPS publica del backend."
        ),

        p("B. El deploy", "SeccionTP"),
        p("4. Dónde se publicó cada parte y por qué", "PreguntaTP"),
        p(
            "<b>Configuracion elegida:</b> Render Web Service para FastAPI y el "
            "frontend servido por StaticFiles. Render permite un repositorio GitHub "
            "directamente, requiere pocas configuraciones y admite FastAPI."
        ),
        p(
            "<b>Alternativa descartada 1: Hugging Face Spaces.</b> El plan gratuito "
            "puede suspenderse sin uso y FastAPI requiere preparar/configurar un "
            "contenedor Docker. Render resulto mas directo para conectar el repositorio "
            "y ejecutar el comando Uvicorn."
        ),
        p(
            "<b>Alternativa descartada 2: Vercel.</b> Puede integrar frontend y "
            "funciones Python sin CORS, pero el empaquetado serverless, sus limites "
            "de tamano/tiempo y el arranque de dependencias de ML requieren mas "
            "configuracion. El servicio web de Render admite este proceso sin adaptar "
            "FastAPI a una funcion serverless."
        ),
        p(
            "<b>Plan elegido:</b> Render Free ofrece alrededor de 512 MB de RAM y "
            "puede dormir tras unos 15 minutos sin actividad; el arranque en frio "
            "puede demorar aproximadamente 30-60 segundos. El modelo ocupa 3.03 MB, "
            "por debajo de la memoria disponible; el consumo total tambien incluye "
            "Python, scikit-learn, pandas y numpy."
        ),
        p(
            "El dataset WA_Fn-UseC_-HR-Employee-Attrition.csv se obtuvo de la copia "
            "IBM HR Analytics distribuida en Kaggle. Contiene 1470 filas y 35 "
            "columnas; no son registros "
            "reales de empleados de IBM. Se usaron diez variables no identificatorias: "
            "edad, departamento, rol, salario, satisfaccion, antiguedad, horas extra, "
            "distancia, equilibrio vida-trabajo y anos desde promocion. La etiqueta "
            "Attrition contiene 1233 No y 237 Yes."
        ),
        p(
            "Se compararon Regresion Logistica y Random Forest por F1 medio en "
            "validacion cruzada estratificada de 5 particiones sobre entrenamiento. "
            "Logistica obtuvo 44.72% y Random Forest 51.08%; se eligio Random Forest. "
            "El conjunto de prueba se reservo para la evaluacion final."
        ),
        p(
            "En los 294 casos de prueba: accuracy 82.99%, precision 45.71%, "
            "recall 34.04%, F1 39.02% y ROC-AUC 75.18%. Matriz: "
            "[[228, 19], [31, 16]]. El modelo ocupa aproximadamente 3.03 MB."
        ),
        p(
            f'<b>Aplicacion publicada:</b> <link href="{APP_URL}">{APP_URL}</link>. '
            f'<b>Repositorio:</b> <link href="{GITHUB_URL}">{GITHUB_URL}</link>.'
        ),
        p("5. Backend encendido o dormido", "PreguntaTP"),
        p(
            "El plan gratuito de Render puede dormir el servicio despues de "
            "inactividad. La primera solicitud posterior puede tardar 30-60 segundos "
            "por el arranque en frio. La app muestra estado de carga en el frontend "
            "y puede informarlo al usuario."
        ),

        p("C. Lo que se rompió", "SeccionTP"),
        p("6. Errores reales documentados", "PreguntaTP"),
        p(
            "Durante la publicacion en Render no se registraron errores. Los "
            "siguientes incidentes reales ocurrieron durante el desarrollo local."
        ),
        p(
            "<b>Error 1: puerto ocupado.</b> Lugar: terminal de Windows al iniciar "
            "Uvicorn local. Mensaje: <i>[Errno 10048] error while attempting to bind "
            "on address ('127.0.0.1', 8000): [winerror 10048] solo se permite un uso "
            "de cada direccion de socket</i>. Causa: el puerto 8000 estaba ocupado "
            "o reservado. Solucion: 1) se eligio el puerto 8080; 2) se ajusto la "
            "configuracion del frontend y README; 3) se comprobo /health y la pagina "
            "con HTTP 200."
        ),
        p(
            "<b>Error 2: impresion de metricas.</b> Lugar: "
            "<i>TP_Final/notebook/entrenamiento.py</i>, al imprimir el resultado del "
            "entrenamiento. Mensaje: <i>ValueError: Unknown format code 'f' for "
            "object of type 'str'</i>. Causa: el resumen mezclaba metricas numericas "
            "con valores textuales y aplicaba formato decimal a todos. Solucion: "
            "1) se identificaron explicitamente las metricas numericas; 2) se "
            "imprimieron con formato decimal; 3) la matriz, el reporte y el nombre "
            "del modelo se muestran por separado; 4) se reejecuto el entrenamiento."
        ),
        p(
            "Verificacion posterior: los 6 tests aprobados cubren health, prediccion "
            "valida, errores 422 por campo faltante/tipo incorrecto/categoria ajena "
            "y categorias validas del dataset."
        ),

        p("D. Límites y seguridad", "SeccionTP"),
        p("7. Uso masivo y fin del plan gratuito", "PreguntaTP"),
        p(
            "Con 1000 usuarios simultaneos, una instancia gratuita podria agotar "
            "CPU, memoria o conexiones y producir latencia, reinicios o errores 5xx. "
            "Un plan pago permitiria mas memoria, concurrencia y escalado. Cuando "
            "terminan los recursos gratuitos, el servicio puede suspenderse o dejar "
            "de atender solicitudes."
        ),
        p(
            "No se usan credenciales ni datos personales en el proyecto. Las claves "
            "futuras deben guardarse como secretos o variables de entorno en Render "
            "y nunca dentro de GitHub, .env incluido, ni en el frontend."
        ),
        p(
            "El dataset IBM HR es una muestra de demostracion y no son registros "
            "reales de empleados de IBM. El modelo no debe decidir despidos: puede "
            "servir para estudiar patrones del dataset, pero no establece causalidad "
            "ni reemplaza una revision humana."
        ),
        p("Uso de IA generativa", "SeccionTP"),
        p(
            "Se utilizo IA como asistente para resolver dudas, evaluar decisiones "
            "y apoyar la implementacion de partes del proyecto. Sus resultados se "
            "verificaron ejecutando la aplicacion localmente, probando la API y "
            "corriendo los tests."
        ),
    ]

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )
    doc.build(story)


def crear_ppt() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    navy = RGBColor(20, 33, 61)
    teal = RGBColor(0, 140, 149)
    orange = RGBColor(252, 163, 17)
    pale = RGBColor(242, 246, 248)
    ink = RGBColor(38, 50, 56)
    muted = RGBColor(95, 107, 115)
    white = RGBColor(255, 255, 255)
    green = RGBColor(28, 132, 86)
    red = RGBColor(177, 52, 52)

    def add_text(slide, text, x, y, w, h, size=20, color=ink, bold=False,
                 align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE):
        shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        frame = shape.text_frame
        frame.clear()
        frame.word_wrap = True
        frame.vertical_anchor = valign
        for index, line in enumerate(text.split("\n")):
            paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
            paragraph.text = line
            paragraph.alignment = align
            paragraph.font.name = "Aptos"
            paragraph.font.size = Pt(size)
            paragraph.font.bold = bold
            paragraph.font.color.rgb = color
        return shape

    def add_card(slide, x, y, w, h, heading, body, accent=teal, body_size=17):
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(w), Inches(h),
        )
        box.fill.solid()
        box.fill.fore_color.rgb = white
        box.line.color.rgb = RGBColor(218, 226, 231)
        strip = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), Inches(0.09), Inches(h),
        )
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent
        strip.line.fill.background()
        add_text(slide, heading, x + 0.25, y + 0.12, w - 0.45, 0.42,
                 size=16, color=navy, bold=True)
        add_text(slide, body, x + 0.25, y + 0.62, w - 0.48, h - 0.76,
                 size=body_size, color=ink, valign=MSO_ANCHOR.TOP)

    def new_slide(title, number, dark=False):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = navy if dark else pale
        if not dark:
            band = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12)
            )
            band.fill.solid()
            band.fill.fore_color.rgb = teal
            band.line.fill.background()
            add_text(slide, title, 0.65, 0.35, 12, 0.65, 27, navy, True)
            add_text(slide, f"PEDRO BUENO PEREYRA  |  TP FINAL  |  {number:02d}",
                     0.65, 7.12, 12, 0.2, 9, muted)
        return slide

    # 1. Portada
    slide = new_slide("", 1, dark=True)
    slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(9.25), Inches(-1.5), Inches(5.1), Inches(5.1)
    ).fill.solid()
    slide.shapes[-1].fill.fore_color.rgb = teal
    slide.shapes[-1].line.fill.background()
    slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(10.2), Inches(3.9), Inches(4.0), Inches(4.0)
    ).fill.solid()
    slide.shapes[-1].fill.fore_color.rgb = RGBColor(34, 52, 83)
    slide.shapes[-1].line.fill.background()
    add_text(slide, "PROYECTO INTEGRADOR  |  IFTS N.º 18",
             0.9, 0.85, 8.6, 0.45, 14, orange, True)
    add_text(slide, "Riesgo de abandono\nde empleados",
             0.9, 1.55, 9.5, 2.0, 37, white, True)
    add_text(slide, "Machine learning + API + aplicación web",
             0.95, 3.85, 8.7, 0.6, 21, RGBColor(205, 218, 228))
    add_text(slide, STUDENT_NAME, 0.95, 5.85, 7.5, 0.45, 18, white, True)
    add_text(slide, "Demostración académica; no reemplaza decisiones humanas.",
             0.95, 6.35, 9.5, 0.4, 12, RGBColor(205, 218, 228))

    # 2. Problema
    slide = new_slide("1. El problema que queremos resolver", 2)
    add_card(
        slide, 0.75, 1.35, 5.75, 3.1, "Pregunta",
        "¿Podemos estimar si un empleado podría abandonar la empresa a partir "
        "de algunas características laborales?",
        accent=teal, body_size=20,
    )
    add_card(
        slide, 6.8, 1.35, 5.75, 3.1, "Uso responsable",
        "La predicción podría orientar una conversación o una encuesta de clima. "
        "No debe usarse para despedir, sancionar ni etiquetar automáticamente.",
        accent=orange, body_size=19,
    )
    add_text(slide, "Objetivo: construir una demostración completa, desde los datos hasta una app web.",
             1.0, 5.25, 11.4, 0.8, 22, navy, True, PP_ALIGN.CENTER)

    # 3. Datos
    slide = new_slide("2. Los datos y qué significa la etiqueta", 3)
    add_card(
        slide, 0.75, 1.3, 3.8, 3.55, "Dataset",
        "1.470 filas, 35 columnas\n\nDataset IBM HR de demostración distribuido en Kaggle; no son empleados reales de IBM.",
        accent=teal, body_size=17,
    )
    add_card(
        slide, 4.77, 1.3, 3.8, 3.55, "Variables de entrada",
        "Edad, área, rol, salario, satisfacción, antigüedad, horas extra, distancia, equilibrio y promoción.",
        accent=orange, body_size=16,
    )
    add_card(
        slide, 8.78, 1.3, 3.8, 3.55, "Objetivo",
        "1.233 No\n\n237 Yes\n\nObjetivo: Attrition",
        accent=green, body_size=20,
    )
    add_text(
        slide,
        "Importante: dataset de demostración; las métricas no demuestran el rendimiento en una empresa real.",
        0.95, 5.45, 11.4, 0.8, 18, red, True, PP_ALIGN.CENTER,
    )

    # 4. Pipeline y comparación de modelos
    slide = new_slide("3. Cómo entrenamos el modelo", 4)
    steps = [
        ("Datos", "10 variables"),
        ("Preparación", "Escalado numérico\n+ One-Hot"),
        ("Comparación", "Regresión Logística\nvs. Random Forest"),
        ("Selección", "Mayor F1 CV\nsolo en train"),
    ]
    x_positions = [0.65, 3.8, 6.95, 10.1]
    for i, (head, body) in enumerate(steps):
        add_card(slide, x_positions[i], 1.65, 2.55, 2.35,
                 head, body, accent=teal if i != 3 else orange, body_size=16)
        if i < len(steps) - 1:
            add_text(slide, "→", x_positions[i] + 2.62, 2.35, 0.42, 0.5,
                     26, teal, True, PP_ALIGN.CENTER)
    add_text(
        slide,
        "Se divide el dataset en 80% para entrenamiento y 20% para prueba. "
        "Se usa class_weight='balanced'. La prueba se reserva hasta terminar "
        "la selección; la validación cruzada se aplica solo al entrenamiento.",
        1.0, 4.75, 11.3, 1.1, 18, navy, False, PP_ALIGN.CENTER,
    )
    add_text(
        slide,                 "Resultado: Random Forest obtuvo el mayor F1 CV (51,08%) y quedó exportado en modelo.joblib.",
        1.0, 6.0, 11.3, 0.55, 17, green, True, PP_ALIGN.CENTER,
    )

    # 5. Métricas
    slide = new_slide("4. Qué tan bien funciona", 5)
    metrics = [
        ("Accuracy", "82,99%", "Aciertos totales"),
        ("Precision", "45,71%", "Alertas correctas"),
        ("Recall", "34,04%", "Abandonos detectados"),
        ("F1", "39,02%", "Balance precision/recall"),
        ("ROC-AUC", "75,18%", "Separación entre clases"),
    ]
    for index, (name, value, desc) in enumerate(metrics):
        x = 0.55 + index * 2.57
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(1.45), Inches(2.35), Inches(2.15),
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = white
        shape.line.color.rgb = RGBColor(218, 226, 231)
        add_text(slide, name, x + 0.12, 1.7, 2.1, 0.4, 15, muted, True, PP_ALIGN.CENTER)
        add_text(slide, value, x + 0.1, 2.15, 2.15, 0.65, 25, teal, True, PP_ALIGN.CENTER)
        add_text(slide, desc, x + 0.15, 2.9, 2.05, 0.45, 12, ink, False, PP_ALIGN.CENTER)
    add_card(
        slide, 0.85, 4.15, 5.55, 1.65, "Matriz de confusión",
        "228 permanencias correctas · 16 abandonos detectados\n"
        "19 falsas alarmas · 31 abandonos no detectados",
        accent=orange, body_size=14,
    )
    add_card(
        slide, 6.7, 4.15, 5.75, 1.65, "Lectura honesta",
        "Aunque Accuracy es alta, Recall es 34,04%: detecta pocos abandonos. "
        "Hay fuerte desbalance de clases.",
        accent=red, body_size=14,
    )

    # 6. Predicción y niveles
    slide = new_slide("5. Cómo se obtiene una predicción", 6)
    add_card(
        slide, 0.8, 1.35, 5.65, 3.65, "Ejemplo de respuesta",
        "Ejemplo: probabilidad 66,06%\n\n"
        "Umbral de clase: 50%\n"
        "Como 66,06% supera 50%, predice “Probable abandono”.",
        accent=teal, body_size=19,
    )
    add_card(
        slide, 6.7, 1.35, 5.7, 3.65, "Nivel visual de riesgo",
        "Bajo: < 45%\n\nMedio: 45% a 69,99%\n\nAlto: ≥ 70%",
        accent=orange, body_size=20,
    )
    add_text(
        slide,
        "La probabilidad es una estimación del modelo, no una certeza ni una explicación causal.",
        0.9, 5.5, 11.5, 0.7, 18, red, True, PP_ALIGN.CENTER,
    )

    # 7. Arquitectura de la aplicación
    slide = new_slide("6. De la pantalla a la predicción", 7)
    flow = [
        ("Formulario", "HTML / CSS"),
        ("Solicitud", "JavaScript\nfetch + JSON"),
        ("API", "FastAPI\nPydantic"),
        ("Modelo", "Pipeline\njoblib"),
        ("Respuesta", "Probabilidad\n+ riesgo"),
    ]
    x_positions = [0.55, 3.1, 5.65, 8.2, 10.75]
    for index, (head, body) in enumerate(flow):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x_positions[index]), Inches(2.0), Inches(2.05), Inches(1.75),
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = white
        shape.line.color.rgb = teal
        add_text(slide, head, x_positions[index] + 0.1, 2.2, 1.85, 0.4,
                 15, navy, True, PP_ALIGN.CENTER)
        add_text(slide, body, x_positions[index] + 0.1, 2.75, 1.85, 0.7,
                 14, ink, False, PP_ALIGN.CENTER)
        if index < len(flow) - 1:
            add_text(slide, "→", x_positions[index] + 2.05, 2.55, 0.45, 0.5,
                     24, orange, True, PP_ALIGN.CENTER)
    add_card(
        slide, 1.0, 4.55, 5.4, 1.45, "GET /health",
        "Confirma que la API y el modelo están disponibles.",
        accent=green, body_size=15,
    )
    add_card(
        slide, 6.85, 4.55, 5.4, 1.45, "POST /predecir",
        "Valida los datos; responde 200 si son válidos y 422 si hay errores.",
        accent=orange, body_size=15,
    )

    # 8. Publicación
    slide = new_slide("7. Aplicación publicada", 8)
    add_card(
        slide, 0.8, 1.35, 5.75, 3.3, "Aplicación en Render",
        APP_URL + "\n\n"
        "Render ejecuta FastAPI y sirve también el frontend. "
        "En plan gratuito puede tardar en responder tras un periodo inactivo.",
        accent=teal, body_size=17,
    )
    add_card(
        slide, 6.8, 1.35, 5.75, 3.3, "Repositorio del proyecto",
        GITHUB_URL + "\n\n"
        "Incluye el código, el entrenamiento, los tests y el modelo exportado.",
        accent=orange, body_size=17,
    )
    add_text(
        slide,
        "Alternativas descartadas: Hugging Face Spaces requiere Docker; Vercel añade límites y configuración serverless. Render fue más directo para FastAPI.",
        0.8, 4.78, 11.8, 0.55, 13, muted, False, PP_ALIGN.CENTER,
    )
    add_text(slide, "Demo: completar el formulario, observar la probabilidad y probar una entrada inválida.",
             0.95, 5.5, 11.5, 0.7, 18, navy, True, PP_ALIGN.CENTER)

    # 9. Tests y errores reales
    slide = new_slide("8. Pruebas y problemas resueltos", 9)
    add_card(
        slide, 0.8, 1.3, 5.75, 3.9, "Verificaciones",
        "6 tests aprobados:\n"
        "• Estado /health\n"
        "• Predicción válida\n"
        "• Campo faltante → HTTP 422\n"
        "• Tipo incorrecto → HTTP 422",
        accent=green, body_size=17,
    )
    add_card(
        slide, 6.8, 1.3, 5.75, 3.9, "Durante el desarrollo",
        "• Puerto 8000 ocupado en Windows (10048); se usó 8080.\n\n"
        "• Error de formato al imprimir métricas; se separaron números y textos.\n\n"
        "No hubo errores en el deploy de Render.",
        accent=orange, body_size=16,
    )
    add_text(slide, "Los tests comprueban comportamiento técnico, no la calidad real de las predicciones.",
             1.0, 5.75, 11.2, 0.65, 17, muted, False, PP_ALIGN.CENTER)

    # 10. Cierre, límites, seguridad y próximos pasos
    slide = new_slide("", 10, dark=True)
    add_text(slide, "9. Límites, seguridad y próximos pasos",
             0.75, 0.45, 11.8, 0.7, 27, white, True)
    add_card(
        slide, 0.75, 1.45, 5.75, 2.8, "Límites y seguridad",
        "• Dataset de demostración, no empleados reales.\n"
        "• Recall bajo para la clase Yes; el modelo omite casos.\n"
        "• El plan gratuito puede dormir; 1000 usuarios pueden superar recursos.\n"
        "• No automatizar decisiones laborales ni publicar secretos.",
        accent=red, body_size=14,
    )
    add_card(
        slide, 6.8, 1.45, 5.75, 2.8, "Próximos pasos",
        "• Datos reales autorizados y mejor documentados.\n"
        "• Explicar qué variables influyen en cada resultado.\n"
        "• Evaluar otros umbrales y mejorar el Recall.",
        accent=teal, body_size=15,
    )
    add_text(
        slide,
        "Uso de IA: asistente para dudas, opiniones y apoyo a la implementación; "
        "se verificó con ejecución, API y tests.",
        0.9, 4.7, 11.5, 1.0, 15, RGBColor(205, 218, 228),
    )
    add_text(
        slide,
        "Conclusión: integramos modelo, API, frontend y publicación; es una demostración académica.",
        0.9, 5.9, 11.5, 0.65, 17, orange, True, PP_ALIGN.CENTER,
    )
    add_text(slide, f"{STUDENT_NAME}  |  IFTS N.º 18",
             1.0, 6.7, 11.3, 0.35, 12, white, True, PP_ALIGN.CENTER)

    prs.save(PPT_PATH)


if __name__ == "__main__":
    crear_pdf()
    crear_ppt()
    print(PDF_PATH)
    print(PPT_PATH)
