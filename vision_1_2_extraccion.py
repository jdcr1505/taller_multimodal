"""Punto 1.2 - Extraccion estructurada (JSON) + validacion + % de aciertos.

Antes de correr: edita imagenes/verdad_terreno.json con los valores REALES
que tu lees en cada una de las 3 imagenes.

Uso:
    python vision_1_2_extraccion.py
    python vision_1_2_extraccion.py --demo-invalido   # muestra la validacion fallando
"""
import argparse
import json
import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError

from common import (IMG_DIR, MODELO_VISION, buscar_imagen, cargar, guardar,
                    normalizar, parte_imagen, preguntar)

CAMPOS = ["componente", "valor", "unidad", "terminales", "funcion", "referencia"]


class Componente(BaseModel):
    """Esquema esperado. Todos los campos deben existir; pueden ser null."""
    model_config = ConfigDict(extra="forbid")
    componente: str
    valor: Optional[str]
    unidad: Optional[str]
    terminales: Optional[int]
    funcion: Optional[str]
    referencia: Optional[str]


PROMPT = (
    "Analiza la imagen del componente electrónico y extrae su nombre, valor nominal, "
    "unidad, cantidad de terminales, función y referencia visible. "
    "Devuelve EXCLUSIVAMENTE un objeto JSON con estas claves exactas: "
    "componente (string), valor (string), unidad (string), terminales (entero), "
    "funcion (string), referencia (string). Si un dato no es visible, usa null. "
    "No añadas texto fuera del JSON."
)


def extraer_json(texto: str) -> dict:
    """Quita ```json ... ``` y texto sobrante; devuelve dict o lanza ValueError."""
    m = re.search(r"\{.*\}", texto, flags=re.S)
    if not m:
        raise ValueError("la respuesta no contiene un objeto JSON")
    return json.loads(m.group(0))


def validar(texto: str):
    """Devuelve (objeto_validado | None, mensaje_error | None). Nunca lanza."""
    try:
        datos = extraer_json(texto)
    except (ValueError, json.JSONDecodeError) as e:
        return None, f"JSON inválido: {e}"
    try:
        return Componente(**datos), None
    except ValidationError as e:
        detalle = "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors())
        return None, f"No cumple el esquema -> {detalle}"


def es_correcto(campo: str, real, extraido) -> bool:
    r, x = normalizar(real), normalizar(extraido)
    if r == x:
        return True
    if campo in ("funcion", "componente") and r and x:
        return r in x or x in r  # criterio laxo: REVISA estos casos a mano
    return False


ap = argparse.ArgumentParser()
ap.add_argument("--demo-invalido", action="store_true")
args = ap.parse_args()

if args.demo_invalido:
    for malo in ['{"componente": "Resistencia", "valor": "220"}',
                 '{"componente": "R", "valor": "1", "unidad": "k", "terminales": "dos", '
                 '"funcion": "x", "referencia": "y"}',
                 "Claro, aquí está: no hay JSON"]:
        print("Entrada :", malo)
        _, err = validar(malo)
        print("Resultado:", err, "\n")
    raise SystemExit

verdad = json.loads((IMG_DIR / "verdad_terreno.json").read_text(encoding="utf-8"))["imagenes"]
if any("REEMPLAZAR" in json.dumps(v) for v in verdad.values()):
    print("AVISO: verdad_terreno.json aún tiene valores 'REEMPLAZAR'. Edítalo primero.\n")

llm_model = cargar(MODELO_VISION, max_tokens=700)  # el JSON es corto; evita el límite de tokens/min de Groq
filas, aciertos, total, log = [], 0, 0, []

for nombre, real in verdad.items():
    ruta = buscar_imagen(nombre)
    print(f"=== {ruta.name} ===")
    crudo = preguntar(llm_model, [{"type": "text", "text": PROMPT}, parte_imagen(ruta)])
    print("Respuesta cruda:", crudo)
    obj, err = validar(crudo)
    if err:
        print("ERROR DE VALIDACIÓN:", err)
    else:
        print("JSON válido según el esquema ✔")
    extraido = obj.model_dump() if obj else {}
    log.append({"imagen": ruta.name, "cruda": crudo, "error": err, "extraido": extraido})

    for c in CAMPOS:
        ok = es_correcto(c, real.get(c), extraido.get(c))
        aciertos += ok
        total += 1
        filas.append(f"| {ruta.name} | {c} | {real.get(c)} | {extraido.get(c)} | {'Sí' if ok else 'No'} |")
    print()

pct = 100 * aciertos / total if total else 0
tabla = ("| Imagen | Campo | Valor real | Valor extraído | ¿Correcto? |\n"
         "|---|---|---|---|---|\n" + "\n".join(filas))
resumen = f"**Porcentaje de aciertos: {aciertos} de {total} campos = {pct:.1f} %**"
print(tabla + "\n\n" + resumen)
print("\nNota: 'funcion' y 'componente' se comparan de forma laxa; revisa esas filas a mano.")

guardar("1_2_tabla_aciertos.md", tabla + "\n\n" + resumen + "\n")
guardar("1_2_respuestas_crudas.json", json.dumps(log, ensure_ascii=False, indent=2))