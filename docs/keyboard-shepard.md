# The Keyboard Model of the Shepard-Risset Illusion

## 1. The Spectral Envelope as Anti-Aliasing

In the standard Shepard-Risset synthesis, a Gaussian amplitude envelope across
octaves is treated as a *necessary* component of the illusion. Without it, the
argument goes, the ear can localize a specific octave, and the wrap-around
becomes audible.

This view confuses two separate things:

| Component | Role | Necessary? |
|---|---|---|
| Octave-stacked pure tones | Provides pitch-class ambiguity — each pitch class is equally represented at every octave | Yes — this is what creates the *possibility* of the illusion |
| Spectral envelope (Gaussian window) | Masks the wrap-edge by ensuring outer octaves are near-silent when they roll over | No — it is an anti-aliasing artifact of finite-range implementation |

The envelope is to the Shepard tone what low-pass filtering is to a zooming Koch
curve animation: it prevents a discontinuity that **wouldn't exist** if the
system were unbounded.

## 2. The Infinite-Keyboard Thought Experiment

Imagine an ideal keyboard extending infinitely in both directions — every pitch
class at every octave from 0 Hz to arbitrarily high frequency. A "note" is the
*entire column* for one pitch class (all G's simultaneously).

If you play columns in chromatic order — all G's, all G#'s, all A's, ... —
the perceived pitch rises by one semitone per step. This works for a simple
reason: each column's power spectrum is the same under octave shift. The
auditory system locks onto a (pitch class, spectral centroid) combination, not
an absolute frequency.

When the progression reaches the note one semitone below the starting pitch
class, the audience hears the *same* relative offset from the original. The
pattern repeats. No envelope was applied — yet the illusion is intact.

The envelope only becomes relevant when the keyboard *runs out of keys* at one
end. The first time the progression reaches the top octave and has nowhere to
go, the note abruptly truncates. The ear hears this. The Gaussian envelope
smooths it over by ensuring nothing was audible at the extreme anyway.

## 3. BTB and the 5-Block Keyboard

The 5 × 88 = 440-key keyboard model is not a practical instrument. It is a
**conceptual proof that the envelope is implementation-dependent**. The
five-block range (2 blocks below standard + 1 standard block + 2 blocks above)
gives enough headroom that the natural limits of hearing (~20 Hz, ~20 kHz) act
as the envelope instead. No artificial Gaussian is needed:

- **Bottom**: 5 octaves below A0 → ~0.86 Hz, inaudible as pitch (felt as
  vibration if at all). By the time the glissando has swept through 3+
  octaves upward, the lowest notes are already inaudible.
- **Top**: 5 octaves above C8 → ~134 kHz, far above the audible ceiling.
  Notes entering this range from below simply vanish from perception.
- **The wrap works** because the note entering at the top (once-inaudible) is the
  same pitch class as the note that left the bottom several steps ago. The ear
  has no way to know that the pattern circled around — it only hears the
  centroid continuing in one direction.

## 4. What This Means for Synthesis

The practical consequence: if you have enough octave headroom, you do not need
an amplitude envelope. A simple hard cutoff at the audible limits suffices. The
Shepard illusion is a *topological* property of pitch-class periodicity under
octave stacking, not a *spectral* property of Gaussian filters.

The envelope is only necessary when the synthesis range clips the audible range
on both sides — which is the case for most computer music implementations
(~8-10 available octaves). With 36 octaves available, the envelope is
superfluous. The range itself provides the decay.

## 5. The IFS Zoom / Shepard Glissando Isomorphism

The Boolean Tile Basis reveals that the Shepard illusion is not an *analogy* to
self-similar geometry — it is the same algebraic symmetry in conjugate domains.

### The IFS attractor has exact 2× self-similarity

Zoom into any corner of a tile's IFS attractor by a factor of 2 and the
structure repeats exactly. This is because the IFS subdivision rule replaces
each cell of the 2×2 truth table with the full tile at the next depth level.
One zoom level = one IFS depth increment = the cycle completes.

### The Shepard glissando has exact 2× octave periodicity

Shift the frequency grid up by one octave and the partial layout repeats
exactly. This is because the φ-ratio spectral channels {1, φ, φ², φ³} are
octave-spaced (log φ ≈ 833¢ ≈ 3 semitones, uniform in log-frequency).
One octave glide = one Shepard cycle = the chord loops.

### The Walsh transform is the bridge

The IFS process generates a 2D binary sequence (varying A and B at each depth
level). The Walsh-Hadamard transform of this sequence gives exactly the four
frequency coefficients (a, x, y, z). The Shepard φ-ratio mapping renders these
as audible:

| Domain | Operation | Symmetry | Cycle |
|---|---|---|---|
| Spatial (IFS) | Zoom 2× into corner | Tile self-similarity | Tile repeats at next depth |
| Frequency (Walsh) | Shift by 1 octave | φ-ratio periodicity | Chord repeats at next octave |

A fixed-A, varying-B slice through the fractal surface is the time-domain
waveform. Its Fourier (Walsh) transform is the spectral layer at that
resolution. Stacking depth levels gives the full Shepard spectrum. The glissando
is the continuous version of stepping through depth levels — each step reveals
the same structure at twice the frequency, and the wrap is invisible because
the underlying tile is scale-invariant.

### The isomorphism is exact

This is not a metaphor. The 2× scaling in the IFS spatial domain *is* the
octave shift in the frequency domain, because the Walsh basis itself is
periodic under dyadic scaling. The Shepard glissando is the same motion as
zooming into the fractal — once you recognize that the Walsh-Hadamard transform
conjugates spatial scaling to frequency translation.

## 6. The Visual Civilization: Color as Octave-Stacked Hue

### A different sensory substrate

Consider a civilization whose primary sense is vision, but whose visual system —
unlike the narrow ~1.7 octaves of human trichromatic vision — can perceive a
dozen or more octaves of electromagnetic frequency simultaneously. In such a
system, the Shepard paradox is a *visual* illusion, not just an auditory one.

Two base frequencies f₀ and f₁ define two primary hues, analogous to the tiles
A and B. Their octave doublings (2f₀, 4f₀, ..., 2ⁿf₀) produce the **same
perceived hue** at increasing visual "brightness-pitch" — analogous to how
octave-spaced tones share a pitch class. A visual civilization would naturally
discover the Walsh algebra through color mixing, just as an auditory
civilization discovers it through tone algebra.

### The tiles as visual hues

| Tile | Active channels | Visual appearance |
|---|---|---|
| **TRUE** | DC only | Broadband white — all frequencies present at equal amplitude |
| **FALSE** | DC zero | Black — no frequencies present |
| **A** | y only (A-dep.) | Pure hue at f₀ — the first primary |
| **B** | x only (B-dep.) | Pure hue at f₁ — the second primary |
| **XOR** | z only (A⊗B) | Pure hue at the difference frequency \|f₀ - f₁\| — a hue that only appears when exactly one primary is present |
| **NOTA** | y inverted | The complement of A — same hue, opposite phase |
| **NOTB** | x inverted | The complement of B |
| **XNOR** | z inverted | The complement of XOR |
| **AND, OR, NOR, NAND, ...** | all three | Composite hues — mixtures of f₀, f₁, and their difference at various amplitudes |

### The visual Shepard paradox

Zoom into any pattern generated by a tile. At 2× magnification, the spatial
structure repeats exactly (the IFS self-similarity). The perceived hue is
determined by the balance of Walsh channels — the ratio of a, x, y, z — which
is invariant under scaling. The civilization sees the same hue at every
magnification level, yet the pattern never stabilizes: finer detail appears
without bound.

If the civilization sweeps the octave-channel that is peak-loud (analogous to
the auditory glide), they perceive an **endless hue shift** toward f₀, wrapping
through the entire color circle when the peak reaches f₁ and the pattern
reasserts itself. The wrap is invisible because the hue at 2f₀ is perceptually
identical to the hue at f₀ — just as the note at 440 Hz and 880 Hz share a
pitch class. The civilization has a **color wheel with 12 or more distinct hues
per octave**, with a Shepard illusion that endlessly cycles through all of them
without repeating.

In human vision, violet feels "closer" to red than green does — a remnant of
the circularity of the 1.7-octave visible spectrum. A many-octave visual system
would experience this circularity as exact: going up through all the octaves
eventually returns to the original hue, just as the Shepard glissando returns
to the original pitch class after one octave of glide.

### The Walsh conjugation in visual terms

Just as the auditory system decomposes a tone into (DC, x, y, z) × (1, φ, φ²,
φ³), the visual system decomposes a color into the same Walsh coefficients ×
base frequencies (f₀, f₁, |f₀-f₁|). The IFS depth process is visual resolution:
at each level d, the civilization sees 2ᵈ×2ᵈ pixels of the pattern. The limit
(infinite depth) is a continuous fractal hue whose local Walsh spectrum is
constant everywhere — a **scale-invariant color**.

The CW chiral traversal, which swaps the x and z channels, corresponds to a
90° rotation of the visual 2×2 pattern. This changes the perceived hue from one
composite to its ν ↔ 16-ν partner — a **topological color complement** that the
civilization's color algebra distinguishes even though the power spectrum is
identical.

### The core insight

In any sensory modality with at least two independent frequency dimensions and
octave-level periodicity, the 16 BTB tiles appear as the complete set of
fundamental "colors" (or "tones"). The Walsh-Hadamard transform is the
universal frequency decomposition for such systems. The Kitaev 16-fold
classification is not specifically about anyons or quantum matter — it is the
classification of scale-invariant dyadic patterns in two variables, realizable
in any modality that respects the Clifford algebra.

## 7. Primary Colors and the Walsh Mixing Model

The two-input Walsh decomposition maps directly onto **color mixing** — both
additive (RGB) and subtractive (CMYK). The four Walsh channels correspond to a
color space with two primaries, one mixed product, and one luminance axis.

### The 4-channel color model

| Walsh channel | Role | Additive model (RGB) | Subtractive model (CMYK) |
|---|---|---|---|
| DC (a) | Luminance / darkness floor | Alpha / opacity | Black (K) |
| x (B-dep.) | First primary | Green (G) | Yellow (Y) |
| y (A-dep.) | Second primary | Red (R) | Cyan (C) |
| z (A⊗B) | Interaction product (third color) | Blue (B) | Magenta (M) |

The three non-DC channels form a **color triangle** analogous to RGB. The two
primaries A and B are Red and Green (additive) or Cyan and Yellow (subtractive).
The interaction product z — the XOR channel — is the third color Blue
(additive) or Magenta (subtractive), which only appears when the two primaries
are mixed with opposite parity.

### The tiles as named colors

| Tile | Active channels | Additive color | Subtractive color | Perceptual description |
|---|---|---|---|---|
| **TRUE** | DC only (a=4) | White | White (no ink) | Maximum luminance |
| **FALSE** | DC zero (a=0) | Black | Black (full ink) | No luminance |
| **A** | y only | Pure red | Pure cyan | Full saturation on second-primary axis |
| **B** | x only | Pure green | Pure yellow | Full saturation on first-primary axis |
| **XOR** | z only | Pure blue | Pure magenta | Full saturation on interaction axis |
| **AND** | x=-1, y=-1, z=+1 (a=1) | Dark, slightly warm tertiary | Dark muddy grey with hue | Low-luminance composite |
| **OR** | x=-1, y=-1, z=-1 (a=3) | Lighter warm tertiary | Pale beige | High-luminance composite; the ν↔16ν partner of AND |
| **NOTA** | y=+2 (a=2) | Cyan (red complement) | Red (cyan complement) | The opposite of A on the second-primary axis |
| **NOTB** | x=+2 (a=2) | Magenta (green complement) | Blue (yellow complement) | The opposite of B on the first-primary axis |
| **XNOR** | z=+2 (a=2) | Yellow (blue complement) | Green (magenta complement) | The opposite of XOR on the interaction axis |

### The chiral traversal as color-space rotation

The CW permutation swaps cells (v₁₀ ↔ v₁₁), which exchanges the x and z Walsh
coefficients while leaving y unchanged. In color terms:

- **Additive**: swaps Green and Blue → Red stays fixed. The color triangle
  rotates 90° around the Red axis, mapping each hue to its topological partner.
- **Subtractive**: swaps Yellow and Magenta → Cyan stays fixed. Same rotation
  around Cyan.

The 8 CW-fixed tiles (TRUE, FALSE, A, NOTA∧B, OR, NOR, B→A, NOTA) correspond
to colors that lie on the **fixed axis** (the y channel or the achromatic axis)
and are unchanged by this rotation.

### Mixing rules

Mixing two tiles in the color model corresponds to adding their Walsh
coefficients (since addition is pointwise XOR in the Boolean domain but
componentwise in the Walsh domain):

- **A + B** (y=2 + x=2) = a composite with all three channels active, no
  preferred orientation → a balanced tertiary
- **XOR + A** (z=-2 + y=-2) = a mix of the interaction hue and the second
  primary → a warm blue or green-magenta, depending on amplitude
- **NOTA + XOR** (y=2 + z=-2) = cancellation on the y axis, leaving pure x →
  pure B

In subtractive (CMYK) terms: mixing two tiles is like overprinting inks. The
DC coefficient adds, and the opponent channels cancel when they have opposite
sign. This is exactly the **algebra of color** under the Walsh-Hadamard
transform: color mixing is Walsh addition, color cancellation is Walsh
subtraction, and the ν ↔ 16-ν partner pairs are complementary colors under
the 90° rotation of the CW traversal.
