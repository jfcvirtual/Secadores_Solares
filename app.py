import streamlit as st

from ui import apply_visual_style

st.set_page_config(
    page_title="Secadores | Apéndices y diseño experimental",
    page_icon=":material/wb_sunny:",
    layout="wide",
)
apply_visual_style()

st.title("Evaluación de secadores")
st.caption("Apéndices resueltos y actividad de diseño experimental")
st.markdown(
    "Guía técnica de secado y propuesta de comparación experimental de cuatro "
    "secadores durante el proceso y el almacenamiento."
)
st.divider()

page_details = [
    (
        "Apéndice 7",
        "Eficiencia global de secado y eficiencia de captación de humedad.",
        "pages/1_Apendice_7.py",
        "Abrir cálculo",
    ),
    (
        "Apéndice 12",
        "Altura de chimenea y caudal de aire por convección natural.",
        "pages/2_Apendice_12.py",
        "Abrir cálculo",
    ),
    (
        "Apéndice 13",
        "Caudal a través del lecho y potencia estimada del ventilador.",
        "pages/3_Apendice_13.py",
        "Abrir cálculo",
    ),
    (
        "Actividad experimental",
        "Diseño factorial, aleatorización y protocolo de medición hasta 15 días de almacenamiento.",
        "pages/4_Diseno_y_protocolo.py",
        "Abrir DBCA",
    ),
    (
        "Actividad experimental DCA",
        "Alternativa sencilla con tratamientos completamente aleatorizados y réplicas ajustables.",
        "pages/5_DCA_factorial.py",
        "Abrir DCA",
    ),
]

for row_start in range(0, len(page_details), 2):
    columns = st.columns(2)
    for column, (title, description, page, label) in zip(
        columns,
        page_details[row_start : row_start + 2],
    ):
        with column:
            with st.container(border=True):
                st.subheader(title)
                st.write(description)
                st.page_link(page, label=label, use_container_width=True)

st.markdown("### Convenciones")
st.markdown(
    "Las humedades de los productos se expresan en base húmeda; los caudales "
    "superficiales se indican por unidad de área del lecho. Cada página conserva "
    "los datos y resultados del apéndice y muestra la sustitución numérica. "
    "La actividad ofrece dos alternativas de diseño factorial, DBCA y DCA, "
    "con un calendario de mediciones ajustable a los recursos disponibles."
)
st.caption("Fuente: Solar_Dryers-APENDICES.pdf, apéndices 7, 12 y 13.")
