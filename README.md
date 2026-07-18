# 🛡️ CyberClean 

**Nettoyeur de fichiers vides + Antivirus léger**  
Interface graphique Tkinter – Design Dracula/Cyberpunk

---

## 📖 Présentation

CyberClean Pro est un outil de maintenance système qui vous permet d’**analyser** un dossier (et ses sous-dossiers) pour :

- 🔍 Détecter les **fichiers vides** (0 octet)
- ⚠️ Identifier les **extensions suspectes** (exécutables, scripts, etc.)
- 🗑️ Supprimer en masse les fichiers vides
- 📊 Générer un **rapport détaillé** en texte

L’interface est intuitive, avec des couleurs sombres et des retours sonores (sur Windows) pour une expérience moderne.

---

## ✨ Fonctionnalités

- **Scan rapide** : parcourt récursivement le dossier choisi
- **Détection des vides** : affiche tous les fichiers de taille 0
- **Détection des fichiers suspects** : extensions connues (`.exe`, `.bat`, `.js`, etc.)
- **Suppression sécurisée** : confirmation avant la suppression définitive
- **Rapport automatique** : sauvegardé dans le dossier du script
- **Copie du rapport** dans le presse-papiers (Ctrl+C)
- **Raccourcis clavier** pour une utilisation efficace
- **Sons** (activation/désactivation)
- **Personnalisation** : sauvegarde du dernier dossier et de l’état du son

---

## 🖥️ Prérequis

- Python 3.6 ou supérieur
- Bibliothèques :
  - `tkinter` (inclus avec Python sous Windows)
  - `os`, `sys`, `json`, `threading`, `datetime` (modules standard)

> **Remarque** : Les sons (`winsound`) ne fonctionnent que sous Windows. Sur d’autres systèmes, ils sont ignorés sans erreur.

---

## 📦 Installation

1. **Téléchargez** le script `cleaner.py` (ou le dossier complet).
2. Assurez-vous que Python est installé.
3. Ouvrez un terminal dans le dossier du script et exécutez :

```bash
python cleaner.py
