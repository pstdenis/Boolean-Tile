"""Interactive playback browser for IFS audio comparison outputs."""
import soundfile as sf
import numpy as np
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

TILES = ["A", "B", "XOR", "AND", "OR", "FALSE"]
OPTS = {
    "1": ("Reference (original speech)", "reference_original.wav", None),
    "2": ("A — IFS Resynth", "{tile}_A_resynth.wav", "Full IFS replacement"),
    "3": ("B — 4^k Filter Bank", "{tile}_B_fb_4k.wav", "Spectral filtering at f0·4^k"),
    "4": ("B — Walsh φ Filter Bank", "{tile}_B_fb_walsh.wav", "Spectral filtering at φ^k ratios"),
    "5": ("C — Vocoder", "{tile}_C_vocoder.wav", "Cross-synthesis: input envelope × IFS carrier"),
}

try:
    import sounddevice as sd
    has_sd = True
except ImportError:
    has_sd = False

def list_files():
    print("\nAvailable WAV files in output/:")
    for f in sorted(os.listdir(OUTPUT)):
        if f.endswith(".wav"):
            size = os.path.getsize(os.path.join(OUTPUT, f))
            print(f"  {f} ({size//1024}KB)")

def play_file(path, tile=""):
    if not os.path.exists(path):
        print(f"  NOT FOUND: {path}")
        return
    audio, sr = sf.read(path)
    dur = len(audio) / sr
    tag = f" [{tile}]" if tile else ""
    print(f"  Playing: {os.path.basename(path)} ({dur:.1f}s, {sr}Hz, RMS={np.sqrt(np.mean(audio**2)):.3f}){tag}")
    if has_sd:
        sd.play(audio, sr)
        sd.wait()
    else:
        print("  Install sounddevice: pip install sounddevice")

if __name__ == "__main__":
    print("=" * 55)
    print("IFS Audio Comparison — Playback Browser")
    print("=" * 55)

    while True:
        print("\nOptions:")
        print("  tile   Choose tile [A|B|XOR|AND|OR|FALSE|all]")
        print("  ref    Play reference speech")
        print("  1-5    Play option")
        print("          1=Reference  2=A Resynth  3=B 4^k  4=B Walsh  5=C Vocoder")
        print("  list   List all files")
        print("  q      Quit")
        inp = input("\n> ").strip().lower()

        if inp == "q":
            break
        elif inp == "list":
            list_files()
        elif inp == "ref":
            play_file(os.path.join(OUTPUT, "reference_original.wav"))
        elif inp == "all":
            tile = input("Tile for 'all' (or Enter for all 6): ").strip().upper()
            tiles = [tile] if tile and tile in TILES else TILES
            for t in tiles:
                print(f"\n--- {t} ---")
                for key, (desc, fname, _) in OPTS.items():
                    if key == "1":
                        continue
                    play_file(os.path.join(OUTPUT, fname.format(tile=t)), t)
        elif inp in TILES:
            tile = inp.upper()
            print(f"\nTile: {tile}")
            for key, (desc, fname, note) in OPTS.items():
                if key == "1":
                    play_file(os.path.join(OUTPUT, fname))
                else:
                    path = os.path.join(OUTPUT, fname.format(tile=tile))
                    play_file(path, tile)
                if note:
                    print(f"     {note}")
        elif inp in "12345":
            tile = input("Tile [A|B|XOR|AND|OR|FALSE]: ").strip().upper()
            if tile not in TILES:
                print(f"Unknown tile: {tile}")
                continue
            key = inp
            desc, fname, note = OPTS[key]
            if key == "1":
                play_file(os.path.join(OUTPUT, fname))
            else:
                play_file(os.path.join(OUTPUT, fname.format(tile=tile)), tile)
            if note:
                print(f"     {note}")
        else:
            print("Unknown command")
