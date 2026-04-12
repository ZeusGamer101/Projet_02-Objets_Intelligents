# README - TP2 du cours de *Développement d'objets intelligents*

## 1. Description du projet
Ce projet d’internet des objets consiste à créer un système de lampe intelligente qui permet à un utilisateur de piloter une LED avec des commandes vocales. Le système doit aussi être en mesure de faire un retour vocal pour confirmer une action ou signaler une erreur. Le système doit transmettre des commandes par le biais d’un broker. Finalement, les évènements doivent être enregistrer dans une base de données.

## 2. Matériel utilisé
- Raspberry PI <br>
- DEL rouge <br>
- Resistance de 220 ohms <br>
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
**Étape 6:** Créer un environnement virtuel (venv) dans le dossier où se trouvent les fichiers en insérant cette ligne de commande dans un terminal python: *python3 -m venv .venv* <br>
**Éatpe 7**: Activer le venv en insérant cette commande dans le même terminal: *source .venv/bin/activate*
**Étape 7:** Dans un terminal python, écrire la commande pip install -r requirement.txt <br>
**Étape 8:** À l'aide des commandes dans le fichier schéma.sql, créer la table events
**Étape 9:** Trouver le bon index pour les écouteurs et le stocker dans la variable MIC_INDEX (publisher.py) <br>

## 5. Procédure de lancement
**Étape 1**: Dans un premier terminal, lancer le subscriber en insérant la ligne de commande: *python src/subscriber_led.py*  <br>
**Étape 2**: Dans un deuxième terminal, lancer le logger en insérant la ligne de commande: *python src/logger_mariadb.py* <br>
**Étape 3**: Dans un troisième terminal, lancer le main avec en insérant la ligne de commande: *python src/main_mariadb.py* <br>
**Étape 4**: Après que le systèm soit calibré, dire le hotword (assistant) pour activer le système<br>

## 6. Commandes supportées
Voici des exemples dec ommandes supportées et les actions qu'elles produistent sur le système: <br>
### Allumage LED:
- Allume la (lampe/LED)<br>
- Allumer la (lampe/LED)<br>
- Met en marche la (lampe/LED)<br>

### Extinction LED:
- Éteint la (lampe/LED)<br>
- Ferme la (lampe/LED)<br>
- Arrête la (lampe/LED)<br>
- Stop la (lampe/LED)<br>

### Clignotement LED:
- Clignote la lampe (lampe/LED)<br>
- Clignoter la lampe (lampe/LED)<br>
- Fait clignoter la lampe(lampe/LED)<br>

### Mode nuit:
- Active le mode (nuit/echo/silence)<br>
- Met le mode (nuit/echo/silence)<br>
- Mode (nuit/echo/silence)<br>

### Donner l'état:
- Donne moi l'état<br>
- Quel est l'état<br>
  
## 7. Structure du projet
- src<br>
  - publisher_sensor.py <br>
  - subscriber_led.py <br>
  - logger_mariadb.py <br>
  - parser_module.py <br>
  - stt_module.py <br>
  - TTS.py <br>
  - hotword.py <br>
  - main.py
- db<br>
  - queries.sql <br>
  - schema.sql <br>


