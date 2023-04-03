import streamlit as st
import openai
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch

# Función para crear el PDF
def crear_pdf_rubrica(pesos, criterios):
    pdf = SimpleDocTemplate("rubrica.pdf", pagesize=letter)
    data = [["Criterio", "Descripción", "Peso", "Punteo"]]
    
    for criterio, peso in pesos.items():
        data.append([criterio, criterios[criterio], f"{peso}%", ""])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    pdf.build([table])

# Función para calificar ensayos utilizando GPT
def calificar_ensayo(ensayo, rubrica, criterios):
    openai.api_key = "your_openai_api_key"
    model_engine = "text-davinci-002"
    
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
