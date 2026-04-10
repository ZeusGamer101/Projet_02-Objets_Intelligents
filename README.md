# README - TP2 du cours de *Développement d'objets intelligents*

## 1. Description du projet
Ce projet d’internet des objets consiste à créer un système de lampe intelligente qui permet à un utilisateur de piloter une LED avec des commandes vocales. Le système doit aussi être en mesure de faire un retour vocal pour confirmer une action ou signaler une erreur. Le système doit transmettre des commandes par le biais d’un broker. Finalement, les évènements doivent être enregistrer dans une base de données.

## 2. Matériel utilisé
- Raspberry PI <br>
- DEL rouge <br>
- Resistance de 220 ohms <br>
- Celullaire avec MQTT Dash ou une autre application d'objets intelligents <br>
- Écouteurs USB avec microphone <br>

## 3. Dépendances
- paho-mqtt <br>
- gpiozero <br>
- PyMySQL <br>
- nltk <br>
- speech_recognition <br>

## 4. Procédure d'installation
**Étape 1:** Installer Mosquitto (broker) et les clients avec la ligne de commande sudo apt install -y mosquitto mosquitto-clients <br>
**Étape 2:** Démarrer le service avec la ligne de commande sudo systemctl enable --now mosquitto <br>
**Étape 3:** Vérifier que le servoce tourne avec la ligne de commande systemctl status mosquitto --no-pager <br>
**Étape 4:** Vérifier le port MQTT avec la ligne de commande sudo ss -lntp | grep 1883 <br>
**Étape 5:** Importer les fichiers à partir de GitHub et les mettre dans un dossier <br>
**Étape 6:** Créer un venv dans le dossier où se trouvent les fichiers <br>
**Étape 7:** Dans un terminal python, écrire la commande pip install -r requirement.txt <br>
**Étape 8**: Trouver le bon index pour les écouteurs et le stocker dans la variable MIC_INDEX (publisher.py) <br>

## 5. Procédures de lancement
**Étape 1**: Lancer le subscriber <br>
**Étape 2**: Lancer le publisher <br>
**Étape 3** Lancer le logger <br>

## 6. Commandes supportées
Voici des exemples dec ommandes supportées et les actions qu'elles produistent sur le système: <br>
- **allume la lampe**: la DEL s'allume <br>
- **éteint la lampe**: la DEL s'éteint <br>
- **fais clignoter la lampe**: la DEL clignote <br>
- **donne-moi l'état**: le système vocal dit quel est l'état actuel de la lampe <br>
- **active le mode nuit**: la DEL clignote lentement <br>

## 7. Structure du projet
src
-- publisher.py
-- subscriber.py
-- logger_mariadb.py <br>
<br>
db
-- queries.sql
-- schema.sql


