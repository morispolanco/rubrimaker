import streamlit as st
import openai
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Asigna la clave API de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Función para crear el PDF
# Define la función que crea la rúbrica
def crear_rubrica():
    st.header("Creación de la rúbrica")
    st.write("Seleccione los criterios de evaluación y asigne un peso a cada uno.")
    pesos = {}

    # Obtiene la descripción de cada criterio
    criterios = {
        "Contenido": "¿El trabajo cumple con los requisitos del proyecto? ¿Está completo y bien desarrollado?",
        "Comprensión": "¿El estudiante comprende el tema y puede explicarlo en sus propias palabras?",
        "Precisión": "¿Hay errores en la información presentada? ¿La información es correcta y precisa?",
        "Creatividad": "¿El trabajo demuestra originalidad y creatividad? ¿El estudiante ha utilizado ideas y técnicas nuevas y únicas para crear el trabajo?",
        "Organización": "¿El trabajo está organizado y bien estructurado? ¿Hay una introducción, desarrollo y conclusión clara?",
        "Presentación": "¿El trabajo está presentado de manera profesional y limpia? ¿Se ha utilizado una presentación adecuada para el proyecto, como imágenes, gráficos y diseños?",
        "Coherencia": "¿Hay una conexión clara entre las diferentes partes del trabajo? ¿El trabajo tiene un flujo lógico y coherente?",
        "Habilidad técnica": "¿El estudiante ha utilizado habilidades técnicas apropiadas para el proyecto, como gramática, ortografía y puntuación adecuadas?",
        "Investigación": "¿El estudiante ha investigado adecuadamente el tema? ¿Se ha utilizado una variedad de fuentes, incluyendo fuentes confiables?",
        "Participación": "¿El estudiante ha participado activamente en el proyecto y ha contribuido significativamente al trabajo en equipo?"
    }

    # Selecciona el peso de cada criterio
    for criterio in criterios:
        peso = st.slider(criterio, 0, 100, step=5)
        pesos[criterio] = peso

    # Crea la rúbrica
    if st.button("Descargar rúbrica en PDF"):
        crear_pdf_rubrica(pesos, criterios)

# Función para calificar ensayos utilizando GPT
def calificar_ensayo(ensayo, rubrica, criterios):
    model_engine = "text-davinci-003"
    
    prompt = f"Calificar el siguiente ensayo según la rúbrica proporcionada:\n\n{ensayo}\n\nRubrica:\n"
    for criterio in rubrica:
        prompt += f"{criterio}: {criterios[criterio]}\n"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    result = response.choices[0].text.strip()
    return result
st.title("RubriMaker")

criterios = {
    # Aquí van todos los criterios y sus descripciones
}

criterios_seleccionados = st.multiselect("Selecciona los criterios de evaluación:", list(criterios.keys()))

for criterio in criterios_seleccionados:
    with st.beta_expander(f"Definición de {criterio}"):
        st.write(criterios[criterio])

pesos = {}
for criterio in criterios_seleccionados:
    pesos[criterio] = st.slider(f"Asigna un peso a {criterio} (%):", 0, 100, 0)

if st.button("Generar rúbrica", key="generar_rubrica"):
    st.header("Rúbrica generada")
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        for criterio, peso in pesos.items():
            st.write(f"{criterio}: {peso}%")

if st.button("Descargar rúbrica en PDF", key="descargar_rubrica"):
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        archivo_pdf = crear_pdf_rubrica(pesos, criterios)
        with open(archivo_pdf, "rb") as f:
            pdf_data = f.read()
        st.download_button("Descargar rúbrica", pdf_data, "rubrica.pdf", "application/pdf")

uploaded_file = st.file_uploader("Sube un archivo de texto con el ensayo (.txt):", type="txt")

if uploaded_file is not None:
    ensayo = uploaded_file.read().decode("utf-8")
    if st.button("Calificar ensayo", key="calificar_ensayo"):
        total = sum(pesos.values())
        if total != 100:
            st.error("La suma de los pesos debe ser igual al 100%.")
        else:
            calificaciones = calificar_ensayo(ensayo, pesos.keys(), criterios)
            st.write(calificaciones)

if st.button("Descargar rúbrica en PDF"):
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        archivo_pdf = crear_pdf_rubrica(pesos, criterios)
        st.download_button("Descargar PDF", archivo_pdf, "rubrica.pdf", "application/pdf")
