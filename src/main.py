from parser_module import detecter_intention, normaliser_texte
from publisher_sensor import client, publish_commande, connecter_mqtt
from hotword import detecter_hotword
from stt_module import ecouter_commande
from TTS import speak
running = True

while running: 
    if detecter_hotword():
        speak("je vous écoute")
        commande = ecouter_commande()

        intent = detecter_intention(commande)

        print("Intention :", intent)

        if intent != "inconnue":
            publish_commande(commande,intent,intent)
            if intent == "on":
                speak("j'allume la lampe")

            elif intent == "off":
                speak("j'éteins la lampe")

            elif intent == "clignoter":
                speak("j'active le clignotement")

            elif intent == "mode nuit":
                speak("mode nuit activé")

            elif intent == "etat":
                #speak("je vérifie l'état de la lampe")
                pass
        else:
            speak("commande non reconnue")
    