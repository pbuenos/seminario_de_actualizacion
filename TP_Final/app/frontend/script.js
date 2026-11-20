// Configura api-base-url en index.html al publicar frontend y backend en dominios distintos.
// Un valor vacio consulta la misma origen, como ocurre al servir todo desde Render.
const API_URL_CONFIG =
  document.querySelector('meta[name="api-base-url"]')?.content.trim().replace(/\/$/, "") || "";
const esLocal =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";
const API_URL = API_URL_CONFIG || (esLocal ? "http://localhost:8080" : "");

const formulario = document.querySelector("#formulario");
const resultado = document.querySelector("#resultado");

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  resultado.className = "";
  resultado.textContent = "Consultando al modelo...";
  const boton = formulario.querySelector("button");
  boton.disabled = true;

  const datosFormulario = new FormData(formulario);
  const datos = Object.fromEntries(datosFormulario.entries());

  for (const campo of [
    "edad",
    "salario_mensual",
    "satisfaccion_laboral",
    "anos_en_la_empresa",
    "distancia_al_hogar",
    "equilibrio_vida_trabajo",
    "anos_desde_ultimo_ascenso",
  ]) {
    datos[campo] = Number(datos[campo]);
  }

  try {
    const respuesta = await fetch(`${API_URL}/predecir`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    const cuerpo = await respuesta.json();
    if (!respuesta.ok) {
      throw new Error(cuerpo.detail?.[0]?.msg || "Los datos enviados no son validos.");
    }

    resultado.className = `contenido ok-${cuerpo.riesgo.toLowerCase()}`;
    resultado.innerHTML =
      `<strong>${cuerpo.prediccion}</strong><br>` +
      `Probabilidad de abandono: ${(cuerpo.probabilidad * 100).toFixed(1)}% · ` +
      `Riesgo ${cuerpo.riesgo}<br>` +
      `<meter min="0" max="1" value="${cuerpo.probabilidad}" low="0.45" high="0.70" optimum="0"></meter>`;
  } catch (error) {
    resultado.className = "contenido error";
    resultado.textContent =
      `No se pudo obtener la predicción. ${error.message} ` +
      "Comprobá que la API esté disponible.";
  } finally {
    boton.disabled = false;
  }
});
