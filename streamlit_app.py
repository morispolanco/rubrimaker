import streamlit as st
import docx2txt
import openai
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Asigna la clave API de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Configuración de Streamlit
st.set_page_config(page_title="Calificador de Ensayos con GPT-3")
st.title("Calificador de Ensayos con GPT-3")

# Descripción de la aplicación
st.write("""
Esta aplicación permite crear una rúbrica para calificar ensayos según diferentes criterios y usar la API de GPT-3 para calificar los ensayos de acuerdo con los criterios seleccionados. Seleccione los criterios y su peso y cargue el archivo de Word con el ensayo que desea calificar. Luego, haga clic en el botón "Calificar ensayo" para obtener el resultado de la calificación.
""")

# Seleccionar los criterios y asignar un peso
st.header("Criterios de la rúbrica")

# Define los criterios en una lista
criterios = [1, 2, 3, 4, 5]

contenido = st.selectbox("Contenido", criterios)
comprension = st.selectbox("Comprensión", criterios)
precision = st.selectbox("Precisión", criterios)
creatividad = st.selectbox("Creatividad", criterios)
organizacion = st.selectbox("Organización", criterios)
presentacion = st.selectbox("Presentación", criterios)
coherencia = st.selectbox("Coherencia", criterios)
habilidad_tecnica = st.selectbox("Habilidad técnica", criterios)
investigacion = st.selectbox("Investigación", criterios)
participacion = st.selectbox("Participación", criterios)

# Cargar archivo de Word
uploaded_file = st.file_uploader("Cargar archivo de Word", type="docx")

if uploaded_file is not None:
    # Leer el contenido del archivo de Word
    docx_text = docx2txt.process(uploaded_file)

    prompt = f"""
    Calificar ensayo según los criterios seleccionados:
    Contenido: {contenido}
    Comprensión: {comprension}
    Precisión: {precision}
    Creatividad: {creatividad}
    Organización: {organizacion}
    Presentación: {presentacion}
    Coherencia: {coherencia}
    Habilidad técnica: {habilidad_tecnica}
    Investigación: {investigacion}
    Participación: {participacion}
    Ensayo: {docx_text}
    """

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=10,
    )

    result = response.choices[0].text

    # Mostrar el resultado de la calificación
    st.header("Resultado de la calificación")
    st.write(result)
