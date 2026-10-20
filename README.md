# Projet IoT – IOT_JMVR

## Présentation
Ce dépôt regroupe les fichiers et travaux du projet IoT « TempHumiX » (IMT Nord Europe) :
création d'un capteur de température et d'humidité autour d'un Arduino UNO, d'abord en
simulation sous SimulIDE, puis sur un boîtier réel communiquant en MQTT.

## Objectifs
- Organiser les sources et les ressources du projet.
- Conserver l'historique des modifications avec Git.
- Synchroniser le travail avec GitHub.

## Organisation du dépôt
- `README.md` : présentation du projet.
- `.gitignore` : fichiers exclus du suivi Git.
- `mon_repertoire.docx` : compte-rendu du projet.
- `SIMULIDE/` : un sous-dossier par mini-projet, contenant le circuit (`.sim1`)
  et le code (`.ino`) portant le même nom.
  - `clignotement_led/` : LED sur la broche 2 clignotant à 1 Hz (500 ms allumée / 500 ms éteinte).
  - `bargraphe/` : chenillard sur un bargraphe de 10 LEDs (broches 3 à 12), pas de 100 ms.

## Prérequis
- Git
- Arduino IDE (carte « Arduino Uno »)
- SimulIDE 1.1.0-SR2

## Utilisation
1. Cloner le dépôt.
2. Ouvrir le `.ino` dans Arduino IDE, puis Sketch → Export Compiled Binary.
3. Ouvrir le `.sim1` dans SimulIDE, clic droit sur l'Uno → Load firmware → choisir le `.hex`.
4. Lancer la simulation (bouton marche).
