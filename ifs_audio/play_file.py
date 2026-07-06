"""Usage: python play_file.py <filename>
   Example: python play_file.py reference_original.wav
           python play_file.py A_A_resynth.wav
"""
import sys, os, soundfile as sf
import numpy as np
try: import sounddevice as sd
except: sd = None

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

if len(sys.argv) < 2:
    print("Usage: python play_file.py <filename>")
    print("Files:")
    for f in sorted(os.listdir(out)):
        if f.endswith(".wav"):
            print(f"  {f}")
    sys.exit(1)

path = sys.argv[1]
if not os.path.isabs(path):
    path = os.path.join(out, path)
if not os.path.exists(path):
    print(f"Not found: {path}")
    sys.exit(1)

audio, sr = sf.read(path)
dur = len(audio) / sr
rms = np.sqrt(np.mean(audio**2))
peak = np.max(np.abs(audio))
print(f"{os.path.basename(path)}: {dur:.1f}s, {sr}Hz, RMS={rms:.3f}, Peak={peak:.3f}")

if sd:
    print("Playing... (Ctrl+C to stop)")
    sd.play(audio, sr)
    sd.wait()
else:
    print("Install sounddevice: pip install sounddevice")
