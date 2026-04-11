import re
from nltk.tokenize import word_tokenize
import time



def normaliser_texte(texte):
    """
    Met le texte en minuscules et enl�ve les espaces inutiles.
    """
    return texte.lower().strip()

def extraire_allumer(texte):
    motif = r"\b(allume|allumer|mets?.*marche)\b"
    resultat = re.search(motif, texte)
    if resultat:
        return "on"
    
    return None

def extraire_eteindre(texte):
    motif = r"\b(éteins|eteins|éteint|eteint|ferme|arrête|arrete|stop)\b"
    resultat = re.search(motif, texte)
    if resultat:
        return "off"
    
    return None

def extraire_clignoter(texte):
    motif = r"\b(clignote|clignoter|fais\s+clignoter)\b"
    resultat = re.search(motif, texte)
    if resultat:
        return "clignoter"
    
    return None


def extraire_mode_nuit(texte):
    """
    Cherche un mode dans le texte.
    Retourne le mode trouv�, sinon None.
    """
    motif = r"(?:active\s+le\s+mode|mets\s+le\s+mode|mode)\s+(nuit|eco|silence)"
    resultat = re.search(motif, texte)
    if resultat:
        return "mode nuit"
    
    return None

def extraire_etat(texte):
    """
    Cherche un mode dans le texte.
    Retourne le mode trouv�, sinon None.
    """
    motif = r"\b(état|etat|donne[-\s]?moi.*état|quel est l'état)\b"
    resultat = re.search(motif, texte)
    if resultat:
        return "état"
    
    return None

def detecter_intention(texte):
    """
    D�termine une intention simple � partir de mots-cl�s
    et des informations extraites.
    """
    tokens = word_tokenize(texte, language="french")
    tokens = [mot.lower() for mot in tokens]

    # Si le texte contient un mode, on consid�re que l'intention est changer_mode
    if extraire_mode_nuit(texte) is not None:
        return "mode nuit"
    
    if extraire_clignoter(texte) is not None:
        return "clignoter"
    
    # Si le texte contient une vitesse, on consid�re que l'intention est changer_vitess
    if extraire_allumer(texte) is not None:
        return "on"
    
    # Commande de d�marrage
    if extraire_eteindre(texte) is not None:
        return "off"
    
    # Commande d'arr�t
    if extraire_etat(texte) is not None:
        return "etat"
    
    return "inconnue"

# Exemple de test
"""
commande = "active mode nuit"
commande = normaliser_texte(commande)

intent = detecter_intention(commande)


print("Commande :", commande)
print("Intention :", intent)


message = {
    "texte" : commande,
    "state" : intent
}

print(message)
"""