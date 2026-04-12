from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

import pymysql
import paho.mqtt.client as mqtt


# -----------------------------
# 1) Param�tres MQTT
# -----------------------------

MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_KEEPALIVE = 60

TEAM = "equipe_blondel_martin"
DEVICE = "piBM"

TOPIC_STATE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/led/state"

MQTT_CLIENT_ID = "b3-logger-demo-pi01"

# -----------------------------
# 2) Param�tres MariaDB
# -----------------------------
DB_HOST = "localhost"
DB_USER = "iot"
DB_PASSWORD = "iot"
DB_NAME = "iot_p1"


def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def db_connect() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True,
        charset="utf8mb4",
    )

# Connexion DB globale (simple)
db = db_connect()


# -----------------------------
# 3) INSERT en BD (SQL param�tr�)
# -----------------------------

def parse_JSON(payload_text: str):
    try:
        obj = json.loads(payload_text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None

def insert_event(payload_text, ts_utc) -> None:
    sql = """
        INSERT INTO events (commande_texte, intention_detectee, resultat,ts_utc)
        VALUES (%s, %s, %s, %s)
    """
    commande_texte = None
    intention_detectee = None
    resultat = None

    obj = parse_JSON(payload_text)

    print(f"Objet {obj}")

    if obj is not None:
        if "Texte reconnu" in obj:
            try:
                commande_texte = obj["Texte reconnu"]
            except (TypeError, ValueError):
                commande_texte = None
        if "Intention" in obj:
            try:
                intention_detectee = obj["Intention"]
            except (TypeError, ValueError):
                intention_detectee = None
        if "[MQTT] envoyé" in obj:
            try:
                resultat = obj["[MQTT] envoyé"]
            except (TypeError, ValueError):
                resultat = None

        

    with db.cursor() as cur:
        cur.execute(sql,(commande_texte,intention_detectee, resultat,ts_utc))

# -----------------------------
# 4) Callbacks MQTT
# -----------------------------
def on_connect(client,_userdata,_flags,reason_code,properties=None):
    print(f"[CONNECT] reason_code={reason_code}")
    if reason_code == 0:
        client.subscribe(TOPIC_STATE,qos=0)
        print(f"[SUB] {TOPIC_STATE}")
    else:
        print("[ERROR] Connexion MQTT echouee.")

def on_message(_client,_userdate,msg: mqtt.MQTTMessage):
    topic = msg.topic
    payload_text = msg.payload.decode("utf-8", errors="replace")
    ts = utc_now_naive()

    try:

        insert_event(payload_text, ts)
        print(f"[DB] event <- {topic}")

    except pymysql.MySQLError as e:
        print(f"[DB-ERROR] {e} -> reconnexion")
        global db
        try:
            db.close()
        except Exception:
            pass
        db = db_connect()


def on_disconnect(_client,_userdate,reason_code,propreties=None):
    print(f"[DISCONNECT] reason_code={reason_code}")


# -----------------------------
# 5) D�marrage
# -----------------------------
client = mqtt.Client(client_id=MQTT_CLIENT_ID,protocol=mqtt.MQTTv311)
client.on_connect = on_connect

client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTT_BROKER_HOST,MQTT_BROKER_PORT,keepalive=MQTT_KEEPALIVE)

print("[INFO] Logger démarré. CTRL+C pour arreter.")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n[STOP] arret demander")
finally:
    try:
        db.close()
    except Exception:
        pass
    client.disconnect()
