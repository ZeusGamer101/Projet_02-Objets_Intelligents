from __future__ import annotations

import json
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

#---------------------------------------------------------------------
# 1) Param�tres MQTT 
# ---------------------------------------------------------------------

BROKER_HOST = "localhost" 
BROKER_PORT = 1883 
KEEPALIVE_S = 60 

TEAM = "equipe_blondel_martin"
DEVICE = "piBM"

CLIENT_ID = "b3-pub-piBM-led"

TOPIC_CMD = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/led/cmd"

# Statut "online/offline" pratique en IoT (peut �tre affich� aussi dans un dashboard)
TOPIC_ONLINE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/status/online"

# QoS:
# - capteurs fr�quents -> QoS 0 (rapide, pas d'ack)
# - �tats/commandes -> souvent QoS 1 (plus fiable)

QOS_SENSOR = 0
QOS_STATUS = 1
PUBLISH_PERIOD_S = 2.0

# ---------------------------------------------------------------------
# 2) Lecture capteur (� brancher sur VOTRE code du cours pr�c�dent)
# ---------------------------------------------------------------------
def publish_commande(state):
    client = mqtt.Client()
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    payload = {"state": state}

    client.publish(TOPIC_CMD, json.dumps(payload), qos=1)
    print(f"[MQTT] envoyé : {payload}")

    time.sleep(1)

    client.loop_stop()
    client.disconnect()

# ---------------------------------------------------------------------
# 3) Callbacks MQTT (�v�nementiel)
# ---------------------------------------------------------------------
def connecter_mqtt():
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=KEEPALIVE_S)
    client.loop_start()

connected = False # drapeau simple pour savoir si on est connect�

def on_connect(client, userdata, flags, reason_code, properties=None):
    global connected
    print(f"[CONNECT] reason_code={reason_code}")
    connected = (reason_code == 0)



def on_disconnect(client,userdata,reason_code,properties=None):
    global connected
    print(f"[DISCONNECT] reason_code={reason_code}")
    connected = False

# ---------------------------------------------------------------------
# 4) Cr�ation du client + LWT + connexion
# ---------------------------------------------------------------------

client = mqtt.Client(
    client_id=CLIENT_ID,
    protocol=mqtt.MQTTv311
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# LWT (Last Will): si le Pi meurt sans se d�connecter proprement,
# le broker publiera "offline" sur TOPIC_ONLINE.

client.will_set(
    topic=TOPIC_ONLINE,
    payload="offline",
    qos=QOS_STATUS,
    retain=True
)

# Option utile en IoT: d�lai de reconnexion progressif (�vite spam r�seau)
# (On garde �a simple; on le renforcera dans les prochaines s�ances)
client.reconnect_delay_set(min_delay=1,max_delay=30)

publish_commande("mode nuit")