import subprocess

def speak(text, langue="fr", debit=150):
    subprocess.run(["espeak-ng", "-v", langue, "-s", str(debit), text])
