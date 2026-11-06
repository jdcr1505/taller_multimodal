# Taller multimodal y audio — Dominio: Electrónica

Visión (Qwen) y transcripción de audio (Whisper) sobre componentes y circuitos electrónicos. Todo se ejecuta por consola.

## Estructura
La carpeta es autocontenida: incluye `utils/load_model.py` (`cargar_llm`, LangChain + Groq), usado para visión y texto como en los ejemplos de clase. La transcripción usa `Groq().audio.transcriptions` directamente. Ejecuta los scripts desde dentro de `taller_multimodal/`.

## Instalación
```bash
pip install -r requirements.txt   # (langchain-groq ya trae `groq`; el repo ya lo usa)
cp .env.example .env      # y pon tu GROQ_API_KEY dentro
```
Variables de entorno: `GROQ_API_KEY` (obligatoria). Opcionales: `MODELO_VISION`, `MODELO_TEXTO`, `MODELO_AUDIO`, `REASONING_EFFORT`.
La clave vive solo en `.env` (ignorado por `.gitignore`). No subir `.env`.

## Carpetas
- `imagenes/` — imágenes del taller (ver `GUIA_TALLER.md` para los nombres) y `verdad_terreno.json`.
- `audios/` — audios (mp3/wav/m4a/ogg/webm) y `guion.json`.
- `resultados/` — salidas en Markdown/JSON generadas por los scripts.

## Cómo ejecutar
| Punto | Comando |
|---|---|
| 1.1 Pregunta sobre una imagen | `python vision_1_1_pregunta.py` |
| 1.2 Extracción estructurada | `python vision_1_2_extraccion.py` (demo de validación: `--demo-invalido`) |
| 1.3 Varias imágenes | `python vision_1_3_multiples.py` |
| 1.4 Errores provocados | `python vision_1_4_errores.py` (o `a b c d`) |
| 2.1 y 2.2 Audio | `python audio_2_transcripcion_respuesta.py` (opcional `--prompt-tecnico`) |
| Grabar un audio (opcional) | `python grabar_audio.py audio1_integrante1_sin_ruido 20` |

Antes de 1.2 edita `imagenes/verdad_terreno.json` con los valores reales de cada imagen.
