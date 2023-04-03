import streamlit as st

# Título de la aplicación
st.title("RubriMaker")

# Seleccionar criterios de evaluación
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

criterios_seleccionados = st.multiselect("Selecciona los criterios de evaluación:", list(criterios.keys()))

# Mostrar definiciones de criterios en ventanas emergentes
for criterio in criterios_seleccionados:
    with st.beta_expander(f"Definición de {criterio}"):
        st.write(criterios[criterio])

# Asignar pesos a los criterios seleccionados
pesos = {}
for criterio in criterios_seleccionados:
    pesos[criterio] = st.slider(f"Asigna un peso a {criterio} (%):", 0, 100, 0)

# Mostrar rúbrica
if st.button("Generar rúbrica"):
    st.header("Rúbrica generada")
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        for criterio, peso in pesos.items():
            st.write(f"{criterio}: {peso}%")

# Guardar rúbrica en un archivo
if st.button("Guardar rúbrica"):
    total = sum(pesos.values())
    if total != 100:
        st.error("La suma de los pesos debe ser igual al 100%.")
    else:
        with open("rubrica.txt", "w") as f:
            for criterio, peso in pesos.items():
                f.write(f"{criterio}: {peso}%\n")
        st.success("Rúbrica guardada en rubrica.txt")
