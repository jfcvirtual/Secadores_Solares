import csv
import io
import random
import streamlit as st

from ui import apply_visual_style

st.set_page_config(
    page_title="Actividad | Diseño y protocolo",
    page_icon=":material/science:",
    layout="wide",
)
apply_visual_style()

st.title("Actividad · Diseño experimental y protocolo")
st.caption("Comparación de cuatro secadores y seguimiento durante secado y almacenamiento")
st.warning(
    "El equipo disponible es de fuente eléctrica, no solar. En esta actividad "
    "se comparan secadores térmicos; no se atribuye el calentamiento a energía solar."
)
st.markdown(
    "La propuesta combina el diseño factorial **secador × carga** con el "
    "calendario de mediciones indicado por el profesor Alfredo Fernández. "
    "Los valores de carga de los controles son solo un ejemplo para construir "
    "el plan y deben reemplazarse por niveles acordados para el cultivo y los equipos."
)

st.header("1. Diseño experimental")
st.markdown(
    "**Diseño recomendado: DBCA factorial.** El factor A es tipo de secador "
    "(cuatro niveles) y el factor B es carga (dos niveles: baja y alta). Cada "
    "bloque corresponde a un día de ensayo y contiene las ocho combinaciones "
    "factoriales en orden aleatorio. Así, las diferencias ambientales entre "
    "días no quedan confundidas con los tratamientos."
)

settings = st.columns(3)
with settings[0]:
    low_load = st.number_input(
        "Carga baja de ejemplo (kg/m²)",
        min_value=0.01,
        value=1.0,
        step=0.1,
        help="Reemplace este valor por el nivel bajo definido en el piloto.",
    )
with settings[1]:
    high_load = st.number_input(
        "Carga alta de ejemplo (kg/m²)",
        min_value=0.01,
        value=2.0,
        step=0.1,
        help="Reemplace este valor por el nivel alto definido en el piloto.",
    )
with settings[2]:
    block_count = st.number_input(
        "Bloques (días de ensayo)",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="Tres bloques son una ilustración; acuerde las réplicas con el curso.",
    )

if high_load <= low_load:
    st.error("La carga alta debe ser mayor que la carga baja.")
    treatment_runs = []
else:
    dryer_names = ["Secador A", "Secador B", "Secador C", "Secador D"]
    load_levels = [("Baja", low_load), ("Alta", high_load)]
    treatment_runs = []
    for block in range(1, int(block_count) + 1):
        combinations = [
            (dryer, load_label, load_value)
            for dryer in dryer_names
            for load_label, load_value in load_levels
        ]
        random.Random(2026 + block).shuffle(combinations)
        for order, (dryer, load_label, load_value) in enumerate(combinations, start=1):
            treatment_runs.append(
                {
                    "Bloque / día": block,
                    "Orden aleatorio": order,
                    "Secador": dryer,
                    "Nivel de carga": load_label,
                    "Carga (kg/m²)": load_value,
                }
            )

if treatment_runs:
    metric_columns = st.columns(3)
    metric_columns[0].metric("Tratamientos factoriales", "8")
    metric_columns[1].metric("Corridas independientes", str(len(treatment_runs)))
    metric_columns[2].metric(
        "Corridas por día",
        "8 combinaciones",
    )
    st.dataframe(treatment_runs, width="stretch", hide_index=True)
    randomization_csv = io.StringIO()
    writer = csv.DictWriter(randomization_csv, fieldnames=treatment_runs[0].keys())
    writer.writeheader()
    writer.writerows(treatment_runs)
    st.download_button(
        "Descargar orden aleatorio (CSV)",
        data=randomization_csv.getvalue().encode("utf-8-sig"),
        file_name="aleatorizacion_secadores.csv",
        mime="text/csv",
        icon=":material/download:",
    )

st.markdown(
    "**Unidad experimental:** una corrida independiente de secado con una "
    "asignación secador × carga. Varias mediciones del mismo lote y varias "
    "lecturas del mismo paquete son observaciones repetidas o submuestras, "
    "no réplicas independientes."
)
st.markdown(
    "**Bloques frente a repeticiones:** para que el día sea un bloque completo, "
    "las ocho combinaciones deben ejecutarse cada día; aleatorice su orden "
    "dentro de cada bloque. Si eso no es factible, no llame bloque a un día "
    "incompleto: reorganice las corridas y modele el día como fuente de variación."
)
st.error(
    "Si hay un solo equipo físico de cada tipo, el efecto de tipo de secador "
    "queda confundido con las particularidades de esas cuatro unidades. Se "
    "podrán comparar esos equipos concretos, pero para generalizar a cada "
    "tecnología hacen falta equipos independientes replicados por tipo."
)
st.markdown(
    "Use como carga la masa de producto por área útil de bandeja (kg/m²) si "
    "las superficies difieren, e informe también la masa total. Defina cultivo, "
    "variedad, madurez, espesor de capa, pretratamiento, preparación de muestra "
    "y criterio común de fin de secado antes de aleatorizar."
)

st.header("2. Mediciones durante el secado")
st.markdown(
    "La secuencia indicada se interpreta como lecturas al minuto 0 y luego "
    "cada 1 minuto hasta 10; cada 2 minutos hasta 20; cada 4 minutos hasta "
    "40; y duplicando el intervalo después de cada tramo (8 minutos hasta "
    "80, 16 hasta 160, etc.). Acuerde la duración máxima y un criterio de "
    "parada común antes de iniciar el ensayo."
)

schedule_settings = st.columns(2)
with schedule_settings[0]:
    max_drying_minutes = st.number_input(
        "Duración máxima ilustrativa (min)",
        min_value=40,
        max_value=480,
        value=120,
        step=20,
        help="El calendario se extiende hasta este tiempo; cámbielo según el piloto.",
    )
with schedule_settings[1]:
    st.metric("Inicio de cada corrida", "0 min · lectura basal")

sampling_times = [0]
minute = 1
interval = 1
segment_end = 10
while minute <= int(max_drying_minutes):
    sampling_times.append(minute)
    if minute == segment_end:
        interval *= 2
        segment_end *= 2
    minute += interval

schedule_rows = []
previous_minute = None
for sample_minute in sampling_times:
    schedule_rows.append(
        {
            "Tiempo transcurrido (min)": sample_minute,
            "Intervalo desde lectura anterior": (
                "Basal"
                if previous_minute is None
                else f"{sample_minute - previous_minute} min"
            ),
        }
    )
    previous_minute = sample_minute

with st.expander(f"Ver calendario de lecturas ({len(sampling_times)} tiempos)", expanded=False):
    st.dataframe(schedule_rows, width="stretch", hide_index=True)
    schedule_csv = io.StringIO()
    writer = csv.DictWriter(schedule_csv, fieldnames=schedule_rows[0].keys())
    writer.writeheader()
    writer.writerows(schedule_rows)
    st.download_button(
        "Descargar calendario (CSV)",
        data=schedule_csv.getvalue().encode("utf-8-sig"),
        file_name="calendario_mediciones_secado.csv",
        mime="text/csv",
        icon=":material/download:",
    )

st.subheader("Variables y forma de medición")
measurement_rows = [
    {
        "Variable": "Temperatura del aire en la cámara / hogar",
        "Registro": "En cada tiempo del calendario, en la zona y altura de las muestras; fijar y no mover la sonda.",
        "Unidad / nota": "°C; anotar también consigna del equipo y temperatura ambiente.",
    },
    {
        "Variable": "Pérdida de masa del producto",
        "Registro": "Pesar una bandeja o muestra testigo preidentificada en cada tiempo, sin cambiar su manejo entre secadores.",
        "Unidad / nota": "% respecto a la masa inicial; registrar también masa en g.",
    },
    {
        "Variable": "Contenido de humedad",
        "Registro": "Medir al inicio y al final; añadir puntos intermedios solo si el método y el equipo lo permiten.",
        "Unidad / nota": "% base húmeda (bh), con el mismo método en todos los tratamientos.",
    },
    {
        "Variable": "Tiempo hasta el criterio de fin",
        "Registro": "Registrar el tiempo transcurrido al alcanzar el criterio común predefinido.",
        "Unidad / nota": "min; respuesta de desempeño del proceso.",
    },
]
st.dataframe(measurement_rows, width="stretch", hide_index=True)

with st.expander("Fórmulas y control de la medición"):
    st.latex(
        r"\text{Pérdida de masa (\%)}="
        r"100\,\frac{m_0-m_t}{m_0}"
    )
    st.latex(
        r"X_{bh}(\%)=100\,\frac{m_{h}-m_{s}}{m_{h}}"
    )
    st.markdown(
        "La pérdida de masa no es idéntica al contenido de humedad: también "
        "puede reflejar compuestos volátiles. Para humedad gravimétrica, "
        "m_h es la masa húmeda y m_s la masa seca hasta peso constante. Si el "
        "método es destructivo (por ejemplo, estufa), use submuestras "
        "independientes y no pretenda medirlas cada minuto. Una balanza "
        "integrada o una muestra testigo pesada rápidamente permite seguir "
        "la pérdida de masa con menor perturbación del secador."
    )

st.header("3. Empaque y almacenamiento durante 15 días")
st.markdown(
    "Al terminar cada corrida, homogeneice el producto y prepare paquetes "
    "individuales para cada fecha de análisis. No abra y vuelva a sellar un "
    "mismo paquete en cada visita: eso altera la exposición al aire y la humedad."
)
storage_days = [0, 4, 8, 12, 15]
storage_rows = [
    {
        "Día de almacenamiento": day,
        "Momento": "Antes de almacenar" if day == 0 else ("Final" if day == 15 else "Seguimiento"),
        "Mediciones": "Humedad, textura, sólidos solubles, acidez titulable y pH",
    }
    for day in storage_days
]
st.dataframe(storage_rows, width="stretch", hide_index=True)

packages_required = len(treatment_runs) * len(storage_days) if treatment_runs else 0
package_metrics = st.columns(3)
package_metrics[0].metric("Fechas de almacenamiento", "0, 4, 8, 12 y 15 días")
package_metrics[1].metric("Paquetes por corrida", str(len(storage_days)))
package_metrics[2].metric(
    "Paquetes para el plan actual",
    str(packages_required),
    help="Un paquete independiente por corrida y fecha, sin contar paquetes de reserva.",
)

st.subheader("Indicadores possecado")
st.dataframe(
    [
        {
            "Indicador": "Humedad",
            "Método / unidad que debe fijarse": "% bh; método gravimétrico o medidor validado para el cultivo.",
            "Recurso": "Analizador de humedad o estufa y balanza.",
        },
        {
            "Indicador": "Textura",
            "Método / unidad que debe fijarse": "Definir prueba de compresión o penetración, geometría, velocidad y unidad.",
            "Recurso": "Texturómetro; si no está disponible, dejar como variable pendiente.",
        },
        {
            "Indicador": "Sólidos solubles",
            "Método / unidad que debe fijarse": "°Brix; estandarizar extracción y temperatura de lectura.",
            "Recurso": "Refractómetro.",
        },
        {
            "Indicador": "Acidez titulable",
            "Método / unidad que debe fijarse": "Definir titulante, punto final y ácido de referencia; reportar como % equivalente.",
            "Recurso": "Bureta, reactivos y protocolo del laboratorio.",
        },
        {
            "Indicador": "pH",
            "Método / unidad que debe fijarse": "Unidades de pH; indicar preparación de muestra y calibrar el equipo.",
            "Recurso": "Potenciómetro y soluciones tampón.",
        },
    ],
    width="stretch",
    hide_index=True,
)
st.info(
    "Antes de empacar, registre humedad final, masa por paquete, material y "
    "tipo de cierre. Mantenga iguales entre tratamientos el empaque y las "
    "condiciones de almacenamiento; registre temperatura y humedad relativa "
    "del lugar durante los 15 días."
)
st.warning(
    "Si no prestan equipos o reactivos, no reporte textura, °Brix, acidez o "
    "pH como medidos. Priorice humedad y masa, y marque los otros indicadores "
    "como pendientes de disponibilidad y protocolo."
)

st.header("4. Análisis e interpretación")
st.markdown(
    "Para las respuestas durante el secado, analice secador, carga, tiempo y "
    "sus interacciones; incluya bloque/día y corrida como fuentes de variación. "
    "Las lecturas del mismo lote están correlacionadas: tiempo es una medida "
    "repetida, no un nuevo replicado. Para almacenamiento, analice secador × "
    "carga × día de almacenamiento; mantenga la corrida como unidad de "
    "agrupación. Si cada fecha usa un paquete distinto por análisis destructivo, "
    "los paquetes quedan anidados en la corrida y fecha."
)
st.latex(
    r"Y=\mu+S+C+S\!\times\!C+T"
    r"+S\!\times\!T+C\!\times\!T"
    r"+S\!\times\!C\!\times\!T"
    r"+B+U_{\mathrm{corrida}}+\varepsilon"
)
st.caption(
    "S: secador; C: carga; T: tiempo; B: bloque (día); U_corrida: "
    "variación entre corridas independientes. La selección del modelo final "
    "y la cantidad de réplicas deben acordarse según los objetivos y la "
    "variabilidad observada en un ensayo piloto."
)

st.header("5. Lista de preparación")
st.markdown(
    "- Confirmar cultivo, variedad, cantidad, niveles de carga y área útil de bandeja.\n"
    "- Verificar sensores, balanza, métodos, calibración y disponibilidad de laboratorio.\n"
    "- Definir criterio común de fin de secado, tipo de empaque y condiciones de almacenamiento.\n"
    "- Etiquetar cada corrida y sus cinco paquetes de almacenamiento antes de iniciar.\n"
    "- Aleatorizar las ocho combinaciones dentro de cada día y registrar cualquier desviación."
)
st.caption(
    "Plan académico sujeto a validación del profesor y a los procedimientos de "
    "seguridad, inocuidad y operación de los equipos del laboratorio."
)
