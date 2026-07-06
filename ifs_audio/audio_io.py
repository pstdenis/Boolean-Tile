import numpy as np
import soundfile as sf
import urllib.request
import os
from pathlib import Path

SPEECH_TEXT = (
    "When the sunlight strikes raindrops in the air, "
    "they act like a prism and form a rainbow. "
    "The rainbow is a division of white light into "
    "many beautiful colors."
)


def download_speech(target_dir: str, target_name: str = "reference.wav",
                    sr: int = 22050) -> str:
    target_path = os.path.join(target_dir, target_name)
    if os.path.exists(target_path):
        print(f"  Reference already exists: {target_path}")
        return target_path

    audio = None

    # Attempt 1: gTTS
    try:
        from gtts import gTTS
        import io
        import tempfile
        print("  Generating speech via gTTS...")
        tts = gTTS(text=SPEECH_TEXT, lang="en", slow=False)
        mp3_bytes = io.BytesIO()
        tts.write_to_fp(mp3_bytes)
        mp3_bytes.seek(0)

        import librosa
        audio, orig_sr = librosa.load(mp3_bytes, sr=sr, mono=True)
        print(f"  gTTS OK: {len(audio) / sr:.1f}s @ {sr}Hz")
    except Exception as exc:
        print(f"  gTTS failed ({exc}), trying Archive.org...")

    # Attempt 2: Archive.org public domain speech
    if audio is None:
        try:
            url = ("https://archive.org/download/"
                   "rainbow_passage_2021/"
                   "rainbow_passage_64kb.mp3")
            print(f"  Downloading from {url} ...")
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; IFS-Audio/1.0)"
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                import librosa
                audio, orig_sr = librosa.load(
                    io.BytesIO(resp.read()), sr=sr, mono=True)
                print(f"  Archive.org OK: {len(audio) / sr:.1f}s @ {sr}Hz")
        except Exception as exc:
            print(f"  Archive.org failed ({exc}), using chirp fallback...")

    # Attempt 3: synthetic chirp fallback
    if audio is None:
        print("  Generating synthetic frequency sweep (200-800Hz, 10s)...")
        t = np.arange(sr * 10, dtype=np.float64) / sr
        freq_t = 200 + 600 * t / 10.0
        phase = np.cumsum(2 * np.pi * freq_t / sr)
        audio = 0.3 * np.sin(phase)
        print(f"  Chirp OK: {len(audio) / sr:.1f}s @ {sr}Hz")

    audio = audio.astype(np.float32)
    sf.write(target_path, audio, sr)
    print(f"  Saved: {target_path}")
    return target_path


def load_audio(path: str, sr: int = 22050) -> tuple:
    audio, orig_sr = sf.read(path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if orig_sr != sr:
        import librosa
        audio = librosa.resample(audio, orig_sr=orig_sr, target_sr=sr)
    return audio.astype(np.float64), sr


def write_wav(path: str, audio: np.ndarray, sr: int):
    parent = Path(path).parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, audio.astype(np.float32), sr)
    print(f"  Wrote: {path}")
