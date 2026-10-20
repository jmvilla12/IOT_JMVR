# Projet IoT – IOT_JMVR

## Présentation
Ce dépôt regroupe les fichiers et travaux du projet IoT « TempHumiX » :
capteur de température et d'humidité sur Arduino UNO (IMT Nord Europe).

## Objectifs
- Organiser les sources et les ressources du projet.
- Conserver l'historique des modifications avec Git.
- Synchroniser le travail avec GitHub.

## Organisation du dépôt
- `README.md` : présentation du projet.
- `.gitignore` : fichiers exclus du suivi Git.
- `SIMULIDE/` : un sous-dossier par mini-projet (`.sim1` + `.ino` du même nom).
  - `clignotement_led/` : clignotement d'une LED sur la broche 2 (500 ms).
- `mon_repertoire.docx` : compte-rendu du projet.

## Prérequis
- Git, Arduino IDE, SimulIDE 1.1.0-SR2.

## Utilisation
1. Cloner le dépôt.
2. Ouvrir le `.ino` dans Arduino IDE → Sketch → Export Compiled Binary.
3. Ouvrir le `.sim1` dans SimulIDE, clic droit sur l'Uno → Load firmware → charger le `.hex`.
4. Lancer la simulation.