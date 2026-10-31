"""Schneidet eine Aufnahme nach einer Schnittliste und kürzt die Pausen.
Aufruf:  python schneiden.py <aufnahme> <schnitt.json> <ausgabe.mp4> [--woerter woerter.json] [--pause 0.25] [--rest 0.12]
schnitt.json: {"stuecke": [{"von": 12.31, "bis": 18.02, "satz": 3}, ...]}   (Zeiten der Aufnahme, in der Reihenfolge des Videos)
Was das Skript macht:
- Ränder: Jedes Stück geht bis zum echten Wortrand – inklusive leiser Zischlaute wie ein „t“ oder „s“ am Wortende, die kaum
  Pegel haben, aber hohe Frequenzen. So wird nie eine Endung oder ein Wortanfang abgeschnitten. Atem mit Abstand zum Wort fliegt raus.
- Pausen: Stille innerhalb eines Stücks, die länger als --pause ist, wird auf --rest gekürzt. Kurze Stillen mitten im Wort
  (vor k, t, p) sind kürzer und bleiben stehen.
- Bild und Ton: Alle Schnitte liegen genau auf Bildgrenzen, der Ton wird sample-genau geschnitten → Lippen bleiben synchron.
Ergebnis: <ausgabe.mp4>, daneben <ausgabe>_zeiten.json (behaltene Stücke, alte → neue Zeit) und, mit --woerter,
<ausgabe>_woerter.json (jedes behaltene Wort mit seiner Zeit im geschnittenen Video – Grundlage für Animationen und Effekte)."""
import argparse, json, os, subprocess, tempfile, wave
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument('aufnahme'); ap.add_argument('schnitt'); ap.add_argument('ausgabe')
ap.add_argument('--woerter'); ap.add_argument('--pause', type=float, default=0.25); ap.add_argument('--rest', type=float, default=0.12)
a = ap.parse_args()
tmp = tempfile.mkdtemp(); basis = os.path.splitext(a.ausgabe)[0]
def probe(*args):
    return subprocess.run(['ffprobe', '-v', 'error', *args, a.aufnahme], capture_output=True, text=True).stdout.strip().split('\n')[0].split(',')[0]
zaehler, nenner = map(int, probe('-select_streams', 'v:0', '-show_entries', 'stream=avg_frame_rate', '-of', 'csv=p=0').split('/'))
FPS = zaehler / nenner
# Startzeiten von Bild und Ton (bei manchen Kameras nicht 0). Alle Zeiten (schnitt.json, Wörter) zählen ab Tonbeginn.
def start(strom):
    v = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', strom, '-show_entries', 'stream=start_time', '-of', 'csv=p=0', a.aufnahme],
                       capture_output=True, text=True).stdout.strip().split('\n')[0].split(',')[0]
    return float(v) if v not in ('', 'N/A') else 0.0
V0, A0 = start('v:0'), start('a:0'); D = A0 - V0   # Tonzeit + D = Zeit ab Bildbeginn
# Analyse in 10-ms-Schritten: Gesamtpegel UND Pegel der hohen Frequenzen (Zischlaute haben kaum Gesamtpegel)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.aufnahme, '-vn', '-ac', '1', '-ar', '16000', f'{tmp}/a.wav'], check=True)
w = wave.open(f'{tmp}/a.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
h = 160; m = len(x) // h; X = x[:m * h].reshape(m, h) * np.hanning(h)
F = np.abs(np.fft.rfft(X, axis=1)) ** 2; f = np.fft.rfftfreq(h, 1 / 16000)
ges = 10 * np.log10(F.sum(1) + 1e-12); hoch = 10 * np.log10(F[:, f > 3500].sum(1) + 1e-12)
# Stimme: höchstens 24 dB unter dem Sprachpegel (Atem liegt meist darunter), einzelne Ausreißer per Mehrheit über 50 ms glätten
roh = ges > max(np.percentile(ges, 5) + 15, np.percentile(ges, 90) - 24)
stimme = np.convolve(roh.astype(int), np.ones(5, int), 'same') >= 3
# Kurze Einzelgeräusche (Schmatzen, Klicks): unter 80 ms und rundherum mindestens 150 ms Stille → keine Stimme
k = 0
while k < m:
    if stimme[k]:
        e = k
        while e < m and stimme[e]: e += 1
        if e - k < 8 and not stimme[max(0, k - 15):k].any() and not stimme[e:e + 15].any(): stimme[k:e] = False
        k = e
    else: k += 1
zisch = hoch > np.percentile(hoch, 5) + 20         # Zisch- und Knacklaute (s, t, z, f): leise, aber hohe Frequenzen
def zisch_rand(i, richtung, max_f, luecke=6):
    """Ab dem Rand eines Worts (i = erstes stilles Bild) einen anhängenden Zischlaut mitnehmen: höchstens max_f × 10 ms,
    Lücken bis 60 ms (Verschluss vor einem „t“). Atem kommt meist mit größerem Abstand und bleibt draußen."""
    k = i if richtung > 0 else i - 1; letzt = None; still = 0; schritte = 0
    while 0 <= k < m and schritte < max_f:
        if zisch[k] or stimme[k]: letzt = k; still = 0
        else:
            still += 1
            if still > luecke: break
        k += richtung; schritte += 1
    if letzt is None: return i
    return letzt + 1 if richtung > 0 else letzt
def stimm_rand(i, richtung, max_f, luecke=6):
    """Von i aus so weit gehen, wie zusammenhängend Stimme ist (kleine Lücken erlaubt)."""
    k = i; letzt = i; still = 0; schritte = 0
    while 0 <= k < m and schritte < max_f:
        if stimme[k]: letzt = k; still = 0
        else:
            still += 1
            if still > luecke: break
        k += richtung; schritte += 1
    return letzt
S = json.load(open(a.schnitt))['stuecke']
behalten = []
for s in S:
    v, b = int(s['von'] * 100), min(m - 1, int(s['bis'] * 100))
    # erste/letzte Stimme im Stück suchen (Wortzeiten können etwas Stille enthalten), dann bis zum echten Wortrand gehen
    erst = next((k for k in range(v, b) if stimme[k]), v); letzt = next((k for k in range(b, v, -1) if stimme[k]), b)
    a0 = stimm_rand(erst, -1, 20); a1 = zisch_rand(a0, -1, 10)
    b0 = stimm_rand(letzt, +1, 15) + 1; b1 = zisch_rand(b0, +1, 15)
    von, bis = max(0, a1 / 100 - 0.04), min(m / 100, b1 / 100 + 0.05)
    # Pausen innerhalb des Stücks kürzen (Zischlaute an beiden Rändern der Pause bleiben)
    teile = []; anfang = von; i = a1
    while i < b1:
        if not stimme[i]:
            j = i
            while j < b1 and not stimme[j]: j += 1
            i2, j2 = zisch_rand(i, +1, 15), zisch_rand(j, -1, 10)
            if j < b1 and (j2 - i2) / 100 > a.pause:
                teile.append((anfang, i2 / 100 + a.rest * 0.55)); anfang = j2 / 100 - a.rest * 0.45
            i = j
        else: i += 1
    teile.append((anfang, bis))
    behalten += teile
# Auf Bildgrenzen legen, Überlappungen zusammenführen
raster = []
for p, q in behalten:
    kp, kq = int(np.floor((p + D) * FPS)), int(np.ceil((q + D) * FPS))
    if raster and kp <= raster[-1][1] and kp >= raster[-1][0]: raster[-1][1] = max(raster[-1][1], kq)
    elif kq > kp: raster.append([kp, kq])
stuecke = [(kp / FPS - D, kq / FPS - D) for kp, kq in raster]   # in Tonzeit, Grenzen genau auf Bildgrenzen
# Bild: Stücke per select behalten. select kann nur vorwärts – liegt ein späterer Versuch zeitlich vor einem früheren Satz,
# wird in mehreren Läufen gerendert und aneinandergehängt.
laeufe = [[stuecke[0]]]
for st in stuecke[1:]:
    if st[0] >= laeufe[-1][-1][1] - 1e-6: laeufe[-1].append(st)
    else: laeufe.append([st])
teile_bild = []
for n, lauf in enumerate(laeufe):
    gruppen = [lauf[k:k + 12] for k in range(0, len(lauf), 12)]
    ausdruck = '+'.join('(' + '+'.join(f'between(t,{A0 + p - 0.5 / FPS:.5f},{A0 + q - 0.5 / FPS:.5f})' for p, q in g) + ')' for g in gruppen)
    open(f'{tmp}/v{n}.txt', 'w').write(f"select='{ausdruck}',setpts=N/({zaehler}/{nenner})/TB")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.aufnahme,
                    '-filter_script:v', f'{tmp}/v{n}.txt', '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                    '-r', f'{zaehler}/{nenner}', f'{tmp}/b{n}.mp4'], check=True)
    teile_bild.append(f'{tmp}/b{n}.mp4')
open(f'{tmp}/liste.txt', 'w').write(''.join(f"file '{t}'\n" for t in teile_bild))
# Ton: sample-genau schneiden, 5 ms Blende an jeder Naht gegen Knackser
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.aufnahme, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', f'{tmp}/t.wav'], check=True)
tw = wave.open(f'{tmp}/t.wav'); y = np.frombuffer(tw.readframes(tw.getnframes()), np.int16).reshape(-1, 2).astype(np.float32)
blende = 240; stuecke_ton = []
for p, q in stuecke:
    i0, i1 = int(round(p * 48000)), int(round(q * 48000))
    st = y[max(0, i0):max(0, i1)].copy()
    if i0 < 0: st = np.concatenate([np.zeros((-i0, 2), np.float32), st])   # Ton beginnt später als das Bild
    if len(st) > 2 * blende:
        r = np.linspace(0, 1, blende)[:, None]; st[:blende] *= r; st[-blende:] *= r[::-1]
    stuecke_ton.append(st)
z = np.concatenate(stuecke_ton).clip(-32768, 32767).astype(np.int16)
o = wave.open(f'{tmp}/schnitt.wav', 'w'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(48000); o.writeframes(z.tobytes()); o.close()
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/liste.txt', '-i', f'{tmp}/schnitt.wav',
                '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', a.ausgabe], check=True)
# Zeiten-Tabelle alt → neu
tab = []; neu = 0.0
for p, q in stuecke: tab.append({'alt_von': round(p, 4), 'alt_bis': round(q, 4), 'neu_von': round(neu, 4)}); neu += q - p
json.dump({'fps': FPS, 'dauer': round(neu, 3), 'stuecke': tab}, open(basis + '_zeiten.json', 'w'), indent=1)
def alt_zu_neu(t):
    for s in tab:
        if s['alt_von'] - 0.02 <= t <= s['alt_bis'] + 0.02: return s['neu_von'] + min(max(t, s['alt_von']), s['alt_bis']) - s['alt_von']
    return None
if a.woerter:
    J = json.load(open(a.woerter)); ww = []
    for ab in J['abschnitte']:
        for wd in ab['woerter']:
            s0, s1 = alt_zu_neu(wd['start']), alt_zu_neu(wd['ende'])
            if s0 is not None and s1 is not None: ww.append({'wort': wd['wort'], 'start': round(s0, 3), 'ende': round(s1, 3)})
    ww.sort(key=lambda w: w['start'])
    json.dump(ww, open(basis + '_woerter.json', 'w'), ensure_ascii=False, indent=1)
d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,duration', '-of', 'csv=p=0', a.ausgabe], capture_output=True, text=True).stdout.split()
print(f'{len(S)} Stücke → {len(stuecke)} Teile nach Pausenkürzung, neue Länge {neu:.2f} s · {a.ausgabe} {d}')
