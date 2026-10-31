// Rendert eine Animation (HTML-Seite) Bild für Bild zu einer Videodatei.
//
// Vertrag der Seite:
//   window.FILM = { dauer: Sekunden, breite: 1920, hoehe: 1080, bereit: Promise|true, zeige(t) }
//   zeige(t) baut exakt das Bild zur Zeit t auf (darf ein Promise zurückgeben).
//   Jedes Bild hängt nur von t ab: kein Math.random ohne festen Startwert, kein Date, keine CSS-Animationen, die selbst laufen.
//
// Aufruf:
//   node render.mjs seite.html --aus=animation.mp4 [--fps=30] [--von=0 --bis=12] [--alpha] [--ton=mix.wav] [--prozesse=4]
//   node render.mjs seite.html --bilder=1.5,4,9.2 --aus=ordner/        (einzelne PNG-Bilder zum Ansehen)
//   --alpha: durchsichtiger Hintergrund → .mov (ProRes 4444), zum Überlagern auf die Kamera.
// Chrome: nutzt Google Chrome, Chromium oder Edge. Anderer Pfad: CHROME=/pfad/zu/chrome node render.mjs …
import puppeteer from 'puppeteer-core';
import { existsSync, mkdirSync, rmSync } from 'fs';
import { tmpdir } from 'os';
import path from 'path';
import { spawnSync } from 'child_process';
const [, , seiteArg, ...rest] = process.argv;
if (!seiteArg) { console.error('Aufruf: node render.mjs <seite.html> --aus=… [Optionen]'); process.exit(1); }
const A = Object.fromEntries(rest.map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const fps = +(A.fps || 30), alpha = !!A.alpha;
const chrome = [process.env.CHROME,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(p => p && existsSync(p));
if (!chrome) { console.error('Kein Chrome gefunden. Pfad setzen: CHROME=/pfad/zu/chrome node render.mjs …'); process.exit(1); }
const url = 'file://' + path.resolve(seiteArg);
const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ['--allow-file-access-from-files', '--hide-scrollbars', '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows', '--force-color-profile=srgb'] });
async function neueSeite() {
  const p = await browser.newPage();
  p.on('pageerror', e => console.error('Fehler in der Seite:', e.message));
  await p.goto(url, { waitUntil: 'load' });
  await p.waitForFunction('window.FILM', { timeout: 20000 });
  const info = await p.evaluate(async () => { await (window.FILM.bereit || true); await document.fonts.ready;
    return { dauer: window.FILM.dauer, breite: window.FILM.breite || 1920, hoehe: window.FILM.hoehe || 1080 }; });
  await p.setViewport({ width: info.breite, height: info.hoehe, deviceScaleFactor: 1 });
  return { p, info };
}
async function bild(p, t, datei) {
  await p.evaluate(async t => { await window.FILM.zeige(t); }, t);   // der Screenshot zeichnet das Bild selbst fertig
  await p.screenshot({ path: datei, omitBackground: alpha, type: 'png' });
}
if (A.bilder) {
  const { p } = await neueSeite(); const ziel = A.aus || 'bilder'; mkdirSync(ziel, { recursive: true });
  for (const t of String(A.bilder).split(',').map(Number)) await bild(p, t, path.join(ziel, `t_${t.toFixed(2)}.png`));
  console.log('Bilder gespeichert in', ziel); await browser.close(); process.exit(0);
}
const erste = await neueSeite(); const info = erste.info; await erste.p.close();
const von = +(A.von || 0), bis = +(A.bis || info.dauer), n = Math.round((bis - von) * fps);
const ordner = path.join(tmpdir(), 'render_' + process.pid); rmSync(ordner, { recursive: true, force: true }); mkdirSync(ordner);
const prozesse = Math.max(1, +(A.prozesse || 4)); let fertig = 0; const start = Date.now();
await Promise.all(Array.from({ length: prozesse }, async (_, w) => {
  const { p } = await neueSeite();
  for (let i = w; i < n; i += prozesse) {
    await bild(p, von + i / fps, path.join(ordner, `${String(i).padStart(6, '0')}.png`));
    if (++fertig % 60 === 0) process.stdout.write(`\r${fertig}/${n} Bilder`);
  }
}));
await browser.close();
const aus = A.aus || (alpha ? 'animation.mov' : 'animation.mp4');
const ton = A.ton ? ['-ss', String(von), '-i', A.ton, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '256k', '-shortest'] : [];
const codec = alpha ? ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le']
                    : ['-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart'];
const r = spawnSync('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', String(fps), '-i', path.join(ordner, '%06d.png'), ...ton, ...codec, aus], { stdio: 'inherit' });
rmSync(ordner, { recursive: true, force: true });
if (r.status !== 0) { console.error('ffmpeg ist fehlgeschlagen'); process.exit(1); }
console.log(`\r${n} Bilder in ${((Date.now() - start) / 1000).toFixed(1)} s → ${aus}`);
