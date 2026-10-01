const fs = require("fs"), vm = require("vm");
const src = fs.readFileSync(process.env.HOME + "/.local/share/kwin/effects/win98menuslide/contents/code/main.js", "utf8");
const sig = { connect() {} };
const ctx = { Effect: { Left: 1, Top: 2, Right: 4, Bottom: 8 }, QEasingCurve: {}, console,
  effects: { windowAdded: sig, windowClosed: sig, windowDataChanged: sig }, effect: {} };
vm.runInNewContext(src + "\nthis.decide = decide;", ctx);
const R = (x, y, w, h) => ({ x, y, width: w, height: h }), P = (x, y) => ({ x, y });
const cases = [
  ["contexto abaixo-direita",        R(500,300,200,250), P(500,300), "HV L T"],
  ["contexto virou pra cima (rodape)",R(500,450,200,250), P(500,700), "HV L B"],
  ["contexto virou pra esquerda",    R(300,300,200,250), P(500,300), "HV R T"],
  ["contexto virou pros dois",       R(300,300,200,250), P(500,550), "HV R B"],
  ["submenu a direita",              R(700,310,180,200), P(650,320), "H L"],
  ["submenu virou pra esquerda",     R(400,310,180,200), P(640,320), "H R"],
  ["menu da barra de menus",         R(100,30,200,300),  P(130,18),  "V T"],
  ["combobox abrindo pra cima",      R(100,400,200,300), P(130,712), "V B"],
  ["tooltip (cursor + 2,16)",        R(502,316,150,24),  P(500,300), "V T"],
  ["menu pelo teclado (mouse dentro)",R(100,100,200,300),P(150,150), "HV L T"],
];
let fail = 0;
for (const [name, f, p, want] of cases) {
  const d = ctx.decide(f, p);
  const got = (d.horiz ? "H" : "") + (d.vert ? "V" : "") +
    (d.horiz ? (d.left ? " L" : " R") : "") + (d.vert ? (d.top ? " T" : " B") : "");
  const ok = got === want; if (!ok) fail++;
  console.log((ok ? "ok  " : "FAIL") + "  " + name.padEnd(34) + " esperado=" + want.padEnd(6) + " obtido=" + got);
}
console.log(fail ? fail + " falha(s)" : "todos os casos ok");
