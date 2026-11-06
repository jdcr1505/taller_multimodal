"""Puntos 2.1 y 2.2 - Transcribe cada audio de audios/ con Whisper y pasa la
transcripcion al modelo de lenguaje para que responda.

Uso:
    python audio_2_transcripcion_respuesta.py
    python audio_2_transcripcion_respuesta.py --prompt-tecnico   # sesga a Whisper con vocabulario de electronica
    python audio_2_transcripcion_respuesta.py --modelo whisper-large-v3

Si existe audios/guion.json (frase que realmente dijiste), calcula el WER.
"""
import argparse
import json

from common import (AUDIO_DIR, EXT_AUDIO, MODELO_AUDIO, MODELO_TEXTO, cargar,
                    cliente, guardar, preguntar)

VOCAB = ("Electrónica: resistencia, ohmios, kiloohmio, condensador electrolítico, "
         "polaridad, transistor NPN, colector, base, emisor, protoboard, Arduino, "
         "diodo LED, circuito en serie, circuito en paralelo, voltaje, corriente.")
SISTEMA = ("Eres un tutor de electrónica. Responde en español, de forma clara y "
           "técnicamente correcta, en máximo 150 palabras.")

ap = argparse.ArgumentParser()
ap.add_argument("--prompt-tecnico", action="store_true")
ap.add_argument("--modelo", default=MODELO_AUDIO)
args = ap.parse_args()


def wer(ref: str, hyp: str) -> float:
    r, h = ref.lower().split(), hyp.lower().split()
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1,
                          d[i-1][j-1] + (r[i-1] != h[j-1]))
    return d[-1][-1] / max(len(r), 1)


guion_path = AUDIO_DIR / "guion.json"
guion = json.loads(guion_path.read_text(encoding="utf-8")) if guion_path.exists() else {}
guion = {k: v for k, v in guion.items() if not k.startswith("_")}

archivos = sorted(p for p in AUDIO_DIR.iterdir() if p.suffix.lower() in EXT_AUDIO)
if not archivos:
    raise SystemExit("No hay audios en audios/ (wav, mp3, m4a, ogg, webm).")

client = cliente()              # Groq, solo para transcribir con Whisper
llm_model = cargar(MODELO_TEXTO)  # cargar_llm, para responder
md = [f"# 2.1 / 2.2  (Whisper: `{args.modelo}`, LLM: `{MODELO_TEXTO}`, "
      f"prompt técnico: {'sí' if args.prompt_tecnico else 'no'})\n"]
tabla = ["| Archivo | Transcripción | WER |", "|---|---|---|"]

for p in archivos:
    mb = p.stat().st_size / 1e6
    print(f"\n=== {p.name} ({mb:.1f} MB) ===")
    if mb > 25:
        print("AVISO: supera 25 MB (límite del plan gratuito); se omite.")
        continue
    kw = dict(file=(p.name, p.read_bytes()), model=args.modelo, language="es", temperature=0)
    if args.prompt_tecnico:
        kw["prompt"] = VOCAB
    texto = client.audio.transcriptions.create(**kw).text.strip()
    print("Transcripción:", texto)

    ref = guion.get(p.stem)
    w = f"{100 * wer(ref, texto):.0f} %" if ref else "—"
    if ref:
        print("Frase real   :", ref, f"\nWER          : {w}")

    respuesta = preguntar(llm_model, texto, sistema=SISTEMA)
    print("\nRespuesta del modelo:\n" + respuesta)

    tabla.append(f"| {p.name} | {texto} | {w} |")
    md.append(f"## {p.name}\n\n**Transcripción:** {texto}\n\n"
              + (f"**Frase real:** {ref}  \n**WER:** {w}\n\n" if ref else "")
              + f"**Respuesta del modelo:**\n\n{respuesta}\n")

sufijo = "_prompt" if args.prompt_tecnico else ""
guardar(f"2_audio{sufijo}.md", "\n".join(md) + "\n\n## Resumen\n\n" + "\n".join(tabla) + "\n")
