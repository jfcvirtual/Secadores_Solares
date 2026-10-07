import streamlit as st

from ui import apply_visual_style

st.set_page_config(
    page_title="Apéndice 12 | Convección natural",
    page_icon=":material/air:",
    layout="wide",
)
apply_visual_style()

ambient_temperature_c = 25.0
dryer_temperature_c = 40.0
cloudy_temperature_c = 30.0
bed_depth_m = 0.2
bed_velocity_m_s = 0.0055
chamber_height_m = 0.6
base_height_m = 1.0
density_slope_kg_m3_c = 0.00308
gravity_m_s2 = 9.81
rice_flow_coefficient = 0.0008
rice_flow_exponent = 0.87
flow_coefficient = rice_flow_coefficient * (
    density_slope_kg_m3_c * gravity_m_s2
) ** rice_flow_exponent
temperature_rise_c = dryer_temperature_c - ambient_temperature_c


def rice_bed_velocity(total_column_height_m: float, delta_temperature_c: float) -> float:
    return flow_coefficient * (
        delta_temperature_c * total_column_height_m / bed_depth_m
    ) ** rice_flow_exponent


required_column_height_m = (
    bed_depth_m
    / temperature_rise_c
    * (bed_velocity_m_s / flow_coefficient) ** (1 / rice_flow_exponent)
)
chimney_height_m = required_column_height_m - chamber_height_m - base_height_m
chimney_height_up_m = chimney_height_m * (4 / 3)
column_height_up_m = base_height_m + chamber_height_m + chimney_height_up_m
velocity_up_m_s = rice_bed_velocity(column_height_up_m, temperature_rise_c)
chimney_height_down_m = chimney_height_m * (2 / 3)
column_height_down_m = base_height_m + chamber_height_m + chimney_height_down_m
velocity_down_m_s = rice_bed_velocity(column_height_down_m, temperature_rise_c)
cloudy_velocity_m_s = rice_bed_velocity(
    required_column_height_m,
    cloudy_temperature_c - ambient_temperature_c,
)

st.title("Apéndice 12 · Convección natural")
st.caption("Dimensionamiento de una chimenea solar para secado de arroz")
st.markdown(
    "El aire ambiente está a 25 °C y 60 % de humedad relativa. Se requiere "
    "calentarlo hasta 40 °C y obtener 5,5 mm/s de velocidad superficial "
    "a través de un lecho de arroz de 0,20 m. La cámara mide 0,60 m de alto "
    "y su base está a 1,00 m del suelo."
)
st.info(
    "La velocidad dada es superficial: caudal volumétrico dividido por el "
    "área de sección del lecho. En la correlación, H es la altura total de "
    "la columna caliente, no solo la chimenea."
)

st.subheader("Hipótesis del modelo")
st.markdown(
    "- Temperatura y densidad del aire uniformes dentro del secador.\n"
    "- Sin fugas laterales; el aire caliente sale por la chimenea.\n"
    "- El secado ocurre por convección, sin contar radiación directa.\n"
    "- La resistencia del lecho domina frente a la del colector, la cámara y la chimenea."
)

st.subheader("Relación entre tiro, lecho y caudal")
st.markdown(
    "La diferencia de presión se debe a la diferencia de densidad entre el "
    "aire ambiente y la columna caliente. Para el intervalo considerado, el "
    "apéndice aproxima la densidad del aire mediante una relación lineal con T."
)
st.latex(r"\rho=1.11363-0.00308T\qquad [\mathrm{kg\,m^{-3}}]")
st.latex(
    r"\Delta P=(\rho_1-\rho_2)gH"
    r"\approx0.00308\,\Delta T\,gH"
)
st.latex(
    r"v=a\left(\frac{\Delta P}{h_b}\right)^b"
    r",\qquad a=0.0008,\quad b=0.87"
)
st.latex(
    r"v=3.81\times10^{-5}"
    r"\left(\frac{\Delta T\,H}{h_b}\right)^{0.87}"
    r"\qquad\text{(ecuación A12.4)}"
)
st.latex(
    r"H=\frac{h_b}{\Delta T}"
    r"\left(\frac{v}{3.81\times10^{-5}}\right)^{1/0.87}"
)

st.subheader("1. Altura necesaria")
st.latex(
    rf"H=\frac{{0.20}}{{15}}"
    rf"\left(\frac{{0.0055}}{{3.81\times10^{{-5}}}}\right)^{{1/0.87}}"
    rf"={required_column_height_m:.2f}\;\mathrm{{m}}"
)
st.latex(
    rf"H_3=H-h_1-h_2={required_column_height_m:.2f}-1.00-0.60"
    rf"={chimney_height_m:.2f}\;\mathrm{{m}}"
)
height_metrics = st.columns(3)
height_metrics[0].metric("Columna caliente total H", f"{required_column_height_m:.2f} m")
height_metrics[1].metric("Altura de cámara", f"{chamber_height_m:.2f} m")
height_metrics[2].metric("Altura requerida de chimenea", f"{chimney_height_m:.2f} m")

st.subheader("2. Efecto de cambiar la chimenea")
scenarios = st.columns(2)
with scenarios[0]:
    st.markdown("**Chimenea un tercio más alta**")
    st.latex(
        rf"H_3'=\frac{{4}}{{3}}H_3={chimney_height_up_m:.2f}\;\mathrm{{m}}"
    )
    st.latex(
        rf"H'=1.00+0.60+H_3'={column_height_up_m:.2f}\;\mathrm{{m}}"
    )
    st.metric(
        "Velocidad resultante",
        f"{velocity_up_m_s:.4f} m/s",
        f"{(round(velocity_up_m_s, 4) / bed_velocity_m_s - 1) * 100:+.0f}%",
    )
with scenarios[1]:
    st.markdown("**Chimenea un tercio más baja**")
    st.latex(
        rf"H_3'=\frac{{2}}{{3}}H_3={chimney_height_down_m:.2f}\;\mathrm{{m}}"
    )
    st.latex(
        rf"H'=1.00+0.60+H_3'={column_height_down_m:.2f}\;\mathrm{{m}}"
    )
    st.metric(
        "Velocidad resultante",
        f"{velocity_down_m_s:.4f} m/s",
        f"{(round(velocity_down_m_s, 4) / bed_velocity_m_s - 1) * 100:+.0f}%",
    )

st.subheader("3. Menor calentamiento en un día nublado")
st.markdown(
    "Conservando la chimenea dimensionada, si el aire del secador alcanza "
    "30 °C, la diferencia de temperatura baja de 15 °C a 5 °C."
)
st.latex(
    rf"v=3.81\times10^{{-5}}"
    rf"\left(\frac{{5\times{required_column_height_m:.2f}}}{{0.20}}\right)^{{0.87}}"
    rf"={cloudy_velocity_m_s:.4f}\;\mathrm{{m\,s^{{-1}}}}"
)
st.metric("Velocidad a 30 °C", f"{cloudy_velocity_m_s:.4f} m/s")
st.warning(
    "El ejemplo supone que la chimenea no gana ni pierde calor. En un secador "
    "real, una chimenea absorbente puede calentar el aire de salida y aumentar el tiro."
)
st.caption("Fuente: documento proporcionado, apéndice 12, pp. 258–261 (PDF, págs. 4–7).")
