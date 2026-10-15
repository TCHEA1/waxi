# Waxi — application Android

Puzzle de blocs aux motifs wax. Version 1 : jeu solo, jeu à 2 ou 3 joueurs sur le même téléphone, publicités AdMob (pub récompensée pour continuer, pub entre les parties toutes les 3 parties).

Identifiant de l'appli : `com.marestchea.waxi`

## Obtenir l'APK avec GitHub

1. Crée un compte gratuit sur github.com.
2. Crée un dépôt vide nommé `waxi` (bouton « New repository », sans README).
3. Envoie le projet dans ce dépôt (Claude peut le faire pour toi si tu lui donnes le nom du dépôt).
4. GitHub fabrique l'APK tout seul en 5 à 10 minutes : onglet **Actions** → dernière exécution « Fabriquer l'APK » → en bas, section **Artifacts** → `waxi-apk`.
5. Décompresse le fichier téléchargé, envoie `waxi.apk` sur ton téléphone et ouvre-le. Android te demandera d'autoriser l'installation d'applications inconnues : accepte pour cette fois.

Cet APK sert à **tester**. Pour le Play Store, il faudra une version signée (fichier `.aab`), préparée à l'étape suivante.

## Avant la publication sur le Play Store

1. **Compte AdMob** (admob.google.com) : crée l'appli « Waxi », puis deux blocs d'annonces : un « Avec récompense » et un « Interstitiel ».
2. Remplace les identifiants de test :
   - `android/app/src/main/res/values/strings.xml` → `admob_app_id` (ton ID d'appli, avec un `~`)
   - `www/index.html`, tout en haut du script, bloc `ADS` → `rewarded`, `interstitial` (tes ID de blocs, avec un `/`) et `testing: false`
3. **Compte développeur Google Play** (play.google.com/console) : paiement unique de 25 $.
4. Créer une clé de signature et fabriquer le fichier `.aab` signé.
5. Fiche Play Store : icône 512 px (`store-icon-512.png`), captures d'écran, description, politique de confidentialité (obligatoire avec la pub).

Ne clique jamais sur tes propres pubs : Google peut fermer ton compte AdMob.

## Modifier le jeu

Tout le jeu est dans `www/index.html`. Après une modification, un nouvel envoi sur GitHub fabrique un nouvel APK.

Sur un ordinateur avec Node.js et Android Studio : `npm install`, `npm run sync`, puis ouvrir le dossier `android` dans Android Studio.
