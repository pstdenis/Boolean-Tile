import numpy as np
import librosa


def extract_pitch(audio: np.ndarray, sr: int,
                  fmin: float = 65.0, fmax: float = 2093.0,
                  hop_length: int = 512) -> tuple:
    print(f"  Pitch tracking (pyin): {len(audio) / sr:.1f}s, "
          f"sr={sr}, hop={hop_length}...")

    f0, voiced_flag, _ = librosa.pyin(
        audio, fmin=fmin, fmax=fmax, sr=sr,
        frame_length=2048, hop_length=hop_length,
        fill_na=np.nan,
    )

    f0 = np.nan_to_num(f0, nan=0.0)

    # interpolate unvoiced regions
    voiced_idx = np.where(f0 > 0)[0]
    if len(voiced_idx) == 0:
        print("  WARNING: no voiced frames detected!")
        return np.zeros(len(audio)), np.zeros(len(audio))

    interp = np.interp(
        np.arange(len(f0)),
        voiced_idx,
        f0[voiced_idx],
        left=f0[voiced_idx[0]],
        right=f0[voiced_idx[-1]],
    )
    interp = np.maximum(interp, 0.0)

    # upsample to sample rate
    n_samples = len(audio)
    frame_times = np.arange(len(f0)) * hop_length / sr
    sample_times = np.arange(n_samples) / sr
    pitch_samples = np.interp(sample_times, frame_times, interp,
                              left=interp[0], right=interp[-1])
    pitch_samples = np.maximum(pitch_samples, 0.0)

    print(f"  Pitch range: {interp[interp > 0].min():.0f}–"
          f"{interp.max():.0f} Hz, "
          f"voiced: {np.mean(f0 > 0) * 100:.0f}%")

    return pitch_samples, interp
