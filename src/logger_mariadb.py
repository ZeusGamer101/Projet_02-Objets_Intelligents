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

MQTT_PREFIX = "ahuntsic/aec-iot/b3/equipe_blondel_martin/piBM"
MQTT_TOPIC_FILTER = f"{MQTT_PREFIX}/#"

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
# 3) Fonctions utilitaires
# -----------------------------
def extract_device(topic:str) -> str:
    parts = topic.split("/")
    return parts[4] if len(parts) >= 5 else "unknown"

def is_telemetry(topic:str) -> bool:
    if "/sensors/" not in topic:
        return False
    if topic.endswith("/value"):
        return False
    return True

def classify_kind(topic:str) -> str:
    if "/cmd/" in topic:
        return "cmd"
    if "/state/" in topic:
        return "state"
    if "/status" in topic:
        return "status"
    return "other"

def try_parse_json(payload_text: str) -> Optional[dict[str,Any]]:
    try:
        obj = json.loads(payload_text)
        return obj if isinstance(obj,dict) else None
    except json.JSONDecodeError:
        return None

# -----------------------------
# 4) INSERT en BD (SQL param�tr�)
# -----------------------------
def insert_telemetry(ts_utc: str,device:str,topic:str,payload_text:str) -> None:
    obj = try_parse_json(payload_text)
    value = None
    unit = None

    if obj is not None:
        if "value" in obj:
            try:
                value = float(obj["value"])
            except(TypeError,ValueError):
                value = None
        if "unit" in obj and isinstance(obj["unit"],str):
            unit = obj["unit"][:16]

    sql = """
        INSERT INTO telemetry (device, topic, value, unit, ts_utc)
        VALUES (%s, %s, %s, %s, %s)
    """
    with db.cursor() as cur:
        cur.execute(sql,(device,topic,value,unit,ts_utc))

def insert_event(device:str,topic:str, payload_text: str, ts_utc: str) -> None:
    sql = """
        INSERT INTO events (device, topic, payload,ts_utc)
        VALUES (%s, %s, %s, %s)
    """
    with db.cursor() as cur:
        cur.execute(sql,(device,topic,payload_text,ts_utc))

# -----------------------------
# 5) Callbacks MQTT
# -----------------------------
def on_connect(client,_userdata,_flags,reason_code,properties=None):
    print(f"[CONNECT] reason_code={reason_code}")
    if reason_code == 0:
        client.subscribe(MQTT_TOPIC_FILTER,qos=0)
        print(f"[SUB] {MQTT_TOPIC_FILTER}")
    else:
        print("[ERROR] Connexion MQTT echouee.")

def on_message(_client,_userdate,msg: mqtt.MQTTMessage):
    topic = msg.topic
    payload_text= msg.payload.decode("utf-8", errors="replace")
    if topic.endswith("/value"):
        print(f"[SKIP] Ignored value topic: {topic}")
        return
    device = extract_device(topic)
    ts = utc_now_naive().isoformat() + "Z"

    try:
        if is_telemetry(topic):
            insert_telemetry(ts,device,topic,payload_text)
            print(f"[DB] telemetry <- {topic}")
        else:
            insert_event(device,topic,payload_text,ts)
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
# 6) D�marrage
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
