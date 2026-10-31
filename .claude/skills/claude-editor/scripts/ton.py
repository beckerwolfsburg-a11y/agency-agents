"""Mischt den Ton: Stimme + Musik (leiser unter der Stimme) + Soundeffekte auf genauen Zeitpunkten, dann gleiche Lautstärke.
Aufruf:  python ton.py <ton.json> <ausgabe.wav>
ton.json:
{
  "stimme": "schnitt/schnitt.mp4",                 Video oder Tondatei mit deiner Stimme (geschnitten)
  "musik": [{"datei": "ton/musik.mp3", "von": 0, "bis": 52, "pegel": 0.25, "ausblenden": 2}],
  "effekte": [{"datei": "ton/einschlag.wav", "zeit": 3.42, "pegel": 0.8},
              {"erzeugen": "klick", "zeit": 5.10, "pegel": 0.5}],
  "lautheit": -14                                   Ziel in LUFS (YouTube, Instagram: -14)
}
Zeiten in Sekunden des geschnittenen Videos (aus schnitt_woerter.json). "erzeugen" baut einen Effekt im Code:
klick (kurz, hell), schlag (tiefer Einschlag), rauschen (Luftzug, z. B. wenn etwas vorbeifliegt).
Die Musik wird automatisch leiser, solange gesprochen wird (Ducking)."""
import json, os, subprocess, sys, tempfile, wave
import numpy as np
cfg = json.load(open(sys.argv[1])); aus = sys.argv[2]; SR = 48000; tmp = tempfile.mkdtemp()
def lade(datei, von=0.0, bis=None):
    args = ['ffmpeg', '-loglevel', 'error', '-ss', str(von), *(['-to', str(bis)] if bis else []), '-i', datei, '-vn', '-ac', '2', '-ar', str(SR), '-f', 's16le', '-']
    return np.frombuffer(subprocess.run(args, capture_output=True, check=True).stdout, np.int16).reshape(-1, 2).astype(np.float32) / 32768
def erzeugen(art):
    t = np.arange(int(SR * {'klick': 0.06, 'schlag': 0.9, 'rauschen': 0.7}[art])) / SR
    rng = np.random.default_rng(7)                       # fester Startwert → jedes Mal derselbe Klang
    if art == 'klick':
        x = np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 90) + rng.normal(0, 0.3, len(t)) * np.exp(-t * 400)
    elif art == 'schlag':
        f = 38 + 70 * np.exp(-t * 18)                     # tiefer Ton, der nach unten fällt
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5) + rng.normal(0, 0.5, len(t)) * np.exp(-t * 60)
    else:
        n = rng.normal(0, 1, len(t)); h = np.convolve(n, np.ones(24) / 24, 'same')   # weiches Rauschen
        x = h * np.sin(np.pi * t / t[-1]) ** 2 * 3
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    return np.stack([x, x], 1).astype(np.float32)
stimme = lade(cfg['stimme']); n = len(stimme)
musik = np.zeros_like(stimme); effekte = np.zeros_like(stimme)
for m in cfg.get('musik', []):
    a0 = int(m['von'] * SR); dauer = m['bis'] - m['von']
    st = lade(m['datei'], m.get('ab', 0), m.get('ab', 0) + dauer)[: n - a0] * m.get('pegel', 0.25)
    aus_s = int(m.get('ausblenden', 2) * SR)
    if aus_s and len(st) > aus_s: st[-aus_s:] *= np.linspace(1, 0, aus_s)[:, None]
    musik[a0:a0 + len(st)] += st
for e in cfg.get('effekte', []):
    x = erzeugen(e['erzeugen']) if 'erzeugen' in e else lade(e['datei'])
    a0 = int(e['zeit'] * SR); x = x[: max(0, n - a0)] * e.get('pegel', 0.7)
    effekte[a0:a0 + len(x)] += x
# Ducking: Musik um ~6 dB absenken, solange die Stimme laut ist (weich, 200 ms)
pegel = np.sqrt(np.convolve((stimme ** 2).mean(1), np.ones(SR // 50) / (SR // 50), 'same'))
spricht = np.convolve((pegel > 0.02).astype(np.float32), np.ones(SR // 5) / (SR // 5), 'same')
musik *= (1 - 0.5 * spricht)[:, None]
mix = stimme + musik + effekte
def schreibe(x, datei):
    o = wave.open(datei, 'w'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); o.close()
schreibe(mix, f'{tmp}/mix.wav')
# Lautheit: messen, auf das Ziel anheben/absenken, Spitzen mit einem Limiter abfangen (−1,5 dB)
def lufs(datei):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', datei, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(r[r.rindex('I:'):].split()[1])
ziel = cfg.get('lautheit', -14); gain = ziel - lufs(f'{tmp}/mix.wav')
for _ in range(3):   # Limiter kostet etwas Lautheit → bis zu drei Runden nachregeln
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{tmp}/mix.wav', '-af',
                    f'volume={gain:.2f}dB,alimiter=limit=0.84:attack=5:release=60:level=false', '-ar', str(SR), aus], check=True)
    jetzt = lufs(aus)
    if abs(jetzt - ziel) <= 0.3: break
    gain += ziel - jetzt
print(f'Lautheit {lufs(aus):.1f} LUFS')
print(f'Ton fertig: {n / SR:.2f} s, {len(cfg.get("effekte", []))} Effekte → {aus}')
