#!/usr/bin/env python3
"""Bande-son originale des reels Kazaia (composée par programme, libre de droits).

Usage :
  python3 outils/musique.py --style nuit --duree 17 --accents 10.6,13.8 sortie.wav

Styles :
  nuit      piano doux + nappe, tempo lent (72), mineur — récits du soir, émotion
  lumineux  piano + nappe claire + pulsation légère (84), majeur — solution, soulagement
  elan      arpège + pulsation sourde + charleston feutré (96), majeur — listes, astuces, rythme
Accents : instants (en secondes) où une montée douce et une note cristalline soulignent
un changement de scène (révélation, carte de fin).
Le morceau dure exactement --duree secondes, avec fondu de fin.
"""
import argparse, wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 44100
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}

def hz(name, octave):
    return 440.0 * 2 ** ((NOTE[name] + 12 * (octave + 1) - 69) / 12)

def chord(spec):
    # "A3 C4 E4" -> fréquences
    out = []
    for tok in spec.split():
        n, o = tok[:-1], int(tok[-1])
        out.append(hz(n, o))
    return out

STYLES = {
    "nuit": dict(bpm=72, prog=["A2 E3 A3 C4 E4", "F2 C3 F3 A3 C4", "C3 G3 C4 E4 G4", "G2 D3 G3 B3 D4"],
                 pulse=0.0, hat=0.0, arp=False, pad=0.22, piano=0.30, bright=2600),
    "lumineux": dict(bpm=84, prog=["F2 C3 E3 A3 C4", "A2 E3 G3 C4 E4", "C3 G3 B3 E4 G4", "G2 D3 F#3 B3 D4"],
                     pulse=0.10, hat=0.0, arp=False, pad=0.20, piano=0.30, bright=3600),
    "elan": dict(bpm=96, prog=["C3 G3 C4 E4 G4", "A2 E3 A3 C4 E4", "F2 C3 F3 A3 C4", "G2 D3 G3 B3 D4"],
                 pulse=0.16, hat=0.02, arp=True, pad=0.16, piano=0.26, bright=4200),
}

def env_adsr(n, a, d, s, r):
    t = np.arange(n) / SR
    e = np.ones(n) * s
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    e[:a_n] = np.linspace(0, 1, max(a_n, 1))[:len(e[:a_n])]
    e[a_n:a_n + d_n] = np.linspace(1, s, max(d_n, 1))[:len(e[a_n:a_n + d_n])]
    if r_n > 0:
        e[-r_n:] *= np.linspace(1, 0, r_n)
    return e

def pad_voice(f, n, rng):
    t = np.arange(n) / SR
    v = np.zeros(n)
    for det in (-0.12, 0.0, 0.12):  # désaccord léger = chorus
        ff = f * 2 ** (det / 12)
        ph = rng.uniform(0, 2 * np.pi)
        v += np.sin(2 * np.pi * ff * t + ph) + 0.35 * np.sin(4 * np.pi * ff * t + ph) + 0.12 * np.sin(6 * np.pi * ff * t + ph)
    lfo = 1 + 0.08 * np.sin(2 * np.pi * 0.18 * t + rng.uniform(0, 6))
    return v * lfo / 3

def piano_note(f, dur, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    v = np.zeros(n)
    for k, amp in enumerate([1.0, 0.45, 0.22, 0.12, 0.06], start=1):
        fk = f * k * (1 + 0.0004 * k * k)  # légère inharmonicité
        v += amp * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.6 + 0.9 * k))
    attack = np.minimum(1, t / 0.004)
    return v * attack * vel

def kick(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 55 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)

def hat(rng, dur=0.08):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n) * np.exp(-t * 60)
    sos = butter(2, 7000, "hp", fs=SR, output="sos")
    return sosfilt(sos, x)

def chime(f, dur=2.5):
    n = int(dur * SR); t = np.arange(n) / SR
    v = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * (1.2 + m)) for m, a in [(1, 1), (2.76, .4), (5.4, .2)])
    return v * np.minimum(1, t / 0.002)

def swell(dur=1.6, rng=None):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n)
    sos = butter(2, [800, 5000], "bp", fs=SR, output="sos")
    return sosfilt(sos, x) * (t / dur) ** 2.2 * 0.5

def reverb(x, seconds=2.6, mix=0.32, rng=None):
    n = int(seconds * SR); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.2 / seconds * 2.3)
    sos = butter(1, 5000, "lp", fs=SR, output="sos")
    ir = sosfilt(sos, ir); ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(x, ir)[: len(x)]
    return (1 - mix) * x + mix * wet

def add(buf, s, seg):
    if s >= len(buf): return
    e = min(len(buf), s + len(seg)); buf[s:e] += seg[: e - s]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sortie")
    ap.add_argument("--style", default="nuit", choices=STYLES)
    ap.add_argument("--duree", type=float, required=True)
    ap.add_argument("--accents", default="")
    ap.add_argument("--graine", type=int, default=7)
    a = ap.parse_args()
    st = STYLES[a.style]; rng = np.random.default_rng(a.graine)
    total = int((a.duree + 0.05) * SR)
    beat = 60 / st["bpm"]; bar = 4 * beat
    mix = np.zeros(total + 6 * SR)

    # Nappe : un accord par mesure, enchaînés en fondu
    nb_bars = int(np.ceil(a.duree / bar)) + 1
    for b in range(nb_bars):
        ch = chord(st["prog"][b % len(st["prog"])])
        start = int(b * bar * SR); n = int((bar + 1.2) * SR)
        e = env_adsr(n, 0.9, 0.6, 0.85, 1.2)
        for f in ch[1:]:
            seg = pad_voice(f, n, rng) * e * st["pad"] / len(ch)
            add(mix, start, seg)
        # basse douce
        add(mix, start, 0.5 * st["pad"] * np.sin(2 * np.pi * ch[0] * np.arange(n) / SR) * e)

    # Piano : motif sur les notes de l'accord (arpège ou notes posées)
    pattern = [(0, 3, 1.0), (1.5, 4, .7), (2, 2, .8), (3, 4, .6)] if not st["arp"] else \
              [(i * 0.5, [1, 2, 3, 4, 3, 2, 3, 4][i], .75 if i % 2 else .9) for i in range(8)]
    for b in range(nb_bars):
        ch = chord(st["prog"][b % len(st["prog"])])
        for pos, idx, vel in pattern:
            tt = b * bar + pos * beat
            if tt > a.duree - 0.6: continue
            f = ch[min(idx, len(ch) - 1)] * (2 if a.style != "nuit" else 1)
            note = piano_note(f, 3.2, vel) * st["piano"]
            add(mix, int(tt * SR), note)

    # Pulsation et charleston feutré
    if st["pulse"] > 0:
        k = kick()
        for i in range(int(a.duree / beat)):
            tt = i * beat
            if tt < bar or tt > a.duree - 0.5: continue  # entre après la 1re mesure
            add(mix, int(tt * SR), k * st["pulse"] * (1 if i % 2 == 0 else .55))
    if st["hat"] > 0:
        h = hat(rng)
        for i in range(int(a.duree / (beat / 2))):
            tt = i * beat / 2 + beat / 4
            if tt < bar or tt > a.duree - 0.5: continue
            add(mix, int(tt * SR), h * st["hat"])

    # Accents : montée + note cristalline
    for acc in [float(x) for x in a.accents.split(",") if x.strip()]:
        sw = swell(rng=rng) * 0.05
        add(mix, int(max(0, acc - 1.6) * SR), sw)
        c = chime(hz("E", 6)) * 0.12 + chime(hz("B", 5)) * 0.07
        add(mix, int(acc * SR), c)

    sos = butter(2, st["bright"], "lp", fs=SR, output="sos")
    mix = sosfilt(sos, mix)
    mix = reverb(mix, rng=rng)[:total]
    # fondus
    fi = int(0.25 * SR); fo = int(1.6 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)
    mix[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    mix /= max(1e-9, np.max(np.abs(mix))) / 0.89
    stereo = np.stack([mix, np.roll(mix, int(0.011 * SR)) * 0.96], axis=1)
    pcm = (stereo * 32767).astype(np.int16)
    with wave.open(a.sortie, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(f"OK {a.sortie} ({a.style}, {a.duree} s)")

if __name__ == "__main__":
    main()
