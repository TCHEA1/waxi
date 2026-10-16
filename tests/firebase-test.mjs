// Vérifie que le serveur Firebase de Waxi accepte : connexion anonyme,
// création d'une partie, arrivée d'un 2e joueur, message de discussion.
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously } from 'firebase/auth';
import { getDatabase, ref, set, get, push, runTransaction, serverTimestamp, remove } from 'firebase/database';
const cfg = {
  apiKey: 'AIzaSyCRBrXJT-Fj88qCU_GrzXXH1PrlJ3lVAE8',
  authDomain: 'waxi-58c6c.firebaseapp.com',
  databaseURL: 'https://waxi-58c6c-default-rtdb.europe-west1.firebasedatabase.app',
  projectId: 'waxi-58c6c',
  appId: '1:202581818055:web:5201c24ad1565002105ce2'
};
const step = async (name, fn) => { try { const r = await fn(); console.log('OK  ', name, r ?? ''); return r; } catch (e) { console.log('ECHEC', name, '→', e.code || '', e.message); process.exitCode = 1; throw e; } };
const code = 'TST' + Math.floor(Math.random() * 10);
try {
  const a1 = initializeApp(cfg, 'j1'), a2 = initializeApp(cfg, 'j2');
  const u1 = await step('connexion anonyme joueur 1', async () => (await signInAnonymously(getAuth(a1))).user.uid);
  const u2 = await step('connexion anonyme joueur 2', async () => (await signInAnonymously(getAuth(a2))).user.uid);
  const d1 = getDatabase(a1), d2 = getDatabase(a2);
  const st = { code, status: 'lobby', hostId: u1, players: [{ id: u1, nom: 'Test1' }], scores: [0], seq: 0 };
  await step('création de la partie ' + code, () => set(ref(d1, `games/${code}/s`), JSON.stringify(st)));
  await step('le joueur 2 rejoint', () => runTransaction(ref(d2, `games/${code}/s`), cur => { if (cur === null) return null; const g = JSON.parse(cur); g.players.push({ id: u2, nom: 'Test2' }); return JSON.stringify(g); }).then(r => r.committed));
  await step('le joueur 1 voit 2 joueurs', async () => JSON.parse((await get(ref(d1, `games/${code}/s`))).val()).players.length);
  await step('message de discussion', () => push(ref(d2, `games/${code}/chat`), { by: u2, nom: 'Test2', t: 'salut', ts: serverTimestamp() }));
  await step('message au nom d\'un autre refusé (attendu)', async () => {
    try { await push(ref(d2, `games/${code}/chat`), { by: u1, t: 'faux', ts: serverTimestamp() }); return 'ATTENTION : accepté'; } catch (e) { return 'bien refusé'; }
  });
  await step('nettoyage', () => remove(ref(d1, `games/${code}`)));
} catch (e) {}
process.exit(process.exitCode || 0);
