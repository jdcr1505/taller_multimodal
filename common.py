"""Utilidades compartidas por todos los scripts del taller."""
import base64
import io
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE = Path(__file__).parent
IMG_DIR = BASE / "imagenes"
AUDIO_DIR = BASE / "audios"
OUT_DIR = BASE / "resultados"

load_dotenv(BASE / ".env")
load_dotenv()  # por si el .env esta en la raiz del repo

MODELO_VISION = os.getenv("MODELO_VISION", "qwen/qwen3.8-27b")
MODELO_TEXTO = os.getenv("MODELO_TEXTO", MODELO_VISION)
MODELO_AUDIO = os.getenv("MODELO_AUDIO", "whisper-large-v3-turbo")
REASONING = os.getenv("REASONING_EFFORT", "low")

EXT_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}
EXT_AUDIO = {".wav", ".mp3", ".m4a", ".ogg", ".webm"}


def cliente() -> Groq:
    if not os.getenv("GROQ_API_KEY"):
        sys.exit("Falta GROQ_API_KEY. Copia .env.example a .env y pon tu clave.")
    return Groq()


def listar_imagenes() -> list[Path]:
    return sorted(p for p in IMG_DIR.iterdir() if p.suffix.lower() in EXT_MIME)


def buscar_imagen(nombre: str) -> Path:
    """Busca por nombre completo o por nombre sin extension (stem)."""
    for p in listar_imagenes():
        if p.name == nombre or p.stem == nombre:
            return p
    sys.exit(f"No encuentro la imagen '{nombre}' en {IMG_DIR}")


def imagen_b64(ruta: Path, max_bytes: int = 3_000_000) -> tuple[str, str]:
    """Devuelve (base64, mime) según el formato REAL del archivo (no la extension).
    Si el formato no lo acepta Groq (p. ej. AVIF, GIF, BMP) o pesa mucho, lo reconvierte."""
    from PIL import Image, UnidentifiedImageError

    datos = ruta.read_bytes()
    try:
        img = Image.open(io.BytesIO(datos))
        img.load()
    except (UnidentifiedImageError, OSError) as e:
        raise SystemExit(f"'{ruta.name}' no es una imagen válida ({e}). "
                         "Ábrela y vuelve a guardarla como .jpg o .png.")
    formato = (img.format or "").upper()
    mime = {"PNG": "image/png", "JPEG": "image/jpeg", "WEBP": "image/webp"}.get(formato)
    esperado = EXT_MIME.get(ruta.suffix.lower())
    if mime and mime != esperado:
        print(f"   AVISO: {ruta.name} dice ser {esperado} pero en realidad es {formato}; se envía como {mime}.")
    if mime is None or len(datos) > max_bytes:
        if img.mode in ("RGBA", "LA", "P"):  # transparencias -> fondo blanco
            img = img.convert("RGBA")
            fondo = Image.new("RGB", img.size, "white")
            fondo.paste(img, mask=img.split()[-1])
            img = fondo
        else:
            img = img.convert("RGB")
        img.thumbnail((1600, 1600))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        datos, mime = buf.getvalue(), "image/jpeg"
        print(f"   ({ruta.name} convertida/reducida a JPEG, {len(datos)/1e6:.1f} MB)")
    return base64.b64encode(datos).decode("utf-8"), mime


def parte_imagen(ruta: Path) -> dict:
    """Bloque de imagen en el formato de LangChain, igual que multimodal.py."""
    b64, mime = imagen_b64(ruta)
    return {"type": "image", "base64": b64, "mime_type": mime}


def limpiar_think(texto: str) -> str:
    return re.sub(r"<think>.*?</think>", "", texto or "", flags=re.S).strip()


# --- Acceso a `utils/load_model.py` del repo (cargar_llm), como en los ejemplos de clase ---
for _p in [BASE, *BASE.parents]:
    if (_p / "utils" / "load_model.py").exists():
        sys.path.insert(0, str(_p))
        break


def cargar(model: str | None = None, max_tokens: int | None = None):
    """Carga el LLM con cargar_llm (utils.load_model)."""
    try:
        from utils.load_model import cargar_llm
    except ImportError:
        sys.exit("No encuentro utils/load_model.py. Esta carpeta debe estar dentro del "
                 "repositorio del proyecto (que contiene utils/).")
    kw = {"max_tokens": max_tokens or int(os.getenv("MAX_TOKENS", "4096"))}
    if REASONING:
        kw["reasoning_effort"] = REASONING
    return cargar_llm(model_name=model or MODELO_VISION, **kw)


def preguntar(llm, contenido, sistema: str | None = None) -> str:
    """Invoca el LLM con un HumanMessage (str o lista de bloques) y devuelve el texto."""
    from langchain_core.messages import HumanMessage, SystemMessage

    msgs = ([SystemMessage(sistema)] if sistema else []) + [HumanMessage(content=contenido)]
    for intento in range(1, 5):
        try:
            c = llm.invoke(msgs).content
            break
        except Exception as e:  # noqa: BLE001
            if ("429" in str(e) or "rate_limit" in str(e).lower()) and intento < 4:
                print(f"   [límite de tokens de Groq; espero 25 s y reintento ({intento}/3)]")
                time.sleep(25)
            else:
                raise
    if not isinstance(c, str):
        c = "".join(x.get("text", "") if isinstance(x, dict) else str(x) for x in c)
    return limpiar_think(c)


def guardar(nombre: str, texto: str) -> Path:
    OUT_DIR.mkdir(exist_ok=True)
    ruta = OUT_DIR / nombre
    ruta.write_text(texto, encoding="utf-8")
    print(f"\n[guardado en {ruta.relative_to(BASE)}]")
    return ruta


def normalizar(s) -> str:
    """Minusculas, sin tildes, sin espacios; unifica ohmios."""
    if s is None:
        return ""
    s = str(s).lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("ω", "ohm").replace("ohmios", "ohm").replace("ohms", "ohm")
    return re.sub(r"[\s\-_.,]", "", s)