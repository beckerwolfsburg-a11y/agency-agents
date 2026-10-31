// Gemeinsame Bewegungen. Alles haengt nur von t ab.
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
// Kurve aus den Vorbildern: cubic-bezier(0.16, 1, 0.3, 1), schnell rein, lange sanft aus. Naeherung als expo-out.
const aus = x => { x = clamp(x, 0, 1); return x === 1 ? 1 : 1 - Math.pow(2, -10 * x); };
const ein = x => { x = clamp(x, 0, 1); return x * x * x; };
const fort = (t, ab, dauer) => clamp((t - ab) / dauer, 0, 1);
// Standard-Auftritt: 0,4 s einblenden, 14 px von unten. Abgang optional: 0,3 s ausblenden.
function auftritt(el, t, ab, weg = Infinity, hub = 14) {
  const e = aus(fort(t, ab, 0.4)) * (1 - ein(fort(t, weg, 0.3)));
  el.style.opacity = e;
  el.style.transform = `translateY(${(1 - aus(fort(t, ab, 0.4))) * hub}px)`;
  return e;
}
// Inaktiv = unscharf und gedimmt, aktiv = scharf (Lebersorger-Kapitelmenue)
function fokus(el, f) {
  el.style.filter = `blur(${(1 - f) * 6}px)`;
  el.style.opacity = 0.35 + 0.65 * f;
}
