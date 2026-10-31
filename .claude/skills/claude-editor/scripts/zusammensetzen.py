"""Setzt das fertige Video zusammen: geschnittene Aufnahme unten, Animationen darüber, fertiger Ton.
Aufruf:  python zusammensetzen.py <ebenen.json> <ausgabe.mp4>
ebenen.json:
{
  "grund": "schnitt/schnitt.mp4",                         deine geschnittene Aufnahme (bestimmt Länge und Bildrate)
  "ton": "ton/ton.wav",                                    fertiger Ton aus ton.py (ohne Angabe: Ton der Aufnahme)
  "ebenen": [
    {"datei": "animationen/hook/hook.mp4", "von": 0.0},     Vollbild-Animation (deckt alles ab)
    {"datei": "animationen/titel/titel.mov", "von": 12.4}   durchsichtige Animation (.mov mit --alpha) über dir
  ]
}
"von" = Sekunde im geschnittenen Video, ab der die Ebene läuft. Jede Ebene läuft in ihrer eigenen Länge.
Spätere Ebenen liegen über früheren. Ergebnis in 1080p oder in der Größe der Aufnahme."""
import json, subprocess, sys
cfg = json.load(open(sys.argv[1])); aus = sys.argv[2]
info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,avg_frame_rate',
                       '-of', 'csv=p=0', cfg['grund']], capture_output=True, text=True).stdout.strip().split('\n')[0].split(',')
B, H, R = int(info[0]), int(info[1]), info[2]
eingaenge = ['-i', cfg['grund']]; kette = [f'[0:v]fps={R},format=yuv420p[b0]']; letzte = 'b0'
for i, e in enumerate(cfg.get('ebenen', []), 1):
    eingaenge += ['-i', e['datei']]
    kette.append(f"[{i}:v]fps={R},scale={B}:{H},format=yuva420p,setpts=PTS-STARTPTS+{e['von']}/TB[e{i}]")
    kette.append(f"[{letzte}][e{i}]overlay=eof_action=pass:repeatlast=0[b{i}]"); letzte = f'b{i}'
ton = len(cfg.get('ebenen', [])) + 1
eingaenge += ['-i', cfg.get('ton', cfg['grund'])]
open('/tmp/_zusammensetzen.txt', 'w').write(';'.join(kette))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *eingaenge, '-filter_complex_script', '/tmp/_zusammensetzen.txt',
                '-map', f'[{letzte}]', '-map', f'{ton}:a', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', aus], check=True)
d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,duration', '-of', 'csv=p=0', aus], capture_output=True, text=True).stdout.split()
print('fertig →', aus, d)
