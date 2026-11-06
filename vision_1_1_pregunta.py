"""Punto 1.1 - Pregunta LIBRE sobre UNA imagen (base64).

Eliges la imagen y escribes tu pregunta; puedes hacer varias preguntas seguidas
sobre la misma imagen (Enter vacío para terminar).

Uso:
    python vision_1_1_pregunta.py                                  # menú + pregunta interactiva
    python vision_1_1_pregunta.py comp_2_capacitor                 # imagen por nombre, pregunta interactiva
    python vision_1_1_pregunta.py comp_2_capacitor --pregunta "¿Qué polaridad tiene?"   # una sola pregunta
"""
import argparse

from common import (MODELO_VISION, buscar_imagen, cargar, guardar,
                    listar_imagenes, parte_imagen, preguntar)

ap = argparse.ArgumentParser()
ap.add_argument("imagen", nargs="?")
ap.add_argument("--pregunta", default=None)
args = ap.parse_args()

if args.imagen:
    ruta = buscar_imagen(args.imagen)
else:
    imgs = listar_imagenes()
    if not imgs:
        raise SystemExit("No hay imágenes en la carpeta imagenes/")
    for i, p in enumerate(imgs, 1):
        print(f"{i}. {p.name}")
    ruta = imgs[int(input("Número de la imagen: ")) - 1]

print(f"\nImagen: {ruta.name}\nModelo: {MODELO_VISION}")
llm_model = cargar(MODELO_VISION)
imagen = parte_imagen(ruta)  # se codifica una sola vez

informe = [f"# 1.1\n\n**Imagen:** {ruta.name}\n"]
pregunta = args.pregunta
while True:
    if pregunta is None:
        pregunta = input("\nTu pregunta sobre la imagen (Enter para terminar): ").strip()
        if not pregunta:
            break
    print(f"\nPregunta: {pregunta}\n")
    respuesta = preguntar(llm_model, [{"type": "text", "text": pregunta}, imagen])
    print("Respuesta:\n" + respuesta)
    informe.append(f"**Pregunta:** {pregunta}\n\n**Respuesta ({MODELO_VISION}):**\n\n{respuesta}\n")
    if args.pregunta:  # modo de una sola pregunta
        break
    pregunta = None

if len(informe) > 1:
    guardar("1_1_pregunta.md", "\n".join(informe))