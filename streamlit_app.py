import streamlit as st
import docx2txt
import openai

# Configuración de Streamlit
st.set_page_config(page_title="Calificador de Ensayos con GPT-3")

# Título de la aplicación
st.title("Calificador de Ensayos con GPT-3")

# Descripción de la aplicación
st.write("""
Esta aplicación permite crear una rúbrica para calificar ensayos según diferentes criterios y usar la API de GPT-3 para calificar los ensayos de acuerdo con los criterios seleccionados.

Seleccione los criterios y su peso y cargue el archivo de Word con el ensayo que desea calificar. Luego, haga clic en el botón "Calificar ensayo" para obtener el resultado de la calificación.

Nota: Debe proporcionar su propia API Key de OpenAI para utilizar la API de GPT-3. Puede obtener su propia API Key en https://beta.openai.com/signup/.
""")

# Seleccionar los criterios y asignar un peso
st.header("Criterios de la rúbrica")
contenido = st.selectbox("Contenido", [1, 2, 3, 4, 5])
comprension = st.selectbox("Comprensión", [1, 2, 3, 4, 5])
precision = st.selectbox("Precisión", [1, 2, 3, 4, 5])
creatividad = st.selectbox("Creatividad", [1, 2, 3, 4, 5])
organizacion = st.selectbox("Organización", [1, 2, 3, 4, 5])
presentacion = st.selectbox("Presentación", [1, 2, 3, 4, 5])
coherencia = st.selectbox("Coherencia", [1, 2, 3, 4, 5])
habilidad_tecnica = st.selectbox("Habilidad técnica", [1, 2, 3, 4, 5])
investigacion = st.selectbox("Investigación", [1, 2, 3, 4, 5])
participacion = st.selectbox("Participación", [1, 2, 3, 4, 5])

# Cargar archivo de Word
uploaded_file = st.file_uploader("Cargar archivo de Word", type="docx")

if uploaded_file is not None:
    # Leer el contenido del archivo de Word
    docx_text = docx2txt.process(uploaded_file)
    
    # Llamar a la API de GPT-3 para evaluar el contenido del ensayo
    openai.api_key = "API_KEY" # Reemplazar con tu propia API Key
    prompt = f"Calificar ensayo según los criterios seleccionados:\n\nContenido: {contenido}\nComprensión: {comprension}\nPrecisión: {precision}\nCreatividad: {creatividad}\nOrganización: {organizacion}\nPresentación: {presentacion}\nCoherencia: {coherencia}\nHabilidad técnica: {habilidad_tecnica}\nInvestigación: {investigacion}\nParticipación: {participacion}\n\nEnsayo
response = openai.Completion.create(
    engine="text-davinci-003",
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
