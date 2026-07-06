"""Distributable render: Reich Phasing (Rainbow Passage) at CD quality."""

import os, sys
import numpy as np
import soundfile as sf
import librosa

# --- Config ---
SR = 44100
CYCLE_COUNT = 100
CROSSFADE_S = 2.0
FADE_IN_S = 2.0
FADE_OUT_S = 4.0

SPEED_SHIFTS = [1.0, 1.01, 0.99, 1.02, 0.98, 1.03]

TITLE = "Reich Phasing (Rainbow Passage)"
ARTIST = "Boolean Tile IFS"
ALBUM = "IFS Audio Works"
DATE = "2026"
GENRE = "Electronic / Generative"
COMMENT = "6-voice Reich-style phasing of the Rainbow Passage speech sample. "
COMMENT += "Each voice time-stretched at a different speed ratio, "
COMMENT += "looped 100 times for a 19-minute evolving texture."

# --- Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

SPEECH_PATH = os.path.join(OUT_DIR, f"reference_{SR}.wav")
WAV_PATH = os.path.join(OUT_DIR, "reich_phasing_44k.wav")
FLAC_PATH = os.path.join(OUT_DIR, "Reich_Phasing_Rainbow_Passage.flac")

SPEECH_TEXT = (
    "When the sunlight strikes raindrops in the air, "
    "they act like a prism and form a rainbow. "
    "The rainbow is a division of white light into "
    "many beautiful colors."
)

# --- 1. Get speech audio at CD quality ---
if os.path.exists(SPEECH_PATH):
    print(f"Reference exists: {SPEECH_PATH}")
    audio, _ = sf.read(SPEECH_PATH)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    audio = audio.astype(np.float64)
else:
    print("Generating speech via gTTS...")
    from gtts import gTTS
    import io
    tts = gTTS(text=SPEECH_TEXT, lang="en", slow=False)
    mp3_bytes = io.BytesIO()
    tts.write_to_fp(mp3_bytes)
    mp3_bytes.seek(0)
    audio, orig_sr = librosa.load(mp3_bytes, sr=SR, mono=True)
    audio = audio.astype(np.float64)
    sf.write(SPEECH_PATH, audio.astype(np.float32), SR)
    print(f"  Saved: {SPEECH_PATH}")

N = len(audio)
audio_len = N / SR
total_samples = N * CYCLE_COUNT
total_dur = total_samples / SR
print(f"\nSpeech: {audio_len:.3f}s @ {SR}Hz ({N} samples)")
print(f"Output: {total_dur:.1f}s ({total_dur/60:.1f} min), "
      f"{total_samples} samples")
print(f"Voices: {len(SPEED_SHIFTS)} {SPEED_SHIFTS}")

# --- 2. Generate mix ---
mix = np.zeros(total_samples, dtype=np.float64)

for vi, shift in enumerate(SPEED_SHIFTS):
    rate = 1.0 / shift
    stretched = librosa.effects.time_stretch(audio, rate=rate)
    loop_len = len(stretched)
    loop_dur = loop_len / SR
    print(f"  V{vi+1}: shift={shift:.4f} loop={loop_dur:.3f}s", flush=True)
    for start in range(0, total_samples, loop_len):
        end = min(start + loop_len, total_samples)
        mix[start:end] += stretched[:end - start]

print(f"  Mix peak before norm: {np.max(np.abs(mix)):.4f}")

# --- 3. Fade in/out and crossfade ---
cf = int(CROSSFADE_S * SR)
fi = int(FADE_IN_S * SR)
fo = int(FADE_OUT_S * SR)

# Crossfade at loop seam
mix[-cf:] *= np.linspace(1.0, 0.0, cf)
mix[:cf] *= np.linspace(0.0, 1.0, cf)

# Fade in at start (after crossfade)
mix[:fi] *= np.linspace(0.0, 1.0, fi)

# Fade out at end (before crossfade region)
mix[-fo:] *= np.linspace(1.0, 0.0, fo)

# --- 4. Normalize ---
pk = np.max(np.abs(mix))
if pk > 0:
    mix /= pk
print(f"  Normalized: peak=1.0 (was {pk:.4f})")

# --- 5. Write 16-bit WAV ---
stereo = np.column_stack((mix, mix))
sf.write(WAV_PATH, stereo.astype(np.float32), SR)
print(f"Wrote: {WAV_PATH}")

# --- 6. Convert to FLAC with metadata ---
meta = {
    "title": TITLE,
    "artist": ARTIST,
    "album": ALBUM,
    "date": DATE,
    "genre": GENRE,
    "comment": COMMENT,
}
meta_args = []
for k, v in meta.items():
    meta_args.extend(["-metadata", f"{k}={v}"])

cmd = (["ffmpeg", "-y", "-i", WAV_PATH,
        "-c:a", "flac", "-sample_fmt", "s16",
        "-ar", str(SR)] + meta_args +
       [FLAC_PATH])
import subprocess
print("Converting to FLAC with metadata...")
subprocess.run(cmd, check=True, capture_output=True)

size_mb = os.path.getsize(FLAC_PATH) / (1024 * 1024)
print(f"\nDone: {FLAC_PATH}")
print(f"      {size_mb:.1f} MB")
