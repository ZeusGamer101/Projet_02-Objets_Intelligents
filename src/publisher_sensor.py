from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from gpiozero import CPUTemperature
import random

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

TOPIC_JSON = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/sensors/cpu"
TOPIC_VALUE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/sensors/cpu/value"

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

def read_temperature_cpu() -> float:
    cpu = CPUTemperature()
    return cpu.temperature



# ---------------------------------------------------------------------
# 3) Callbacks MQTT (�v�nementiel)
# ---------------------------------------------------------------------

connected = False # drapeau simple pour savoir si on est connect�

def on_connect(client, userdata, flags, reason_code, properties=None):
    global connected
    print("[CONNECT] reason_code={reason_code}")
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

# Connexion non bloquante + thread r�seau:
client.connect_async(BROKER_HOST,BROKER_PORT,keepalive=KEEPALIVE_S)
client.loop_start()

# ---------------------------------------------------------------------
# 5) Boucle principale (capteur -> publish)
# ---------------------------------------------------------------------
try:
    client.publish(TOPIC_ONLINE,"online",qos=QOS_STATUS,retain=True)

    while True:
        if not connected:
            print("[WAIT] en attente de connexion MQTT...")
            time.sleep(1.0)
            continue
    
        cpu_temp = read_temperature_cpu()

        payload = {
            "device_id": DEVICE,
            "sensor" : "CPU",
            "value" : cpu_temp,
            "unit" : "C",
            "ts" : datetime.now(timezone.utc).isoformat()
        }

        # 1) Message JSON (contrat "riche")
        client.publish(TOPIC_JSON,json.dumps(payload),qos=QOS_SENSOR,retain=False)

        # 2) Valeur simple (facile pour dashboards)
        client.publish(TOPIC_VALUE,str(cpu_temp),qos=QOS_SENSOR,retain=False)

        print(f"[PUB] {TOPIC_JSON} -> {payload}")
        time.sleep(PUBLISH_PERIOD_S)

except KeyboardInterrupt:
    print("\n[STOP] arr�t demand� (Ctrl+C)")
finally:
    client.publish(TOPIC_ONLINE,"offline",qos=QOS_STATUS,retain=True)
    client.loop_stop()
    client.disconnect()
