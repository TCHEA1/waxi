// Copie les polices dans www/fonts pour que le jeu marche sans internet
const fs = require('fs');
const path = require('path');
const out = path.join(__dirname, '..', 'www', 'fonts');
fs.mkdirSync(out, { recursive: true });
const files = [
  ['@fontsource/bungee/files/bungee-latin-400-normal.woff2', 'bungee-400.woff2'],
  ['@fontsource/baloo-2/files/baloo-2-latin-500-normal.woff2', 'baloo2-500.woff2'],
  ['@fontsource/baloo-2/files/baloo-2-latin-700-normal.woff2', 'baloo2-700.woff2'],
  ['@fontsource/baloo-2/files/baloo-2-latin-800-normal.woff2', 'baloo2-800.woff2'],
];
for (const [src, dst] of files) fs.copyFileSync(require.resolve(src), path.join(out, dst));
console.log('Polices copiées');
