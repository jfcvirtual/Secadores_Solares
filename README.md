# Evaluación de secadores y diseño experimental

Aplicación multipágina de Streamlit para estudiar el desempeño de secadores y planificar una comparación experimental de cuatro equipos. Incluye en español los apéndices resueltos 7, 12 y 13 de [`docs/Solar_Dryers-APENDICES.pdf`](docs/Solar_Dryers-APENDICES.pdf), además de una propuesta de diseño y protocolo de medición.

> **Alcance del experimento propuesto:** los equipos disponibles son de fuente eléctrica. La actividad los trata como secadores térmicos; no atribuye su calentamiento a energía solar.

## Instalación y ejecución

Desde la raíz del repositorio, crea y activa el entorno, instala las dependencias y arranca la aplicación:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit mostrará la dirección local en la terminal, normalmente <http://localhost:8501>. Para detener el servidor, usa `Ctrl+C` en la terminal donde está ejecutándose.

## Contenido de la aplicación

- **Apéndice 7:** eficiencia global de secado y eficiencia de captación de humedad.
- **Apéndice 12:** estimación del flujo por convección natural y dimensionamiento de una chimenea.
- **Apéndice 13:** flujo a través de un lecho de grano y potencia estimada del ventilador.
- **Actividad experimental (página 4):** propuesta DBCA factorial, aleatorización por bloque/día, calendario de muestreo y plan de calidad durante 15 días de almacenamiento.
- **Actividad experimental DCA (página 5):** alternativa sencilla con los mismos tratamientos factoriales y réplicas completamente aleatorizadas.

## Ecuaciones de los apéndices

### Apéndice 7: desempeño del secador

El ejemplo seca 100 kg de pimientos desde 80 % hasta 5 % de humedad en base húmeda. La humedad se introduce en las fórmulas como fracción: $X_i=0.80$ y $X_f=0.05$.

La masa de sólidos secos, el agua restante en el producto final y el agua evaporada son:

$$
m_s=m_0(1-X_i)=100(1-0.80)=20\;\mathrm{kg}
$$

$$
m_{w,f}=m_s\frac{X_f}{1-X_f}
=20\frac{0.05}{0.95}=1.05\;\mathrm{kg}
$$

$$
m_{ev}=m_{w,i}-m_{w,f}=80-1.05=78.95\;\mathrm{kg}
$$

La eficiencia global compara el calor latente asociado al agua evaporada con la energía solar incidente sobre el colector:

$$
\eta_d=\frac{m_{ev}L_v}{I_d A_c N_d}
=\frac{78.95\times2320}{20\,000\times15\times3}
\approx0.204=20.4\%
$$

Donde $L_v=2320\;\mathrm{kJ\,kg^{-1}}$ es el calor latente, $I_d=20\,000\;\mathrm{kJ\,m^{-2}\,día^{-1}}$ la insolación diaria, $A_c=15\;\mathrm{m^2}$ el área del colector y $N_d=3$ días.

La eficiencia de captación de humedad compara el agua evaporada con la capacidad de transporte de humedad del aire:

$$
\eta_p=\frac{m_{ev}}{\dot V\,\rho\,t\,(w_{as}-w_i)}
$$

El ejemplo usa $\dot V=0.5\;\mathrm{m^3\,s^{-1}}$, $\rho=1.28\;\mathrm{kg\,m^{-3}}$, $w_i=0.014$ y $w_{as}=0.0186\;\mathrm{kg\,kg^{-1}}$ de aire seco. El último valor procede de la carta psicrométrica citada en el apéndice.

**Discrepancia de tiempo en la fuente:** aunque el texto dice tres días, sustituye $t=129\,600\;\mathrm{s}$, que equivale a 36 horas. Con ese tiempo se obtiene el resultado publicado, $\eta_p\approx20.7\%$. Tres días completos son $259\,200\;\mathrm{s}$ y, con los mismos datos, dan $\eta_p\approx10.3\%$. La aplicación muestra ambos valores para hacer visible la diferencia.

### Apéndice 12: convección natural

El ejemplo estima el tiro producido al calentar aire de 25 °C a 40 °C y hacerlo pasar por un lecho de arroz de 0.20 m. La densidad del aire se aproxima por:

$$
\rho=1.11363-0.00308T\qquad[\mathrm{kg\,m^{-3}}]
$$

La diferencia de presión entre el aire caliente y el ambiente es:

$$
\Delta P=(\rho_1-\rho_2)gH
\approx0.00308\,\Delta T\,gH
$$

La relación empírica de flujo a través del grano es:

$$
v=a\left(\frac{\Delta P}{h_b}\right)^b,
\qquad a=0.0008,\quad b=0.87
$$

Combinando las relaciones anteriores, con $g=9.81\;\mathrm{m\,s^{-2}}$:

$$
v=3.81\times10^{-5}\left(\frac{\Delta T\,H}{h_b}\right)^{0.87}
\qquad\text{(ecuación A12.4)}
$$

Aquí $v$ es la velocidad superficial a través del lecho (caudal por área), $h_b$ el espesor del lecho y $H$ la altura **total** de la columna caliente. Se despeja:

$$
H=\frac{h_b}{\Delta T}
\left(\frac{v}{3.81\times10^{-5}}\right)^{1/0.87}
$$

Con $v=0.0055\;\mathrm{m\,s^{-1}}$, $h_b=0.20\;\mathrm{m}$ y $\Delta T=15\;^\circ\mathrm{C}$, se obtiene $H=4.05\;\mathrm{m}$. Descontando 0.60 m de cámara y 1.00 m entre el suelo y la cámara, la chimenea requerida mide **2.45 m**.

- Si la chimenea aumenta un tercio: $H_3=3.27\;\mathrm{m}$, $H=4.87\;\mathrm{m}$ y $v\approx0.0065\;\mathrm{m\,s^{-1}}$ (aproximadamente 18 % más).
- Si disminuye un tercio: $H_3=1.63\;\mathrm{m}$, $H=3.23\;\mathrm{m}$ y $v\approx0.0045\;\mathrm{m\,s^{-1}}$ (aproximadamente 18 % menos).
- Si el aire llega solo a 30 °C, $\Delta T=5\;^\circ\mathrm{C}$ y $v\approx0.0021\;\mathrm{m\,s^{-1}}$ con la altura calculada.

El modelo supone temperatura y densidad uniformes, ausencia de fugas, secado por convección y resistencia al flujo dominada por el lecho. También supone que la chimenea no gana ni pierde calor.

### Apéndice 13: ventilación forzada

Para 3000 kg de grano a una densidad aparente de $780\;\mathrm{kg\,m^{-3}}$:

$$
V_b=\frac{3000}{780}=3.85\;\mathrm{m^3},\qquad
A_b=2\times2=4\;\mathrm{m^2},\qquad
h_b=\frac{3.85}{4}=0.96\;\mathrm{m}
$$

La resistencia indicada es $325\;\mathrm{Pa}$ por metro de profundidad, por lo que:

$$
\Delta P=325\times0.96=312\;\mathrm{Pa}
$$

Con $a=0.0003$ y $b=1$, la ecuación A13.1 es:

$$
v=a\left(\frac{\Delta P}{h_b}\right)^b
=0.0003\left(\frac{312}{0.96}\right)
=0.0975\approx0.1\;\mathrm{m\,s^{-1}}
$$

El caudal volumétrico y la potencia estática del aire son:

$$
\dot V=vA_b=0.1\times4=0.4\;\mathrm{m^3\,s^{-1}}
\qquad\text{(se usa la velocidad redondeada del ejemplo)}
$$

$$
P_{aire}=\dot V\,\Delta P=0.4\times312=124.8\approx125\;\mathrm{W}
\qquad\text{(ecuación A13.2)}
$$

Para una eficiencia mecánica del ventilador $\eta_f=0.60$:

$$
P_{motor}=\frac{P_{aire}}{\eta_f}
=\frac{125}{0.60}=208.3\approx210\;\mathrm{W}
$$

El cálculo no incluye pérdidas adicionales en conductos o accesorios.

## Actividad: diseño y protocolo experimental

### Objetivo y factores

Comparar cuatro secadores eléctricos y dos niveles de carga, y evaluar tanto la cinética de secado como algunos indicadores de calidad durante el almacenamiento.

- **Factor A, secador:** cuatro niveles, identificados provisionalmente como A, B, C y D. Registrar tipo, marca, capacidad y condiciones de operación de cada equipo.
- **Factor B, carga:** dos niveles, bajo y alto. Si las áreas útiles de bandeja difieren, definir la carga como masa de producto por área ($\mathrm{kg\,m^{-2}}$) y registrar también la masa total.
- **Bloque:** día de ensayo, para controlar variaciones ambientales entre días.
- **Unidad experimental:** una corrida de secado independiente con una combinación asignada de secador y carga.

### Diseño recomendado

Se recomienda un **DBCA factorial**: cada bloque/día contiene las cuatro combinaciones de secador por las dos cargas (ocho tratamientos), ejecutadas en orden aleatorio. Con $B$ días completos:

$$
N_{corridas}=4\times2\times B=8B
$$

La configuración ilustrativa de la aplicación usa tres bloques, por lo que produce 24 corridas (ocho por día). Los niveles de carga que aparecen inicialmente en los controles, 1 y 2 $\mathrm{kg\,m^{-2}}$, son ejemplos editables, no recomendaciones para un cultivo particular. La aplicación genera una secuencia aleatoria reproducible y permite descargarla como CSV.

La aplicación incluye ambas opciones: la **página 4** desarrolla el DBCA y la **página 5** el DCA factorial. En un DCA, cada una de las ocho combinaciones se repite $r$ veces y las $8r$ corridas se asignan en orden aleatorio:

$$
N_{corridas,DCA}=4\times2\times r=8r
$$

El DCA es apropiado si las condiciones de ensayo son suficientemente homogéneas y no se espera que el día afecte sistemáticamente las respuestas. Si los ensayos ocurren en días distintos y la temperatura ambiente u otras condiciones pueden afectar el proceso, es preferible bloquear por día con el DBCA. Si se elige DBCA, cada bloque debe incluir las ocho combinaciones; no se debe tratar un día incompleto como bloque completo sin ajustar el diseño y el análisis.

**Precaución sobre los equipos:** si solo existe una unidad física de cada tipo, el tipo queda confundido con las características de esa unidad. Varias bandejas o mediciones de la misma corrida no replican el tipo de equipo. Las conclusiones podrán comparar esos cuatro equipos concretos, pero no generalizar a toda una tecnología sin secadores independientes replicados por tipo.

Antes del ensayo, definir cultivo y variedad, madurez, acondicionamiento, espesor de capa, niveles de carga, criterio común de fin de secado, método de humedad y condiciones de almacenamiento. Hacer un piloto para verificar que las corridas caben en el calendario y para estimar la variabilidad y las réplicas necesarias.

### Mediciones durante el secado

La nota del profesor se interpreta como el siguiente calendario, con una lectura basal en $t=0$:

| Tramo | Frecuencia | Tiempos de ejemplo (min) |
| --- | --- | --- |
| Inicio | Basal | 0 |
| Hasta 10 min | Cada 1 min | 1, 2, ..., 10 |
| Hasta 20 min | Cada 2 min | 12, 14, 16, 18, 20 |
| Hasta 40 min | Cada 4 min | 24, 28, 32, 36, 40 |
| Hasta 80 min | Cada 8 min | 48, 56, ..., 80 |
| Después | Duplicar el intervalo en cada tramo | Cada 16 min hasta 160, luego cada 32 min, etc. |

La página genera el calendario hasta una duración máxima editable y permite descargarlo como CSV. La duración máxima y el criterio de parada se deben fijar antes de empezar y aplicarse de igual manera a todos los tratamientos.

| Variable | Procedimiento recomendado | Registro |
| --- | --- | --- |
| Temperatura en el hogar/cámara | Medir el aire en la zona y altura de las muestras; fijar la sonda y no moverla. Usar registrador automático si está disponible. | °C; registrar además temperatura ambiente y consigna del equipo. |
| Pérdida de masa | Pesar una bandeja o muestra testigo identificada en cada tiempo con el mismo procedimiento para todos los secadores. | Masa en g y pérdida porcentual respecto a la masa inicial. |
| Contenido de humedad | Medir al inicio y al final; añadir puntos intermedios solo si el método está disponible y validado. | Porcentaje en base húmeda (bh), usando el mismo método en todos los tratamientos. |
| Tiempo de secado | Registrar el tiempo en que se alcanza el criterio común de finalización. | Minutos. |

La pérdida de masa se calcula como:

$$
	ext{Pérdida de masa (\%)}=100\,\frac{m_0-m_t}{m_0}
$$

El contenido de humedad en base húmeda es:

$$
X_{bh}(\%)=100\,\frac{m_h-m_s}{m_h}
$$

Donde $m_0$ es la masa inicial, $m_t$ la masa en el tiempo $t$, $m_h$ la masa húmeda de la muestra y $m_s$ su masa seca hasta peso constante. La pérdida de masa no equivale necesariamente a agua perdida, pues puede incluir otros compuestos volátiles. Una determinación gravimétrica en estufa es destructiva: usar submuestras independientes y no plantear una determinación de estufa cada minuto. Para una serie de alta frecuencia, preferir una balanza integrada o un método rápido no destructivo validado.

### Empaque, almacenamiento e indicadores

Después del secado, homogeneizar cada corrida y preparar **un paquete separado para cada fecha**. Las fechas propuestas para cubrir los 15 días y conservar la periodicidad de cuatro días son 0 (antes de almacenar), 4, 8, 12 y 15. No abrir y volver a sellar el mismo paquete para los análisis: cada paquete debe permanecer cerrado hasta su fecha de muestreo.

Con 24 corridas y cinco fechas se requieren inicialmente $24\times5=120$ paquetes, más unidades de reserva. Registrar masa por paquete, material y tipo de cierre. Mantener iguales el empaque y las condiciones de almacenamiento entre tratamientos; monitorear y anotar temperatura y humedad relativa durante los 15 días.

| Indicador | Unidad/protocolo que debe acordarse | Recurso posible |
| --- | --- | --- |
| Humedad | % bh; método gravimétrico o medidor validado para el cultivo. | Analizador de humedad o estufa y balanza. |
| Textura | Definir prueba de compresión o penetración, preparación, geometría, velocidad y unidad. | Texturómetro. |
| Sólidos solubles | °Brix; estandarizar extracción y temperatura de lectura. | Refractómetro. |
| Acidez titulable | Definir titulante, punto final y ácido de referencia; expresar como porcentaje equivalente. | Bureta, reactivos y protocolo de laboratorio. |
| pH | Indicar preparación de la muestra y calibrar el equipo con soluciones tampón. | Potenciómetro. |

Humedad, textura, sólidos solubles, acidez y pH son respuestas diferentes. Si no se dispone de instrumentos o reactivos, no reportar esas variables como medidas: mantenerlas como objetivos pendientes y priorizar humedad y masa.

### Análisis estadístico

Para las respuestas registradas durante el secado, considerar secador ($S$), carga ($C$), tiempo ($T$) y sus interacciones. El tiempo está repetido dentro de cada corrida; sus lecturas no son réplicas independientes. Incluir bloque/día y corrida como fuentes de variación, y contemplar la correlación entre medidas del mismo lote.

$$
Y=\mu+S+C+S\times C+T+S\times T+C\times T
+S\times C\times T+B+U_{corrida}+\varepsilon
$$

Para las variables de almacenamiento, estudiar secador, carga, día de almacenamiento y sus interacciones. Incluir la corrida como agrupación. Si cada fecha utiliza un paquete diferente por tratarse de análisis destructivos, considerar los paquetes anidados en la corrida y la fecha; si se sigue no destructivamente el mismo paquete, modelar las fechas como medidas repetidas. Las submuestras técnicas no aumentan el número de réplicas experimentales.

La cantidad final de bloques/réplicas y el modelo deben definirse con los objetivos del curso, la factibilidad del calendario y, de ser posible, la variabilidad observada en un ensayo piloto.

## Archivos principales

- `app.py`: portada y enlaces a las páginas.
- `pages/`: páginas de los apéndices y de la actividad experimental.
- `ui.py`: estilo común de la aplicación.
- `requirements.txt`: dependencias Python.
- `docs/Solar_Dryers-APENDICES.pdf`: documento fuente de los apéndices.

La propuesta experimental es académica y debe validarse con el profesor, los responsables de laboratorio y los procedimientos de operación, seguridad e inocuidad aplicables.
