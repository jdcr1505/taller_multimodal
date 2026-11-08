# 2.1 / 2.2  (Whisper: `whisper-large-v3-turbo`, LLM: `qwen/qwen3.8-27b`, prompt técnico: no)

## audio1_integrante1_sin_ruido.wav

**Transcripción:** ¿Cuál es la diferencia entre una resistencia de 220 ohmios y una de 1 kilo ohmio? ¿Y cómo afecta esto al paso de la corriente en un circuito?

**Frase real:** ¿Cuál es la diferencia entre una resistencia de 220 ohmios y una de 1 kiloohmio, y cómo afecta esto al paso de la corriente en un circuito?  
**WER:** 11 %

**Respuesta del modelo:**

La diferencia es el valor de resistencia al paso de la corriente:

- **220 Ω**: ofrece poca oposición.
- **1 kΩ (1000 Ω)**: ofrece casi 5 veces más oposición.

Por la **ley de Ohm** (I = V/R), a igual tensión, la resistencia menor deja pasar más corriente.

**Ejemplo con 5 V:**
- 220 Ω → I ≈ 22,7 mA
- 1 kΩ → I = 5 mA

**Efecto práctico:**
- Con 220 Ω se disipa más potencia (P = V²/R), por lo que la resistencia se calienta más.
- Con 1 kΩ la corriente es menor, útil para proteger componentes sensibles o limitar corriente en LEDs de bajo consumo.

En resumen: a menor resistencia, mayor corriente y mayor disipación de potencia.

## audio2_integrante2_sin_ruido.wav

**Transcripción:** ¿Para qué sirve un condensador electrolítico y qué sucede si se conecta con la polaridad invertida?

**Frase real:** ¿Para qué sirve un condensador electrolítico y qué sucede si se conecta con la polaridad invertida?  
**WER:** 0 %

**Respuesta del modelo:**

Un condensador electrolítico se utiliza principalmente para **filtrar, almacenar energía y suavizar tensiones** en fuentes de alimentación, acoplar señales y desacoplar ruidos. Su alta capacitancia en volumen reducido se logra gracias a una capa de óxido que actúa como dieléctrico sobre el ánodo.

Si se conecta con la **polaridad invertida**, la capa de óxido se degrada, provocando:

- Corriente de fuga elevada.
- Calentamiento interno.
- Generación de gas (H₂ y O₂).
- Fuga del electrolito o, en casos extremos, **explosión** del componente.

Por eso siempre se debe respetar la marca de polaridad (−) en la carcasa.

## audio3_integrante1_con_ruido.wav

**Transcripción:** Explica a mí cómo funciona un transistor NPN y cuál es la diferencia entre su colector, base y emisor.

**Frase real:** Explícame cómo funciona un transistor NPN y cuál es la diferencia entre su colector, base y emisor.  
**WER:** 18 %

**Respuesta del modelo:**

Un transistor NPN tiene tres regiones: **emisor** (n), **base** (p) y **colector** (n).

- **Emisor:** inyecta electrones (portadores mayoritarios) hacia la base. Está dopado fuertemente.
- **Base:** región delgada y débilmente dopada. Controla cuántos electrones pasan al colector. Una pequeña corriente de base (I_B) regula una corriente mucho mayor de colector (I_C).
- **Colector:** recoge los electrones que atraviesan la base. Está dopado moderadamente y opera en polarización inversa.

**Funcionamiento:** al aplicar un voltaje positivo en la base respecto al emisor, la unión base-emisor se polariza en directo y los electrones fluyen. Si el colector está a mayor potencial que la base, la unión base-colector (inversa) atrae esos electrones. Así, una pequeña I_B controla una I_C mucho mayor (I_C = β·I_B), logrando **amplificación** o **conmutación**.

## audio4_integrante2_sin_ruido.wav

**Transcripción:** ¿Cuál es la diferencia entre un circuito conectado en serie y uno conectado en paralelo?

**Frase real:** ¿Cuál es la diferencia entre un circuito conectado en serie y uno conectado en paralelo?  
**WER:** 0 %

**Respuesta del modelo:**

**Serie:** Los componentes se conectan uno tras otro, formando un único camino para la corriente.

- La **corriente** es la misma en todos los elementos.
- El **voltaje total** se reparte entre ellos (V = V₁ + V₂ + …).
- Si un componente se abre, **todo el circuito deja de funcionar**.

**Paralelo:** Los componentes se conectan entre los mismos dos nodos, creando múltiples caminos.

- El **voltaje** es el mismo en cada rama.
- La **corriente total** se reparte entre las ramas (I = I₁ + I₂ + …).
- Si una rama se abre, **las demás siguen funcionando**.

**Resumen rápido:** En serie comparten corriente; en paralelo comparten voltaje.


## Resumen

| Archivo | Transcripción | WER |
|---|---|---|
| audio1_integrante1_sin_ruido.wav | ¿Cuál es la diferencia entre una resistencia de 220 ohmios y una de 1 kilo ohmio? ¿Y cómo afecta esto al paso de la corriente en un circuito? | 11 % |
| audio2_integrante2_sin_ruido.wav | ¿Para qué sirve un condensador electrolítico y qué sucede si se conecta con la polaridad invertida? | 0 % |
| audio3_integrante1_con_ruido.wav | Explica a mí cómo funciona un transistor NPN y cuál es la diferencia entre su colector, base y emisor. | 18 % |
| audio4_integrante2_sin_ruido.wav | ¿Cuál es la diferencia entre un circuito conectado en serie y uno conectado en paralelo? | 0 % |
