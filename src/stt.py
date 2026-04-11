import speech_recognition as sr
import subprocess

r = sr.Recognizer()

# R�glages de base test�s en pratique
r.dynamic_energy_threshold = False

r.energy_threshold = 1200
r.pause_threshold = 0.8

MIC_INDEX = 1 # Remplacez 1 par l'index r�el de votre micro
def parler(texte):
    subprocess.run(["espeak-ng", "-v", "fr", "-s", "150", texte])

with sr.Microphone(device_index=MIC_INDEX) as source:
    print("Ne parlez pas pendant 2 secondes...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Seuil �nergie calibr� =", r.energy_threshold)
    print("Parlez maintenant...")

    try:
        audio = r.listen(source, timeout=8, phrase_time_limit=6)
    except sr.WaitTimeoutError:
        print("Temps �coul� : aucune voix d�tect�e")
        raise SystemExit

try:
    texte = r.recognize_google(audio, language="fr-FR")
    print("Texte reconnu :", texte)
    parler(texte)
except sr.UnknownValueError:
    print("Le syst�me n'a pas compris")
except sr.RequestError as e:
    print("Erreur du service STT :", e)
    