# README - TP2 du cours de *Développement d'objets intelligents*

## 1. Description du projet
Ce projet d’internet des objets consiste à créer un système de lampe intelligente qui permet à un utilisateur de piloter une LED avec des commandes vocales. Le système doit aussi être en mesure de faire un retour vocal pour confirmer une action ou signaler une erreur. Le système doit transmettre des commandes par le biais d’un broker. Finalement, les évènements doivent être enregistrer dans une base de données.

## 2. Matériel utilisé
- Raspberry PI
- DEL rouge
- Resistance de 220 ohms
- Celullaire avec MQTT Dash ou une autre application d'objets intelligents
- Écouteurs USB avec microphone

## 3. Dépendances:
- paho-mqtt
- gpiozero
- PyMySQL
- nltk
- speech_recognition

## 4. Procédure d'installatiom
**Étape 1:** Installer Mosquitto (broker) et les clients avec la ligne de commande sudo apt install -y mosquitto mosquitto-clients
**Étape 2:** Démarrer le service avec la ligne de commande sudo systemctl enable --now mosquitto
**Étape 3:** Vérifier que le servoce tourne avec la ligne de commande systemctl status mosquitto --no-pager
**Étape 4:** Vérifier le port MQTT avec la ligne de commande sudo ss -lntp | grep 1883
**Étape 5:** Importer les fichiers à partir de GitHub et les mettre dans un dossier
**Étape 6:** Créer un venv dans le dossier où se trouvent les fichiers
**Étape 7:** Dans un terminal python, écrire la commande pip install -r requirement.txt
**Étape 8**: Trouver le bon index des écouteurs

## 5. Procédures de lancement

## 6. Commandes supportées

## 7. Structure du projet
