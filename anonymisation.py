import re

def anonymiser_transcription(texte):
    # Téléphones
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)

    # Emails
    texte = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", texte)

    # Montants €
    texte = re.sub(r"\b\d[\d\s.,]*\s?€", "[MONTANT]", texte)

    # Dates simples (12/01/2024)
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)

    # Dates complexes (12 janvier 2024)
    texte = re.sub(r"\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|"
                   r"juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
                   "[DATE]", texte, flags=re.IGNORECASE)

    # IBAN français
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11,30}\b", "[IBAN]", texte)

    # Carte bancaire
    texte = re.sub(r"\b(?:\d{4}[\s-]?){3}\d{4}\b", "[CB]", texte)

    # Numéro de sécurité sociale FR
    texte = re.sub(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b", "[SECU]", texte)

    # Numéro SIRET
    texte = re.sub(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b", "[SIRET]", texte)

    # Identifiants internes (ID-12345)
    texte = re.sub(r"\bID[-_]?\d{3,10}\b", "[ID]", texte)

    # Noms de villes (liste simple)
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Lille", "Bordeaux", "Nice", "Nantes"]
    for ville in villes:
        texte = re.sub(rf"\b{ville}\b", "[VILLE]", texte, flags=re.IGNORECASE)
    # Noms de personnes (Prénom Nom)
    texte = re.sub(r"\b[A-Z][a-zàâäéèêëïîôöùûüç]+(?:[-\s][A-Z][a-zàâäéèêëïîôöùûüç]+)+\b", "[NOM]", texte)

    # Noms d’entreprises (liste simple)
    entreprises = ["Microsoft", "Google", "Amazon", "Orange", "Total", "EDF", "Renault"]
    for ent in entreprises:
        texte = re.sub(rf"\b{ent}\b", "[ENTREPRISE]", texte, flags=re.IGNORECASE)

    return texte
