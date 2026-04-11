import speech_recognition as sr
import subprocess

#print(sr.Microphone.list_working_microphones())

def speak(text, langue="fr", debit=100):
    subprocess.run(["espeak-ng", "-v", langue, "-s", str(debit), text])

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index, name)

def ecouter_commande():
    r = sr.Recognizer()

    # R�glages de base test�s en pratique
    r.dynamic_energy_threshold = False
    r.energy_threshold = 1200
    r.pause_threshold = 0.8

    MIC_INDEX = 1 

    with sr.Microphone(device_index=MIC_INDEX) as source:
        print("Ne parlez pas pendant 2 secondes...")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Seuil �nergie calibr� =", r.energy_threshold)
        print("Parlez maintenant...")

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("Temps �coul� : aucune voix d�tect�e")
            speak("Vous devez parler")
            raise SystemExit
        
    try:
        texte = r.recognize_google(audio, language="fr-FR")
        print("Texte reconnu :", texte)
        return texte
    except sr.UnknownValueError:
        print("Le syst�me n'a pas compris")
        speak("Je ne comprends pas ce que tu dis")
        return None
    except sr.RequestError as e:
        print("Erreur du service STT :", e)
        return None

ecouter_commande()