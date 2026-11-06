# Guía: qué poner en cada carpeta y qué capturar para el informe

## IMÁGENES (carpeta `imagenes/`, mínimo 5; esto da 7)

| Archivo (nombre exacto, cualquier extensión png/jpg/webp) | Qué buscar | Punto |
|---|---|---|
| `01_circuito_led.jpg` | Foto de un circuito simple: batería/pila + resistencia + LED (en protoboard o armado). Que se vean bien los 3 componentes. | 1.1 |
| `comp_1_resistencia.jpg` | Una sola resistencia, de cerca, con las bandas de color nítidas (ej. 220 Ω: rojo-rojo-marrón-dorado). | 1.2 |
| `comp_2_capacitor.jpg` | Un condensador electrolítico con la serigrafía legible (ej. "100µF 25V") y la franja de polaridad. | 1.2 |
| `comp_3_transistor.jpg` | Un transistor TO-92 (BC547 / 2N2222) con la referencia impresa legible. | 1.2 |
| `multi_1_arduino.jpg` | Placa Arduino UNO sola. | 1.3 |
| `multi_2_protoboard.jpg` | Un circuito sencillo (LED + resistencia) montado en protoboard, conectado al Arduino o a una pila. | 1.3 |
| `multi_3_diagrama.png` | El esquema/diagrama electrónico DEL MISMO circuito (puede ser un dibujo tuyo o de Tinkercad/Fritzing). Para un buen análisis, que coincida con la foto de la protoboard. | 1.3 |

Consejos: imágenes de ≤ 3 MB y buena luz, sin reflejos. 1.4 reutiliza la primera imagen alfabética (`01_circuito_led`), no necesita otra.
Puedes tomar las fotos tú mismo (lo mejor, para que la "verdad" sea tuya) o usar imágenes libres de internet; en ese caso cita la fuente en el informe.

### Qué escribir en `imagenes/verdad_terreno.json`
Lo que TÚ lees en cada foto, por ejemplo:
- resistencia: componente "Resistencia", valor "220", unidad "Ω", terminales 2, funcion "Limitar corriente", referencia "rojo-rojo-marrón-dorado"
- condensador: "Condensador electrolítico", "100", "µF", 2, "Almacenar energía / filtrar", "100µF 25V"
- transistor: "Transistor NPN", null, null, 3, "Amplificar / conmutar", "BC547"

(Esquema para la plantilla: componente/String, valor/String, unidad/String, terminales/Integer, funcion/String, referencia/String.)

### Qué hacer en el informe por punto
- **1.1**: captura de la imagen + la terminal. Análisis: ¿identificó resistencia, LED, fuente? ¿explicó que la resistencia limita la corriente y el LED tiene polaridad ánodo/cátodo?
- **1.2**: pega la tabla de `resultados/1_2_tabla_aciertos.md` (revísala: "función" y "componente" se corrigen de forma laxa). En "¿Cómo se valida el JSON?": Pydantic con `extra="forbid"`, campos obligatorios, `terminales` entero, y `validar()` captura el error y lo imprime en lugar de fallar (muestra captura de `--demo-invalido`). Analiza errores típicos: confundir valor de bandas de color, leer mal la serigrafía, inventar la función.
- **1.3**: capturas de las 3 imágenes + respuesta. ¿Notó si el diagrama coincide con la protoboard? ¿Alucinó conexiones?
- **1.4**: el script produce 4 errores en `resultados/1_4_errores.md`. Explica la causa de cada uno: (a) modelo sin visión no acepta `image_url`; (b) más de 3 imágenes excede el límite; (c) MIME declarado no es imagen; (d) payload > límite de tamaño. Si alguno no da error (la API a veces es permisiva), repórtalo tal cual y explica por qué.

## AUDIOS (carpeta `audios/`, mínimo 4, 10–30 s, ≥2 integrantes, 1 con ruido)

Nombres exactos (así `guion.json` calcula el WER sin tocar nada):

| Archivo | Quién | Qué decir (lee EXACTO esta frase) |
|---|---|---|
| `audio1_integrante1_sin_ruido.mp3` | Integrante 1 | "¿Cuál es la diferencia entre una resistencia de 220 ohmios y una de 1 kiloohmio, y cómo afecta esto al paso de corriente en un circuito?" |
| `audio2_integrante2_sin_ruido.mp3` | Integrante 2 | "¿Para qué sirve un condensador electrolítico y qué sucede si se conecta con la polaridad invertida?" |
| `audio3_integrante1_con_ruido.mp3` | Integrante 1, **con ruido** (TV, música, ventilador o calle de fondo) | "Explícame cómo funciona un transistor NPN y cuál es la diferencia entre su colector, base y emisor." |
| `audio4_integrante2_sin_ruido.mp3` | Integrante 2 | "¿Cuál es la diferencia entre un circuito conectado en serie y uno conectado en paralelo? Explica cómo cambia la corriente." |

Si cambias las frases, actualiza `audios/guion.json`. Si quieres un audio más corto/largo, procura 10–30 s (a ritmo normal estas frases duran ~10–15 s).

### Qué hacer en el informe
- **2.1**: corre el script, pega la transcripción de cada audio y el WER. Evalúa: ¿acertó "ohmios", "kiloohmio", "condensador electrolítico", "NPN", "colector/emisor"? ¿Se degradó el audio 3 por el ruido? Extra recomendado: corre también con `--prompt-tecnico` y compara (`resultados/2_audio.md` vs `2_audio_prompt.md`).
- **2.2**: pega la respuesta del modelo por cada audio y valídala con tu conocimiento (p. ej. condensador invertido → sobrecalentamiento/ruptura; NPN → corriente de base controla colector-emisor). Si una transcripción salió mal, muestra cómo alteró la respuesta.
