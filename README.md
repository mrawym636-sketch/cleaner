# 🛡️ CyberClean Pro v4.6 — Nettoyeur & Antivirus léger (Tkinter)

CyberClean Pro est un utilitaire de nettoyage et d'analyse de fichiers simple et visuel. Il détecte les fichiers vides, signale les fichiers à extensions suspectes et permet la suppression en masse des fichiers vides. Interface thème "Dracula/Cyberpunk" implémentée en Tkinter (single-file : `cleaner.py`).

## Fonctionnalités principales
- Analyse récursive d'un dossier pour :
  - détecter les fichiers vides,
  - repérer les fichiers avec extensions suspectes (ex. .exe, .bat, .js, .msi, .dll, .py, .apk, ...).
- Suppression des fichiers vides (action irréversible, confirmation requise).
- Rapport d'analyse généré automatiquement (fichier texte horodaté).
- Copie du rapport dans le presse-papiers et ouverture du rapport.
- Progression, log et résumé (total analysé, vides, suspects, supprimés).
- Sons d'alerte / retour (sur Windows via winsound).
- Raccourcis clavier : Esc (annuler), Ctrl+C (copier), Ctrl+D (effacer), F1 (aide).

## Exigences
- Python 3.8+.
- Tkinter (inclus sur la plupart des distributions Python).
  - Sous Debian/Ubuntu : `sudo apt install python3-tk` si absent.
- (Optionnel) Windows : `winsound` est utilisé pour les sons (intégré sur Windows).

## Installation
Aucun paquet externe nécessaire. Cloner le dépôt ou copier `cleaner.py` dans un dossier, puis exécuter avec Python.

## Exécution
Depuis le dossier contenant `cleaner.py` :
```bash
python cleaner.py
```

## Utilisation
1. Choisir le dossier cible (ou parcourir avec le bouton).
2. Cliquer sur "🔍 Scanner" pour analyser.
3. Après analyse :
   - consulter le rapport dans la zone de log,
   - cliquer sur "🗑️ Supprimer les vides" pour effacer les fichiers vides (confirmation requise),
   - utiliser "📋 Copier" pour copier le rapport,
   - "📂 Rapport" ouvre le fichier rapport généré par l'application.

Raccourcis :
- Esc : annule un scan en cours.
- Ctrl+C : copie le rapport.
- Ctrl+D : efface les résultats.
- F1 : affiche l'aide intégrée.

## Rapports et paramètres
- Le rapport est enregistré automatiquement dans le répertoire du script avec le nom :
  `CyberClean_Report_JJ-MM-AAAA_HH-MM-SS.txt`
- Les paramètres persistants (dernier dossier choisi, son activé/désactivé) sont sauvegardés dans `cyberclean_settings.json` situé dans le même dossier que le script.

## Sécurité et bonnes pratiques
- La suppression est définitive : sauvegardez vos données importantes avant d'utiliser la suppression en masse.
- Vérifiez la liste des fichiers vides avant confirmation.
- Pour supprimer certains fichiers système ou protégés, exécutez l'application avec des privilèges administrateur si nécessaire.
- Les fichiers marqués "suspects" sont uniquement signalés par extension — ce n'est pas un verdict définitif. Examinez-les manuellement avant action.

## Limitations connues
- Détection basée sur l'extension (fausses alertes possibles).
- Fonction son disponible uniquement sur Windows via `winsound`.
- L'outil n'intègre pas d'analyse antivirus approfondie (pas d'analyse heuristique/scan de signatures) — il s'agit d'un utilitaire d'aide au nettoyage.

## Dépannage
- GUI ne démarre pas : vérifiez que Tkinter est installé.
- Permissions refusées lors de la suppression : exécutez en administrateur / fermez les applications qui verrouillent les fichiers.
- Aucun rapport : lancez d'abord un scan complet et relisez la zone de log.

## Contribuer
Améliorations et corrections de bugs bienvenues : ouvrir une issue ou proposer une PR. Idées :
- ajouter une quarantaine plutôt que suppression directe,
- prise en charge multi-plateforme des sons,
- règles d'exclusion / profils d'analyse,
- tests automatisés.

## Licence
MIT — ajoutez un fichier LICENSE si vous souhaitez inclure le texte complet.

## Auteur
Script : `cleaner.py` — adapté pour usage personnel / distribution. Ajoutez votre nom/contact si vous publiez le projet.
