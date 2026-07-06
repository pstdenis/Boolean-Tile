import numpy as np

PHI = (1 + np.sqrt(5)) / 2
WALSH_RATIOS = np.array([1.0, PHI**2, PHI, PHI**3], dtype=np.float64)

def get_fractal_wave_value(bits, phase, depth, fine_weight=0.0):
    a = 0.0
    for k in range(depth):
        lp = (phase * (4.0 ** k)) % 1.0
        si = int(lp * 4)
        bv = 1.0 if bits[si] else -1.0
        a += bv / (2.0 ** k)
    if fine_weight > 0.0:
        lp = (phase * (4.0 ** depth)) % 1.0
        si = int(lp * 4)
        bv = 1.0 if bits[si] else -1.0
        a += fine_weight * bv / (2.0 ** depth)
    return a

def generate_ifs_waveform(sr, pitch_curve, tile_bits, depth=6):
    num_samples = len(pitch_curve)
    out = np.zeros(num_samples, dtype=np.float64)
    phase = 0.0
    for i in range(num_samples):
        f0 = pitch_curve[i]
        if f0 > 0:
            phase += f0 / sr
        phase %= 1.0
        out[i] = get_fractal_wave_value(tile_bits, phase, depth)
    mx = np.max(np.abs(out))
    if mx > 0:
        out /= mx
    return out

def generate_walsh_waveform(sr, pitch_curve, walsh_coeffs, num_octaves=6):
    num_samples = len(pitch_curve)
    out = np.zeros(num_samples, dtype=np.float64)

    # skip DC (index 0), use x, y, z (indices 1, 2, 3)
    active = [(i, c / 4.0) for i, c in enumerate(walsh_coeffs[1:], 1) if c != 0]
    if not active:
        return out

    t = np.arange(num_samples, dtype=np.float64) / sr
    for coeff_idx, norm_coeff in active:
        ratio = WALSH_RATIOS[coeff_idx]
        for octave in range(num_octaves):
            gain = norm_coeff / (2.0 ** octave)
            f_ratio = ratio * (2.0 ** octave)
            phase_accum = np.zeros(num_samples, dtype=np.float64)
            last_phase = 0.0
            for i in range(num_samples):
                f0 = pitch_curve[i]
                if f0 > 0:
                    last_phase += f0 * f_ratio / sr
                phase_accum[i] = last_phase
            out += gain * np.sin(2.0 * np.pi * phase_accum)

    mx = np.max(np.abs(out))
    if mx > 0:
        out /= mx
    return out

def compute_ifas_harmonic_mask(sr, pitch_curve, tile_bits, depth, hop_length, fft_size):
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    n_bins = len(freqs)
    n_frames = (len(pitch_curve) + hop_length - 1) // hop_length

    masks = np.zeros((n_frames, n_bins), dtype=np.float64)
    for frame_idx in range(n_frames):
        center_sample = frame_idx * hop_length
        f0_val = pitch_curve[center_sample] if center_sample < len(pitch_curve) else 0.0
        if f0_val <= 0:
            masks[frame_idx, :] = 1.0
            continue

        mask = np.zeros(n_bins)
        time_s = center_sample / sr
        phase_acc = time_s * f0_val

        for k in range(depth):
            harmonic = f0_val * (4.0 ** k)
            if harmonic > sr / 2:
                break

            phase_k = (phase_acc * (4.0 ** k)) % 1.0
            quadrant = int(phase_k * 4) % 4
            gain = (1.0 if tile_bits[quadrant] else -1.0) / (2.0 ** k)

            bw_ratio = 0.08
            sigma = harmonic * bw_ratio
            window = np.exp(-0.5 * ((freqs - harmonic) / sigma) ** 2)
            mask += gain * window

        masks[frame_idx, :] = mask
    return masks, freqs

def compute_walsh_harmonic_mask(sr, pitch_curve, walsh_coeffs, num_octaves, hop_length, fft_size):
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    n_bins = len(freqs)
    n_frames = (len(pitch_curve) + hop_length - 1) // hop_length

    masks = np.zeros((n_frames, n_bins), dtype=np.float64)
    active = [(i, c / 4.0) for i, c in enumerate(walsh_coeffs[1:], 1) if c != 0]

    for frame_idx in range(n_frames):
        center_sample = frame_idx * hop_length
        f0_val = pitch_curve[center_sample] if center_sample < len(pitch_curve) else 0.0
        if f0_val <= 0:
            masks[frame_idx, :] = 1.0
            continue

        mask = np.zeros(n_bins)
        for coeff_idx, norm_coeff in active:
            ratio = WALSH_RATIOS[coeff_idx]
            for octave in range(num_octaves):
                harmonic = f0_val * ratio * (2.0 ** octave)
                if harmonic > sr / 2:
                    break
                gain = norm_coeff / (2.0 ** octave)
                bw_ratio = 0.08
                sigma = harmonic * bw_ratio
                window = np.exp(-0.5 * ((freqs - harmonic) / sigma) ** 2)
                mask += gain * window

        masks[frame_idx, :] = mask
    return masks, freqs
