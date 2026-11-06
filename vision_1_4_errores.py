"""Punto 1.4 - Errores provocados a proposito. Cada caso se captura e imprime.

Casos:
  a  modelo SIN vision (LLM_MODEL del .env, por defecto openai/gpt-oss-20b) recibiendo una imagen
  b  4 imagenes en una solicitud (el limite es 3)
  c  tipo MIME mal declarado (se declara application/pdf para una imagen)
  d  imagen demasiado grande (payload sintetico de ~25 MB)

Uso:
    python vision_1_4_errores.py          # corre todos
    python vision_1_4_errores.py a b      # solo algunos
Toma la primera imagen de imagenes/ para los casos.
"""
import base64
import os
import sys

from common import EXT_MIME, MODELO_VISION, cargar, guardar, listar_imagenes

SIN_VISION = os.getenv("MODELO_SIN_VISION", os.getenv("LLM_MODEL", "openai/gpt-oss-20b"))
imgs = listar_imagenes()
if not imgs:
    raise SystemExit("Pon al menos una imagen en imagenes/")
ruta = imgs[0]
datos = ruta.read_bytes()
mime = EXT_MIME[ruta.suffix.lower()]
b64 = base64.b64encode(datos).decode()


def bloque(b64_, mime_):
    return {"type": "image", "base64": b64_, "mime_type": mime_}


Q = {"type": "text", "text": "Identifica los componentes electrónicos de la imagen."}
grande = base64.b64encode(datos + os.urandom(25_000_000)).decode()

casos = {
    "a": ("Modelo sin visión", SIN_VISION, [Q, bloque(b64, mime)]),
    "b": ("4 imágenes (máx. 3)", MODELO_VISION, [Q] + [bloque(b64, mime)] * 4),
    "c": ("MIME mal declarado", MODELO_VISION, [Q, bloque(b64, "application/pdf")]),
    "d": ("Imagen demasiado grande (~25 MB)", MODELO_VISION, [Q, bloque(grande, "image/png")]),
}

from langchain_core.messages import HumanMessage  # noqa: E402

seleccion = sys.argv[1:] or list(casos)
informe = ["# 1.4 Errores provocados\n"]
for k in seleccion:
    titulo, modelo, contenido = casos[k]
    print(f"\n=== Caso {k}: {titulo} | modelo: {modelo} ===")
    try:
        r = cargar(modelo, max_tokens=200).invoke([HumanMessage(content=contenido)])
        salida = "SIN ERROR. Respuesta: " + str(r.content)[:300]
    except Exception as e:  # noqa: BLE001 - queremos ver cualquier error de la API
        salida = f"{type(e).__name__}: {e}"
    print(salida)
    informe.append(f"## Caso {k}: {titulo}\n\nModelo: `{modelo}`\n\n```\n{salida}\n```\n")

guardar("1_4_errores.md", "\n".join(informe))
