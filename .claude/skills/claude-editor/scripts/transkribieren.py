"""Schreibt eine Aufnahme Wort für Wort mit.
Die Aufnahme wird zuerst an den Pausen in kurze Abschnitte zerlegt, jeder Abschnitt wird einzeln mitgeschrieben.
So glättet die Spracherkennung weniger und Wiederholungen bleiben sichtbar.
Aufruf:  python transkribieren.py <aufnahme> <ausgabe.json> [--modell large-v3-turbo] [--sprache de] [--prompt "Fachwörter"]
Ergebnis: {"dauer": s, "abschnitte": [{"nr", "start", "ende", "text", "woerter": [{"wort", "start", "ende", "p"}]}], "geraeusche": [[start, ende]]}
Alle Zeiten in Sekunden der Aufnahme."""
import argparse, json, os, subprocess, sys, tempfile, wave
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument('aufnahme'); ap.add_argument('ausgabe')
ap.add_argument('--modell', default='', help='leer = large-v3-turbo (auf Apple-Chips über MLX, sonst faster-whisper)')
ap.add_argument('--sprache', default='de')
ap.add_argument('--prompt', default='')
ap.add_argument('--pause', type=float, default=0.35, help='Stille in s, an der ein neuer Abschnitt beginnt')
a = ap.parse_args()
tmp = tempfile.mkdtemp()
wav = os.path.join(tmp, 'ton.wav')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.aufnahme, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', wav], check=True)
w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
dauer = len(x) / 16000
# Pegel in 10-ms-Schritten, Stille = unter Grundrauschen + 15 dB
h = 160; m = len(x) // h
db = 20 * np.log10(np.sqrt((x[:m * h].reshape(m, h) ** 2).mean(1)) + 1e-9)
leise = db < np.percentile(db, 5) + 15
abschnitte = []; i = 0; start = None
while i < m:
    if not leise[i]:
        if start is None: start = i
        i += 1; continue
    j = i
    while j < m and leise[j]: j += 1
    if start is not None and (j - i) / 100 >= a.pause:
        abschnitte.append((max(0, start - 10), min(m, i + 10)))   # 100 ms Rand, damit kein Wort abgeschnitten wird
        start = None
    i = j
if start is not None: abschnitte.append((max(0, start - 10), m))
abschnitte = [(s, e) for s, e in abschnitte if e - s >= 15]          # unter 0,15 s ist kein Wort
# Atem und Geräusche sind deutlich leiser als Sprache: Abschnitte, die 20 dB unter dem Sprachpegel bleiben, nicht mitschreiben
sprache = np.percentile(db, 90)
geraeusche = [(s, e) for s, e in abschnitte if np.percentile(db[s:e], 90) < sprache - 20]
abschnitte = [(s, e) for s, e in abschnitte if (s, e) not in geraeusche]
def gut(logprob, kompression, keine_sprache):
    # Whispers eigene Prüfwerte: Endlosschleifen („hela hela …“) haben hohe Kompression, Geräusche niedrige Sicherheit
    return kompression <= 2.4 and not (keine_sprache > 0.6 and logprob < -1.0)
# Auf Apple-Chips läuft MLX auf der Grafikeinheit (etwa 10x schneller), sonst faster-whisper auf dem Prozessor
try:
    import mlx_whisper
    MODELL = a.modell or 'mlx-community/whisper-large-v3-turbo'
    def erkennen(stueck, prompt):
        r = mlx_whisper.transcribe(stueck, path_or_hf_repo=MODELL, language=a.sprache, word_timestamps=True,
                                   initial_prompt=prompt, condition_on_previous_text=False)
        return [(w['word'], w['start'], w['end'], w.get('probability', 1.0)) for seg in r['segments'] if gut(seg['avg_logprob'], seg['compression_ratio'], seg['no_speech_prob'])
                for w in seg.get('words', [])]
except ImportError:
    from faster_whisper import WhisperModel
    modell = WhisperModel(a.modell or 'large-v3-turbo', device='cpu', compute_type='int8')
    def erkennen(stueck, prompt):
        segs, _ = modell.transcribe(stueck, language=a.sprache, word_timestamps=True, initial_prompt=prompt,
                                    condition_on_previous_text=False, vad_filter=False, beam_size=5)
        return [(w.word, w.start, w.end, w.probability) for seg in segs if gut(seg.avg_logprob, seg.compression_ratio, seg.no_speech_prob)
                for w in (seg.words or [])]
# „Äh“ im Prompt sorgt dafür, dass Füllwörter mitgeschrieben statt weggeglättet werden; Fachwörter verbessern die Schreibweise
prompt = ('Äh, ähm. ' + a.prompt).strip()
import re
norm = lambda t: re.sub(r'[^\wäöüß]', '', t.lower())
FLOSKELN = {norm(t) for t in ('Vielen Dank.', 'Vielen Dank fürs Zuschauen.', 'Danke fürs Zuschauen.', 'Tschüss.',
            'Untertitel der Amara.org-Community', 'Untertitel im Auftrag des ZDF für funk, 2017', 'Bis zum nächsten Mal.')}
aus = []
for n, (s, e) in enumerate(abschnitte, 1):
    stueck = x[s * h:e * h]
    woerter = [{'wort': wd.strip(), 'start': round(s / 100 + ws, 3), 'ende': round(s / 100 + we, 3), 'p': round(float(wp), 3)}
               for wd, ws, we, wp in erkennen(stueck, prompt) if wd.strip()]
    # Bei Atem oder Geräuschen ohne Sprache wiederholt Whisper gern den Prompt – solche kurzen Abschnitte verwerfen
    # Typische Whisper-Erfindungen auf Stille
    if norm(' '.join(w['wort'] for w in woerter)) in FLOSKELN: woerter = []
    # Ein Abschnitt unter 0,8 s mit drei gleichen Wörtern hintereinander ist ein Geräusch, keine Sprache
    if (e - s) < 80 and any(norm(woerter[k]['wort']) == norm(woerter[k + 1]['wort']) == norm(woerter[k + 2]['wort']) for k in range(len(woerter) - 2)): woerter = []
    text = ' '.join(wd['wort'] for wd in woerter)
    aus.append({'nr': n, 'start': round(s / 100, 2), 'ende': round(e / 100, 2), 'text': text, 'woerter': woerter})
    print(f'{n}/{len(abschnitte)}  {s / 100:7.2f}  {text[:80]}', flush=True)
json.dump({'dauer': round(dauer, 3), 'abschnitte': aus, 'geraeusche': [[round(s / 100, 2), round(e / 100, 2)] for s, e in geraeusche]}, open(a.ausgabe, 'w'), ensure_ascii=False, indent=1)
print(f'fertig: {len(aus)} Abschnitte, {sum(len(x["woerter"]) for x in aus)} Wörter → {a.ausgabe}')
