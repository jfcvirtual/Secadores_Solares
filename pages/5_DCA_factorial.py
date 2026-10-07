import csv
import io
import random
import streamlit as st

from ui import apply_visual_style

st.set_page_config(
    page_title="Actividad | DCA factorial",
    page_icon=":material/science:",
    layout="wide",
)
apply_visual_style()

st.title("Actividad · Diseño completamente al azar")
st.caption("Alternativa sencilla: factorial de cuatro secadores × dos cargas")
st.warning(
    "Los equipos disponibles son eléctricos. Se comparan secadores térmicos, "
    "no se evalúa el uso de energía solar."
)

st.markdown(
    "En esta alternativa, los tratamientos se asignan completamente al azar "
    "a las corridas experimentales. Se conservan los factores de la propuesta "
    "DBCA: tipo de secador y nivel de carga; aquí no se forman bloques por día."
)

st.header("1. Tratamientos y réplicas")
st.markdown(
    "- **Factor A, secador:** cuatro equipos (A, B, C y D).\n"
    "- **Factor B, carga:** dos niveles, baja y alta.\n"
    "- **Tratamientos:** las ocho combinaciones secador × carga.\n"
    "- **Unidad experimental:** una corrida independiente con un lote asignado a un tratamiento."
)

settings = st.columns(3)
with settings[0]:
    low_load = st.number_input(
        "Carga baja de ejemplo (kg/m²)",
        min_value=0.01,
        value=1.0,
        step=0.1,
        help="Cambie el valor por la carga baja definida para el cultivo y los secadores.",
    )
with settings[1]:
    high_load = st.number_input(
        "Carga alta de ejemplo (kg/m²)",
        min_value=0.01,
        value=2.0,
        step=0.1,
        help="Cambie el valor por la carga alta definida para el cultivo y los secadores.",
    )
with settings[2]:
    replicate_count = st.number_input(
        "Réplicas independientes por tratamiento",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="El valor inicial es ilustrativo; defina réplicas con base en los objetivos y un piloto.",
    )

if high_load <= low_load:
    st.error("La carga alta debe ser mayor que la carga baja.")
    randomized_runs = []
else:
    dryer_names = ["Secador A", "Secador B", "Secador C", "Secador D"]
    load_levels = [("Baja", low_load), ("Alta", high_load)]
    randomized_runs = [
        {
            "Secador": dryer,
            "Nivel de carga": load_label,
            "Carga (kg/m²)": load_value,
            "Réplica": replicate,
        }
        for dryer in dryer_names
        for load_label, load_value in load_levels
        for replicate in range(1, int(replicate_count) + 1)
    ]
    random.Random(2026).shuffle(randomized_runs)
    for order, run in enumerate(randomized_runs, start=1):
        run["Orden aleatorio"] = order
    randomized_runs = [
        {
            "Orden aleatorio": run["Orden aleatorio"],
            "Secador": run["Secador"],
            "Nivel de carga": run["Nivel de carga"],
            "Carga (kg/m²)": run["Carga (kg/m²)"],
            "Réplica": run["Réplica"],
        }
        for run in randomized_runs
    ]

if randomized_runs:
    run_count = len(randomized_runs)
    package_count = run_count * 5
    metrics = st.columns(3)
    metrics[0].metric("Combinaciones factoriales", "8")
    metrics[1].metric("Corridas independientes", str(run_count))
    metrics[2].metric("Paquetes para almacenamiento", str(package_count))
    st.dataframe(randomized_runs, width="stretch", hide_index=True)

    randomization_csv = io.StringIO()
    writer = csv.DictWriter(randomization_csv, fieldnames=randomized_runs[0].keys())
    writer.writeheader()
    writer.writerows(randomized_runs)
    st.download_button(
        "Descargar orden aleatorio (CSV)",
        data=randomization_csv.getvalue().encode("utf-8-sig"),
        file_name="aleatorizacion_DCA_secadores.csv",
        mime="text/csv",
        icon=":material/download:",
    )

st.header("2. Cuándo usar este DCA")
st.markdown(
    "Use el DCA si las corridas pueden hacerse bajo condiciones ambientales "
    "y operativas suficientemente homogéneas, sin un efecto sistemático del "
    "día, y si es viable aleatorizar el orden de todas las corridas. Mantenga "
    "estables la preparación del producto, las condiciones de operación, el "
    "criterio de fin de secado y el almacenamiento."
)
st.info(
    "Si los ensayos ocurren en días distintos y la temperatura ambiente u otras "
    "condiciones pueden afectar el proceso, la variación del día puede confundirse "
    "con los tratamientos. En ese caso use la propuesta DBCA de la página 4, "
    "con las ocho combinaciones en cada bloque/día."
)
st.warning(
    "Si existe un solo equipo físico de cada tipo, las réplicas de lotes permiten "
    "comparar esas cuatro unidades concretas, pero no separan el efecto de la "
    "tecnología de las particularidades de cada máquina."
)
st.markdown(
    "Las cargas iniciales de 1 y 2 kg/m² son ejemplos editables, no valores "
    "recomendados. Si las áreas de bandeja son distintas, defina la carga por "
    "área útil y registre también la masa total. No cuente varias mediciones "
    "del mismo lote como réplicas independientes."
)

st.header("3. Protocolo resumido")
st.markdown(
    "**Durante el secado:** registrar temperatura del aire en la cámara/hogar, "
    "en la zona y altura de las muestras; mantener fija la ubicación de la sonda. "
    "Medir masa o pérdida de masa con la misma frecuencia y procedimiento para "
    "todos los tratamientos, y humedad al inicio y al final con un método "
    "consistente. Registrar el tiempo hasta un criterio común de fin."
)
st.markdown(
    "Calendario interpretado de la nota: lectura basal en el minuto 0; cada "
    "minuto hasta 10; cada 2 minutos hasta 20; cada 4 minutos hasta 40; después "
    "duplicar el intervalo (8 minutos hasta 80, 16 hasta 160, etc.). Acordar "
    "antes del ensayo la duración máxima y la regla de parada."
)
st.markdown(
    "**Durante el almacenamiento:** preparar cinco paquetes separados por "
    "corrida, uno para cada fecha: días 0, 4, 8, 12 y 15. Mantener el mismo "
    "material de empaque y cierre, no reabrir los paquetes antes del análisis y "
    "registrar temperatura y humedad relativa del lugar. Para tres réplicas por "
    "tratamiento, el ejemplo requiere 24 corridas y 120 paquetes, antes de "
    "considerar reservas."
)

st.dataframe(
    [
        {
            "Indicador possecado": "Humedad",
            "Registro": "% base húmeda; mismo método en todas las muestras.",
            "Disponibilidad": "Prioritario; estufa/balanza o medidor validado.",
        },
        {
            "Indicador possecado": "Textura",
            "Registro": "Definir prueba y unidad antes del ensayo.",
            "Disponibilidad": "Texturómetro; si no hay equipo, dejar pendiente.",
        },
        {
            "Indicador possecado": "Sólidos solubles",
            "Registro": "°Brix, con extracción estandarizada.",
            "Disponibilidad": "Refractómetro; sujeto al préstamo del laboratorio.",
        },
        {
            "Indicador possecado": "Acidez titulable",
            "Registro": "Definir titulante, punto final y ácido de referencia.",
            "Disponibilidad": "Reactivos y protocolo; sujeto a disponibilidad.",
        },
        {
            "Indicador possecado": "pH",
            "Registro": "Calibrar el potenciómetro e indicar preparación de muestra.",
            "Disponibilidad": "Equipo y tampones; sujeto a disponibilidad.",
        },
    ],
    width="stretch",
    hide_index=True,
)
st.warning(
    "No reportar textura, °Brix, acidez ni pH como medidos si no se cuenta con "
    "el equipo, reactivos y método. Las determinaciones destructivas requieren "
    "muestras o paquetes independientes por fecha."
)
st.caption(
    "La página 4 contiene la propuesta alternativa con DBCA y el protocolo "
    "detallado. Antes de ejecutar el DCA, validar el número de réplicas, la "
    "homogeneidad de las condiciones y la disponibilidad de muestras con el "
    "profesor y el laboratorio."
)
