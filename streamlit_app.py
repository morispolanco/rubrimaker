import streamlit as st
import openai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch

# Función para crear el PDF
def crear_pdf_rubrica(pesos, criterios):
    archivo_pdf = "rubrica.pdf"
    doc = SimpleDocTemplate(archivo_pdf, pagesize=letter)

    data = [["Criterio", "Peso", "Punteo", "Descripción"]]
    for criterio, peso in pesos.items():
        data.append([criterio, f"{peso}%", "", criterios[criterio]])

    table = Table(data, colWidths=[1.5 * inch, 1 * inch, 1 * inch, 2.5 * inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))

    doc.build([table])

    return archivo_pdf

# Función para calificar ensayos utilizando GPT
def calificar_ensayo(ensayo, rubrica, criterios):
    openai.api_key = "tu_api_key_aqui"

    calificaciones = {}
    for criterio in rubrica:
        prompt = f"Evalúa el siguiente ensayo basado en el criterio '{criterio}': {criterios[criterio]}\n\nEnsayo:\n{ensayo}\n\nCalificación:"
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=10, n=1, stop=None, temperature=0.5)
        calificacion = response.choices[0].text.strip()
        calificaciones[criterio] = calificacion

    return calificaciones
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
            st.error("La suma de los pesos debe ser igual al 
