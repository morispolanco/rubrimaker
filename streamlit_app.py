import streamlit as st

# Título de la aplicación
st.title("RubriMaker")

# Seleccionar criterios de evaluación
criterios = ["Contenido", "Creatividad", "Precisión", "Comprensión", "Presentación", "Coherencia", "Organización", "Investigación", "Participación"]
criterios_seleccionados = st.multiselect("Selecciona los criterios de evaluación:", criterios)

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
