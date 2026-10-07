import streamlit as st

from ui import apply_visual_style

st.set_page_config(
    page_title="Apéndice 13 | Lecho y ventilador",
    page_icon=":material/air:",
    layout="wide",
)
apply_visual_style()

crop_mass_kg = 3000.0
bulk_density_kg_m3 = 780.0
chamber_width_m = 2.0
chamber_length_m = 2.0
maximum_bed_depth_m = 1.5
pressure_resistance_pa_m = 325.0
flow_coefficient = 0.0003
fan_efficiency = 0.60

bed_volume_m3 = crop_mass_kg / bulk_density_kg_m3
bed_area_m2 = chamber_width_m * chamber_length_m
bed_depth_m = round(bed_volume_m3 / bed_area_m2, 2)
pressure_drop_pa = pressure_resistance_pa_m * bed_depth_m
superficial_velocity_unrounded_m_s = flow_coefficient * (
    pressure_drop_pa / bed_depth_m
)
superficial_velocity_m_s = round(superficial_velocity_unrounded_m_s, 1)
volumetric_flow_m3_s = superficial_velocity_m_s * bed_area_m2
air_power_w = volumetric_flow_m3_s * pressure_drop_pa
motor_power_w = round(air_power_w) / fan_efficiency
nominal_motor_power_w = round(motor_power_w, -1)

st.title("Apéndice 13 · Flujo a través del lecho")
st.caption("Secador de convección forzada · estimación del caudal y potencia")
st.markdown(
    "Se secan 3 toneladas de cereal con densidad aparente de 780 kg/m³ en "
    "una cámara de 2 × 2 m de sección y 1,5 m de profundidad máxima. La "
    "resistencia al flujo del grano es 325 Pa por metro de lecho."
)
st.info(
    "Primero se calcula la profundidad realmente ocupada por el grano. "
    "El valor de 1,5 m es la profundidad máxima de la cámara, no la altura "
    "del lecho usada en la correlación."
)

st.subheader("1. Volumen y profundidad del producto")
st.latex(
    rf"V_b=\frac{{m}}{{\rho_b}}"
    rf"=\frac{{3000}}{{780}}={bed_volume_m3:.2f}\;\mathrm{{m^3}}"
)
st.latex(
    rf"A_b=2\times2={bed_area_m2:.2f}\;\mathrm{{m^2}},"
    rf"\qquad h_b=\frac{{V_b}}{{A_b}}"
    rf"=\frac{{{bed_volume_m3:.2f}}}{{4}}={bed_depth_m:.2f}\;\mathrm{{m}}"
)
st.metric("Profundidad ocupada del lecho", f"{bed_depth_m:.2f} m")

st.subheader("2. Caudal de aire")
st.markdown(
    "La correlación empírica del apéndice usa a = 0,0003 y b = 1 para este "
    "cultivo. La velocidad v es el caudal por unidad de sección transversal."
)
st.latex(
    r"v=a\left(\frac{\Delta P}{h_b}\right)^b"
    r"=0.0003\left(\frac{\Delta P}{h_b}\right)"
    r"\qquad\text{(ecuación A13.1)}"
)
st.latex(
    rf"\Delta P=325\;\frac{{\mathrm{{Pa}}}}{{\mathrm{{m}}}}"
    rf"\times{bed_depth_m:.2f}\;\mathrm{{m}}"
    rf"={pressure_drop_pa:.0f}\;\mathrm{{Pa}}"
)
st.latex(
    rf"v=0.0003\left(\frac{{{pressure_drop_pa:.0f}}}"
    rf"{{{bed_depth_m:.2f}}}\right)"
    rf"={superficial_velocity_unrounded_m_s:.4f}"
    rf"\approx{superficial_velocity_m_s:.1f}"
    rf"\;\mathrm{{m\,s^{{-1}}}}"
)
st.latex(
    rf"\dot V=vA_b={superficial_velocity_m_s:.2f}"
    rf"\times{bed_area_m2:.0f}={volumetric_flow_m3_s:.2f}"
    rf"\;\mathrm{{m^3\,s^{{-1}}}}"
)
flow_metrics = st.columns(3)
flow_metrics[0].metric("Caída de presión", f"{pressure_drop_pa:.0f} Pa")
flow_metrics[1].metric("Velocidad superficial", f"{superficial_velocity_m_s:.2f} m/s")
flow_metrics[2].metric("Caudal volumétrico", f"{volumetric_flow_m3_s:.2f} m³/s")

st.subheader("3. Potencia del ventilador")
st.markdown(
    "La potencia estática transferida al aire es el producto del caudal "
    "volumétrico y la caída de presión. Para estimar la potencia del motor, "
    "se divide por la eficiencia mecánica del ventilador."
)
st.latex(
    rf"P_{{aire}}=\dot V\,\Delta P"
    rf"={volumetric_flow_m3_s:.2f}\times{pressure_drop_pa:.0f}"
    rf"={air_power_w:.1f}\approx{round(air_power_w):.0f}"
    rf"\;\mathrm{{W}}"
    rf"\qquad\text{{(ecuación A13.2)}}"
)
st.latex(
    rf"P_{{motor}}=\frac{{P_{{aire}}}}{{\eta_f}}"
    rf"=\frac{{{round(air_power_w):.0f}}}{{0.60}}"
    rf"={motor_power_w:.1f}\approx{nominal_motor_power_w:.0f}"
    rf"\;\mathrm{{W}}"
)
power_metrics = st.columns(2)
power_metrics[0].metric("Potencia estática del aire", f"{air_power_w:.0f} W")
power_metrics[1].metric(
    "Potencia de motor estimada",
    f"≈ {nominal_motor_power_w:.0f} W",
)
st.caption(
    f"La profundidad de cámara disponible es {maximum_bed_depth_m:.1f} m; "
    "el lecho calculado (0,96 m) cabe dentro de ella. Se siguen los "
    "redondeos del ejemplo (v ≈ 0,1 m/s); no se incluyen pérdidas adicionales "
    "en conductos."
)
st.caption("Fuente: documento proporcionado, apéndice 13, pp. 262–263 (PDF, págs. 8–9).")
