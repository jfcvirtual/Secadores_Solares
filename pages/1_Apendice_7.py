import streamlit as st

from ui import apply_visual_style

st.set_page_config(
    page_title="Apéndice 7 | Desempeño",
    page_icon=":material/monitoring:",
    layout="wide",
)
apply_visual_style()

fresh_mass_kg = 100.0
initial_moisture_fraction = 0.80
final_moisture_fraction = 0.05
latent_heat_kj_kg = 2320.0
irradiance_kj_m2_day = 20_000.0
collector_area_m2 = 15.0
drying_days = 3.0
airflow_m3_s = 0.5
air_density_kg_m3 = 1.28
inlet_humidity_kg_kg = 0.014
adiabatic_saturation_humidity_kg_kg = 0.0186

initial_water_kg = fresh_mass_kg * initial_moisture_fraction
dry_solids_kg = fresh_mass_kg - initial_water_kg
final_water_kg = (
    dry_solids_kg
    * final_moisture_fraction
    / (1 - final_moisture_fraction)
)
water_evaporated_kg = initial_water_kg - final_water_kg
solar_energy_kj = irradiance_kj_m2_day * collector_area_m2 * drying_days
drying_efficiency = (
    water_evaporated_kg * latent_heat_kj_kg / solar_energy_kj
)
time_reported_s = 129_600.0
time_elapsed_s = drying_days * 24 * 60 * 60
pickup_capacity_reported_kg = (
    airflow_m3_s
    * air_density_kg_m3
    * time_reported_s
    * (adiabatic_saturation_humidity_kg_kg - inlet_humidity_kg_kg)
)
pickup_capacity_elapsed_kg = (
    airflow_m3_s
    * air_density_kg_m3
    * time_elapsed_s
    * (adiabatic_saturation_humidity_kg_kg - inlet_humidity_kg_kg)
)
pickup_efficiency_reported = water_evaporated_kg / pickup_capacity_reported_kg
pickup_efficiency_elapsed = water_evaporated_kg / pickup_capacity_elapsed_kg

st.title("Apéndice 7 · Evaluación del desempeño")
st.caption("Secado de pimientos · base húmeda (bh)")
st.markdown(
    "Se evalúa un lote de 100 kg de pimientos que pasa de 80 % a 5 % de "
    "humedad en tres días. El colector tiene 15 m² y recibe una insolación "
    "media diaria de 20 MJ/m². El ventilador entrega 0,5 m³/s."
)

with st.expander("Datos psicrométricos y de operación", expanded=True):
    st.markdown(
        "La densidad del aire es 1,28 kg/m³. A 25 °C y 70 % de humedad "
        "relativa, la humedad absoluta de entrada es 0,014 kg/kg de aire seco. "
        "El valor de saturación adiabática usado por el texto es 0,0186 kg/kg, "
        "obtenido allí de la carta psicrométrica."
    )

st.subheader("1. Agua evaporada del producto")
st.latex(
    r"m_s=m_0(1-X_i)=100(1-0.80)=20\;\mathrm{kg}"
)
st.latex(
    r"m_{w,f}=m_s\frac{X_f}{1-X_f}"
    r"=20\frac{0.05}{0.95}=1.05\;\mathrm{kg}"
)
st.latex(
    r"m_{ev}=m_{w,i}-m_{w,f}=80-1.05=78.95\;\mathrm{kg}"
)

mass_metrics = st.columns(3)
mass_metrics[0].metric("Sólidos secos", f"{dry_solids_kg:.2f} kg")
mass_metrics[1].metric("Agua final", f"{final_water_kg:.2f} kg")
mass_metrics[2].metric("Agua evaporada", f"{water_evaporated_kg:.2f} kg")

st.subheader("2. Eficiencia global de secado")
st.markdown(
    "Compara el calor latente asociado al agua evaporada con la energía "
    "solar incidente en el área del colector durante todo el secado."
)
st.latex(
    r"\eta_d=\frac{m_{ev}L_v}{I_d A_c N_d}"
    r"=\frac{78.95\times2320}{20\,000\times15\times3}"
    r"=0.204\approx20.4\%"
)
st.caption(
    "L_v = 2320 kJ/kg; I_d = 20 000 kJ/(m²·día); "
    "A_c = 15 m²; N_d = 3 días."
)
st.metric("Eficiencia global de secado", f"{drying_efficiency:.1%}")

st.subheader("3. Eficiencia de captación de humedad")
st.markdown(
    "Representa la fracción de la capacidad potencial de transporte de "
    "humedad del aire que se utilizó para evaporar agua del lote."
)
st.latex(
    r"\eta_p=\frac{m_{ev}}{\dot V\,\rho\,t\,(w_{as}-w_i)}"
)
st.latex(
    r"\eta_p=\frac{78.95}"
    r"{0.5\times1.28\times129\,600\times(0.0186-0.014)}"
    r"=0.207\approx20.7\%"
)
st.latex(
    rf"\eta_p(3\;\mathrm{{d}})=\frac{{78.95}}"
    rf"{{0.5\times1.28\times259\,200\times(0.0186-0.014)}}"
    rf"={pickup_efficiency_elapsed:.3f}"
    rf"\approx{pickup_efficiency_elapsed:.1%}"
)
st.caption(
    "La diferencia de humedades absolutas se usa tal como aparece en el "
    "apéndice; no se vuelve a estimar a partir de la humedad relativa."
)
st.warning(
    "El apéndice indica 3 días, pero sustituye t = 129 600 s (36 h). "
    "Por eso se muestran el 20,7 % publicado con ese tiempo y el 10,3 % "
    "que corresponde a 3 días completos (259 200 s)."
)
pickup_metrics = st.columns(2)
pickup_metrics[0].metric(
    "Resultado del apéndice (129 600 s)",
    f"{pickup_efficiency_reported:.1%}",
)
pickup_metrics[1].metric(
    "Recálculo para 3 días",
    f"{pickup_efficiency_elapsed:.1%}",
)
st.caption("Fuente: documento proporcionado, apéndice 7, pp. 235–236 (PDF, págs. 2–3).")
