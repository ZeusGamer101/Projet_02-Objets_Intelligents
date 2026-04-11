import speech_recognition as sr

HOTWORD = "assistant"

def detecter_hotword():

    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 1200
    r.pause_threshold = 0.8

    MIC_INDEX = 1 

    with sr.Microphone(device_index=MIC_INDEX) as source:
        print("Ne parlez pas pendant 2 secondes...")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Dites le mot d'activation...")
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            print("Temps �coul� : aucune voix d�tect�e")
            raise SystemExit
        
    try:
        texte = r.recognize_google(audio, language="fr-FR").lower()
        print("Texte capt� :", texte)
        if HOTWORD in texte:
            print("Hot-word detecte")
            return True
        else:
            print("Hot-Word non detecte")
            return False
    except sr.UnknownValueError:
        print("Le syst�me n'a pas compris")
        return False
    except sr.RequestError as e:
        print("Erreur du service STT :", e)
        return False
    
detecter_hotword()