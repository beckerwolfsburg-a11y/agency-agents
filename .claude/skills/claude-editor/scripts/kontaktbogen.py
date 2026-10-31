"""Macht Übersichtsbilder (Kontaktbögen) aus einem Video, damit Claude es Bild für Bild ansehen kann.
Aufruf:  python kontaktbogen.py <video> <ordner> [--alle 0.5] [--von 0] [--bis ende] [--spalten 6] [--zeilen 5]
--alle 0.5  = ein Bild alle halbe Sekunde (für Effekte: --alle 0.0333 = jedes einzelne Bild bei 30 B/s)
Ergebnis: <ordner>/bogen_001.jpg … und bogen.txt mit der Zeit jedes Feldes (Bogen, Zeile, Spalte → Sekunde)."""
import argparse, os, subprocess
ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('ordner')
ap.add_argument('--alle', type=float, default=0.5); ap.add_argument('--von', type=float, default=0); ap.add_argument('--bis', type=float)
ap.add_argument('--spalten', type=int, default=6); ap.add_argument('--zeilen', type=int, default=5)
a = ap.parse_args()
os.makedirs(a.ordner, exist_ok=True)
dauer = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.video],
                             capture_output=True, text=True).stdout)
bis = min(a.bis or dauer, dauer)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(a.von), '-to', str(bis), '-i', a.video,
                '-vf', f'fps=1/{a.alle},scale=480:-2,tile={a.spalten}x{a.zeilen}:padding=4:color=white',
                '-q:v', '3', os.path.join(a.ordner, 'bogen_%03d.jpg')], check=True)
pro = a.spalten * a.zeilen; n = int((bis - a.von) / a.alle + 0.999)
with open(os.path.join(a.ordner, 'bogen.txt'), 'w') as f:
    for i in range(n):
        f.write(f'bogen_{i // pro + 1:03d}.jpg  Zeile {i % pro // a.spalten + 1}  Spalte {i % a.spalten + 1}  →  {a.von + i * a.alle:.2f} s\n')
print(f'{(n + pro - 1) // pro} Bögen mit {n} Bildern in {a.ordner}')
