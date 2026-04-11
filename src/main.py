from parser_module import detecter_intention, normaliser_texte
from publisher_sensor import client, publish_commande, connecter_mqtt
from hotword import detecter_hotword
from stt_module import ecouter_commande
from TTS import speak

if detecter_hotword():
    speak("je vous écoute")
    commande = ecouter_commande()

    intent = detecter_intention(commande)

    print("Intention :", intent)

    if intent != "inconnue":
        publish_commande(intent)
        if intent == "on":
            speak("j'allume la lampe")

        elif intent == "off":
            speak("j'éteins la lampe")

        elif intent == "clignoter":
            speak("j'active le clignotement")

        elif intent == "mode nuit":
            speak("mode nuit activ�")
    else:
        speak("commande non reconnue")