# 1.3

**Imágenes:** multi_1_arduino.jpg, multi_2_protoboard.jpg, multi_3_diagrama.jpg

**Pregunta:** Te envío 3 imágenes, sin primeros planos adicionales. Describe cada una por separado, cuenta los cables de la protoboard, lee las bandas de la resistencia (la dorada es la última) y dime si el diagrama coincide con el montaje. Si algo no se ve con claridad, dilo. Máximo 200 palabras.

**Respuesta (qwen/qwen3.8-27b):**

**Imagen 1:** Placa Arduino UNO (azul) sobre mesa de madera, vista general. Sin protoboard ni cables.

**Imagen 2:** Protoboard blanca con un LED azul encendido y una resistencia de película (beige). Cables conectados: **4** (rojo con conector azul al riel +, rojo con conector azul a la derecha, negro y rojo/marrón pelado a la izquierda). Bandas de la resistencia (dorada última): **marrón‑negro‑rojo‑dorado → 1‑0‑×10² = 1 kΩ** (±5 %).

**Imagen 3:** Diagrama esquemático: fuente V_BATT en serie con R y el LED (V_LED), corriente I descendente.

**Coincidencia:** Sí, en topología: el montaje es un circuito serie fuente‑resistencia‑LED (rojo al riel +, negro al riel −), igual que el esquema.

**No se ve con claridad:** la conexión exacta de la resistencia al riel negativo y la polaridad del LED (pata larga/corta); los cables pelados del riel + izquierdo resultan ambiguos, por lo que no puedo confirmar con certeza que la resistencia esté en serie como dibuja el diagrama.
