# Taller multimodal y audio — Dominio: Electrónica

Visión (Qwen) y transcripción de audio (Whisper) sobre componentes y circuitos electrónicos con Groq. Todo se ejecuta por consola.

## Estructura
- `common.py` — funciones compartidas (carga de imágenes, modelo, reintentos).
- `utils/load_model.py` — `cargar_llm` (LangChain + Groq), usado para visión y texto, como en los ejemplos de clase. La transcripción usa `Groq().audio.transcriptions` directamente.
- `vision_1_1_pregunta.py`, `vision_1_2_extraccion.py`, `vision_1_3_multiples.py`, `vision_1_4_errores.py` — Parte 1 (visión).
- `audio_2_transcripcion_respuesta.py` — Parte 2 (audio).
- `grabar_audio.py` — ayuda opcional para grabar desde el micrófono.
- `imagenes/`, `audios/`, `resultados/` — datos y salidas (ver abajo).

Ejecuta los scripts desde la raíz del repositorio.

## Instalación
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (en Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env        # en Linux/macOS: cp .env.example .env
```
Edita `.env` y pon tu `GROQ_API_KEY`.

## Variables de entorno
- `GROQ_API_KEY` (obligatoria).

La clave vive solo en `.env`, que está ignorado por `.gitignore`. No se sube al repositorio.

## Carpetas
- `imagenes/` — las 7 imágenes del taller y `verdad_terreno.json` (valores reales para medir los aciertos del punto 1.2):
  `01_circuito_led`, `comp_1_resistencia`, `comp_2_capacitor`, `comp_3_transistor`, `multi_1_arduino`, `multi_2_protoboard`, `multi_3_diagrama`.
- `audios/` — los 4 audios (`audio1_integrante1_sin_ruido`, `audio2_integrante2_sin_ruido`, `audio3_integrante1_con_ruido`, `audio4_integrante2_sin_ruido`) y `guion.json` (frase que se dijo en cada uno, para calcular el WER).
- `resultados/` — salidas en Markdown/JSON generadas por los scripts.

## Cómo ejecutar
| Punto | Comando |
|---|---|
| 1.1 Pregunta sobre una imagen | `python vision_1_1_pregunta.py` (eliges la imagen y escribes la pregunta) |
| 1.2 Extracción estructurada | `python vision_1_2_extraccion.py` (demo de validación: `--demo-invalido`) |
| 1.3 Varias imágenes | `python vision_1_3_multiples.py` (eliges 2 o 3 imágenes y escribes la pregunta) |
| 1.4 Error provocado | `python vision_1_4_errores.py a` (casos: `a` modelo sin visión, `b` 4 imágenes, `c` tipo mal declarado, `d` imagen muy grande) |
| 2.1 y 2.2 Audio | `python audio_2_transcripcion_respuesta.py` (eliges los audios; `--todos`, `--prompt-tecnico` opcionales) |
| Grabar un audio (opcional) | `python grabar_audio.py audio1_integrante1_sin_ruido 20` |

Antes de ejecutar el 1.2, revisa `imagenes/verdad_terreno.json`, que contiene los valores reales de cada imagen.

Si Groq devuelve un error 429 por el límite de tokens por minuto del plan gratuito, el programa espera y reintenta solo; si persiste, espera un minuto y vuelve a ejecutar.

## Informe
El informe con capturas y análisis está en este repositorio en PDF.