"""Punto 1.3 - Varias imagenes (2 o 3) en UNA solicitud, con pregunta LIBRE.

Eliges las imagenes y escribes tu pregunta; puedes hacer varias preguntas seguidas
sobre el mismo grupo de imagenes (Enter vacío para terminar).

Uso:
    python vision_1_3_multiples.py                                   # menú + pregunta interactiva
    python vision_1_3_multiples.py multi_1_arduino multi_2_protoboard multi_3_diagrama
    python vision_1_3_multiples.py img1 img2 --pregunta "Tu pregunta"   # una sola pregunta
"""
import argparse
import re

from common import (MODELO_VISION, buscar_imagen, cargar, guardar,
                    listar_imagenes, parte_imagen, preguntar)

ap = argparse.ArgumentParser()
ap.add_argument("imagenes", nargs="*")
ap.add_argument("--pregunta", default=None)
args = ap.parse_args()

if args.imagenes:
    rutas = [buscar_imagen(n) for n in args.imagenes]
else:
    imgs = listar_imagenes()
    if not imgs:
        raise SystemExit("No hay imágenes en la carpeta imagenes/")
    for i, p in enumerate(imgs, 1):
        print(f"{i}. {p.name}")
    nums = re.findall(r"\d+", input("Números de las imágenes (2 o 3, separados por coma o espacio): "))
    rutas = [imgs[int(n) - 1] for n in nums]

if not 2 <= len(rutas) <= 3:
    raise SystemExit("Se necesitan 2 o 3 imágenes (máximo 3 por solicitud con Qwen en Groq).")

print("\nImágenes:", ", ".join(p.name for p in rutas), f"\nModelo: {MODELO_VISION}")
llm_model = cargar(MODELO_VISION)
partes = [parte_imagen(p) for p in rutas]  # se codifican una sola vez

informe = [f"# 1.3\n\n**Imágenes:** {', '.join(p.name for p in rutas)}\n"]
pregunta = args.pregunta
while True:
    if pregunta is None:
        pregunta = input("\nTu pregunta sobre las imágenes (Enter para terminar): ").strip()
        if not pregunta:
            break
    print(f"\nPregunta: {pregunta}\n")
    respuesta = preguntar(llm_model, [{"type": "text", "text": pregunta}] + partes)
    print("Respuesta:\n" + respuesta)
    informe.append(f"**Pregunta:** {pregunta}\n\n**Respuesta ({MODELO_VISION}):**\n\n{respuesta}\n")
    if args.pregunta:  # modo de una sola pregunta
        break
    pregunta = None

if len(informe) > 1:
    guardar("1_3_multiples.md", "\n".join(informe))