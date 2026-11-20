"""Genera el informe PDF y la presentacion PPT del trabajo final."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
STUDENT_NAME = "Pedro Bueno Pereyra"
PDF_PATH = ROOT / "TPF_Pedro_Bueno_Pereyra.pdf"
PPT_PATH = ROOT / "TPF_Pedro_Bueno_Pereyra.pptx"
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

    story = [
        Spacer(1, 15 * mm),
        p("TPF_Pedro_Bueno_Pereyra", "TituloTP"),
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

        p("2. Contrato de la API", "PreguntaTP"),
        p("GET /health", "PreguntaTP"),
        p('Entrada: sin cuerpo. Salida 200: {"estado":"ok","modelo":"random_forest",'
          '"scikit_learn":"1.8.0"}'),
        p("POST /predecir", "PreguntaTP"),
        p(
            "Ejemplo de entrada:",
            "CuerpoTP",
        ),
        p(
            '{"edad":29,"departamento":"Ventas","rol":"Ejecutivo comercial",'
            '"salario_mensual":3200,"satisfaccion_laboral":3,'
            '"anos_en_la_empresa":2,"horas_extras":"Yes",'
            '"distancia_al_hogar":15,"equilibrio_vida_trabajo":3,'
            '"anos_desde_ultimo_ascenso":1}',
            "CodeTP",
        ),
        p(
            'Salida 200: {"prediccion":"Probable abandono","probabilidad":0.5338,'
            '"riesgo":"Medio"}'
        ),
        p(
            "Codigos posibles: 200 para una prediccion valida; 422 para campos "
            "faltantes, tipos incorrectos o valores fuera de rango; 500 si falla "
            "el servidor o el modelo."
        ),

        p("3. CORS", "PreguntaTP"),
        p(
            "CORS apareceria si frontend y backend quedan en dominios distintos, "
            "por ejemplo GitHub Pages y Render. Se resolvio habilitando "
            "CORSMiddleware en FastAPI para metodos GET y POST. Si se publica todo "
            "dentro de Render no se requiere una solicitud cross-origin, pero la "
            "configuracion queda lista para una separacion futura."
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
            "<b>Alternativa descartada 1: Hugging Face Spaces.</b> Permite Docker "
            "y es conocido, pero un servicio puede suspenderse sin uso y las "
            "condiciones requieren revision."
        ),
        p(
            "<b>Alternativa descartada 2: Vercel.</b> Puede integrar frontend y "
            "serverless Python sin CORS, pero el limite de peso y el arranque de "
            "la funcion resultan menos sencillos para scikit-learn y numpy."
        ),
        p(
            "El modelo Random Forest exportado pesa aproximadamente 5.60 MB y entra "
            "holgadamente en el limite de memoria indicado para esta entrega."
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
            "siguientes dos incidentes ocurrieron durante el desarrollo y las "
            "pruebas locales, no durante el deploy."
        ),
        p(
            "<b>Error 1: puerto ocupado.</b> Mensaje: "
            "<i>[Errno 10048] solo se permite un uso de cada direccion de socket "
            "para el protocolo/direccion</i>. Aparecio al iniciar Uvicorn en 8000 "
            "en Windows. La causa fue que el puerto estaba ocupado o reservado. "
            "Se resolvio iniciando la app en 8080 y configurando frontend y README "
            "con el mismo puerto."
        ),
        p(
            "<b>Error 2: formato de impresion de metricas.</b> El script intento "
            "aplicar formato decimal a una cadena al imprimir el resumen. Aparecio "
            "después de comparar modelos. Se corrigio limitando el formato decimal "
            "a las metricas numericas y mostrando por separado la comparacion."
        ),
        p(
            "Verificacion posterior: los 4 tests aprobados comprueban health, "
            "prediccion valida, campo faltante y tipo incorrecto."
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
            "El dataset es sintetico y el modelo no debe decidir despidos. Puede "
            "servir para mostrar patrones generales, pero no establece causalidad "
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

    slides = [
        ("Riesgo de abandono de empleados", f"{STUDENT_NAME} | IFTS N.º 18"),
        ("Problema y datos", "Predecir abandono laboral. Dataset sintetico reproducible de 2000 registros."),
        ("Datos y modelo", "Se compararon Regresion Logistica y Random Forest. Random Forest tuvo el mejor F1."),
        ("Metricas finales", "Accuracy 60.25% | Precision 60.09% | Recall 65.69% | F1 62.76% | ROC-AUC 63.59%"),
        ("Arquitectura", "Navegador -> frontend -> POST JSON -> FastAPI -> modelo.joblib -> respuesta"),
        ("Contrato y demo", "GET /health y POST /predecir. Pydantic valida 422. Demo valida y entrada invalida."),
        ("Deploy", f"Render: {APP_URL}\nGitHub: {GITHUB_URL}"),
        ("Errores reales", "No hubo errores durante el deploy. En desarrollo local: puerto 8000 ocupado (10048), se cambió a 8080; error de formato al imprimir métricas, corregido separando textos y números."),
        ("Limites y seguridad", "Arranque en frio, 1000 usuarios simultaneos, plan terminado, secretos fuera de GitHub."),
        ("Uso de IA y conclusion", "IA como asistente para resolver dudas, evaluar decisiones y apoyar la implementacion. Verificacion con ejecucion local, API y tests."),
        ("Conclusión y próximos pasos", "Proyecto técnico funcionando. Mejoras: datos reales, explicabilidad y ajuste de umbral."),
    ]

    for titulo, cuerpo in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(238, 243, 247)

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(1.2))
        title = title_box.text_frame.paragraphs[0]
        title.text = titulo
        title.font.size = Pt(30)
        title.font.bold = True
        title.font.color.rgb = RGBColor(23, 35, 60)

        body_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(4))
        body = body_box.text_frame.paragraphs[0]
        body.text = cuerpo
        body.font.size = Pt(16 if "https://" in cuerpo else 22)
        body.font.color.rgb = RGBColor(38, 50, 56)

    prs.save(PPT_PATH)


if __name__ == "__main__":
    crear_pdf()
    crear_ppt()
    print(PDF_PATH)
    print(PPT_PATH)
