"""Ayuda opcional para grabar desde el microfono.
Uso: python grabar_audio.py audio1_integrante1_sin_ruido [segundos]   (por defecto 20 s)
Guarda audios/<nombre>.wav
"""
import sys
import sounddevice as sd
from scipy.io.wavfile import write
from common import AUDIO_DIR

nombre = sys.argv[1] if len(sys.argv) > 1 else "audio_nuevo"
dur = int(sys.argv[2]) if len(sys.argv) > 2 else 20
sr = 16000  # suficiente para voz y pesa poco
input(f"Pulsa ENTER y habla durante {dur} s...")
print("Grabando...")
audio = sd.rec(int(dur * sr), samplerate=sr, channels=1, dtype="int16")
sd.wait()
AUDIO_DIR.mkdir(exist_ok=True)
write(AUDIO_DIR / f"{nombre}.wav", sr, audio)
print(f"Guardado en audios/{nombre}.wav")
