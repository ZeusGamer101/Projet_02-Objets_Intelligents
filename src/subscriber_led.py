import json
from typing import Any
import paho.mqtt.client as mqtt
from gpiozero import LED
from typing import Any, Optional

#===================================
# Paramètres MQTT
#===================================
BROKER_HOST = "localhost" # Dans notre cas, localhost représente le raspberry PI de Blondel
BROKER_PORT = 1883
KEEPALIVE_S = 60

TEAM = "equipe_blondel_martin"
DEVICE = "piBM"

CLIENT_ID = "b3-sub-piBM-led"

LED_PIN_BCM = 17 # Pin sur laquelle la LED est branchée
led = LED(LED_PIN_BCM)

TOPIC_CMD = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/led/cmd"
TOPIC_STATE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/led/state"

QOS_CMD = 1


#===================================
# Fonctions utilitaires LED
#===================================
def publish_led_state(client: mqtt.Client) -> None:
    """ 
    Cette foction sert à publier l'état actuel de la LED sur TOPIC_STATE
    Étant donnée que retain = TRue, le broker va garder en mémoire le dernier état connu
    """
    state = "on" if led.is_lit else "off"
    client.publish(TOPIC_STATE, state, qos=1, retain=True)
    print(f"[STATE] {TOPIC_STATE} -> {state}")


def parse_command(payload_text: str) -> str | None:
    """
    Cette fonction sert à décodé le message JSON qui contient la commande pour la LED
    La fonction va normaliser les données. Le programme va prendre toutes les écriture possibles de commandes pour allumer et
    étindre la LED et va les convertir en "on" ou "off". Si la commande est invalide, la fonction retourne "None"
    Cela facilite la lecture et l'interpétation des commandes par le programme
    """

    try:
        data: dict[str, Any] = json.loads(payload_text)
    except json.JSONDecodeError: # Gestion d'exception: la commande n'est pas un fromat JSON
        return None
    
    # Normalisation des données
    if "state" in data and isinstance(data["state"], str):
        s = data["state"].strip().lower()
        if s in ("on", "off"):
            return s
    
    if "value" in data:
        v = data["value"]
        if v in (1, True, "1", "on", "ON"): # Formats accepté
            return "on"
        if v in (0, False, "0", "off", "OFF"):
            return "off"

        
#===================================
# Callback MQTT
#===================================
def on_connect(client, userdata, flags, reason_code, properties=None):
    """
    Cette fonction en est une de type callback qui va être appellé à chauqe fois que le client se connect au broker
    Parmi les paramètre, il y client qui est l'objet de la classe externe MQTT client et reaosn code qui dnne le résultat de la connection
    (reason code de 0 veut dire que la connection entre le client et le broker s'est bien faite)

    """
    print(f"[CONNECT] reason_code={reason_code}")
    if reason_code == 0:

        client.subscribe(TOPIC_CMD, qos=QOS_CMD) # Quand la connection a été établie, le client s'abonne à TOPIC_CMD
        print(f"[SUB] {TOPIC_CMD} (qos={QOS_CMD})")

        publish_led_state(client) # Ici, on publie l'état de la LED au moment de la connection
    
    else:
        print("[ERROR] Connexion MQTT échouée.")
        
def on_message(client, userdata, msg: mqtt.MQTTMessage):
    """
    Cette fonction est appellée à chaque fois que le client va recevoir un message.
    Le programme appelle la fonction pour parser le JSON et regarde le résultat retourné par la fonction
    S'il y avait une erreur au niveau du JSON de commande, un message d'erreur va être affiché
    Si le retour de parse_command est on, la LED s'allume. Si le retour est off, la LED s'éteint

    """

    payload_text = msg.payload.decode("utf-8", errors="replace")
    print(f"[MSG] topic={msg.topic} qos={msg.qos} retain={msg.retain} payload={payload_text}")

    command = parse_command(payload_text)
    if command is None:
        print("[WARN] Commande invalide (JSON attendu). Ignorée.")
        return
    
    if command == "on":
        led.on()
    else:
        led.off()
    publish_led_state(client)

def on_disconnect(client, userdata, reason_code, properties=None):
    """
    Cette fonction est appellée quand le client se déconnecte. Lors de la déconnection, le programme éteint la LED
    
    """
    print(f"[DISCONNECT] reason_code={reason_code}")
    led.off()

#===================================
# Démarrage du client MQTT
#===================================
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.reconnect_delay_set(min_delay=1, max_delay=30)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=KEEPALIVE_S)
client.loop_forever()