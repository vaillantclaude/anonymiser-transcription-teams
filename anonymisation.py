import re

def anonymiser_transcription(texte):

    # Téléphones FR
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)

    # Emails
    texte = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", texte)

    # Montants €
    texte = re.sub(r"\b\d[\d\s.,]*\s?€", "[MONTANT]", texte)

    # Dates simples
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)

    # Dates complexes
    texte = re.sub(
        r"\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )

    # Heures (14h30, 9h, 09:45)
    texte = re.sub(r"\b\d{1,2}[:h]\d{0,2}\b", "[HEURE]", texte)

    # IBAN
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11,30}\b", "[IBAN]", texte)

    # Carte bancaire
    texte = re.sub(r"\b(?:\d{4}[\s-]?){3}\d{4}\b", "[CB]", texte)

    # Sécurité sociale
    texte = re.sub(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b", "[SECU]", texte)

    # SIRET
    texte = re.sub(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b", "[SIRET]", texte)

    # Numéros de dossier (1 à 10 chiffres)
    texte = re.sub(
        r"\b(?:dossier|dos|d)[-_ ]?\d{1,10}\b",
        "[DOSSIER]",
        texte,
        flags=re.IGNORECASE
    )

    # Identifiants internes
    texte = re.sub(r"\bID[-_]?\d{3,10}\b", "[ID]", texte)

    # Initiales (C.V., J.D., M.L.)
    texte = re.sub(r"\b[A-Z]\.[A-Z]\.\b", "[INITIALES]", texte)

    # Villes
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Lille", "Bordeaux", "Nice", "Nantes"]
    for ville in villes:
        texte = re.sub(rf"\b{ville}\b", "[VILLE]", texte, flags=re.IGNORECASE)

    # Noms de personnes (Prénom + Nom)
    texte = re.sub(
        r"\b[A-Z][a-zàâäéèêëïîôöùûüç]+(?:[-\s][A-Z][a-zàâäéèêëïîôöùûüç]+)+\b",
        "[NOM]", texte
    )

    # Prénoms automatiques (avec accents)
    texte = re.sub(
        r"\b[A-Z][a-zàâäéèêëïîôöùûüç]{2,}\b",
        "[PRENOM]",
        texte
    )

    # Noms en MAJUSCULES
    texte = re.sub(r"\b[A-Z]{2,}\b", "[NOM]", texte)

    # Entreprises
    entreprises = ["Microsoft", "Google", "Amazon", "Orange", "Total", "EDF", "Renault"]
    for ent in entreprises:
        texte = re.sub(rf"\b{ent}\b", "[ENTREPRISE]", texte, flags=re.IGNORECASE)

    # Adresses postales (numéro + rue)
    texte = re.sub(
        r"\b\d{1,4}\s+(rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|allée|place)\s+[A-Za-zÀ-ÿ0-9\s'-]+\b",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )

    # Codes postaux FR
    texte = re.sub(r"\b\d{5}\b", "[CP]", texte)

    return texte
