import streamlit as st
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def crear_pdf_rubrica(pesos, criterios):
    archivo_pdf = "rubrica.pdf"
    doc = SimpleDocTemplate(archivo_pdf, pagesize=landscape(letter))

    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.wordWrap = "CJK"

    data = [["Criterio", "Peso", "Descripción", "Punteo"]]
    for criterio, peso in pesos.items():
        descripcion = Paragraph(criterios[criterio], style)
        data.append([criterio, f"{peso}%", descripcion, ""])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 1), (-1, -1), "MIDDLE")
    ]))

    doc.build([table])

    return archivo_pdf

st.title("RubriMaker")

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

criterios_seleccionados = st.multiiselect("Selecciona los criterios de evaluación:", list(criterios.keys()))

for criterio in criterios_seleccionados:
    with st.beta_expander(f"Definición de {criterio}"):
        st.write(criterios[criterio])

pesos = {}
for criterio in criterios_seleccionados:
    pesos[criterio] = st.slider(f"Asigna un peso a {criterio} (%):", 0, 100, 0)

if st.button("Generar rúbrica"):
    st.header("Rúbrica generada")
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        for criterio, peso in pesos.items():
            st.write(f"{criterio}: {peso}%")

if st.button("Descargar rúbrica en PDF"):
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        archivo_pdf = crear_pdf_rubrica(pesos, criterios)
        with open(archivo_pdf, "rb") as f:
            pdf_data = f.read()
        st.download_button("Descargar rúbrica", pdf_data, "rubrica.pdf", "application/pdf")

if st.button("Descargar rúbrica en PDF"):
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        archivo_pdf = crear_pdf_rubrica(pesos, criterios)
        with open(archivo_pdf, "rb") as f:
            pdf_data = f.read()
        st.download_button("Descargar rúbrica", pdf_data, "rubrica.pdf", "application/pdf")
