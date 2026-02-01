import re

def anonymiser_transcription(texte):

    # --- Adresses postales (doit passer AVANT les villes) ---
    texte = re.sub(
        r"\b\d{1,4}\s+(rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|allée|place)\s+[A-Za-zÀ-ÿ0-9\s'-]+\b",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )

    # --- Codes postaux ---
    texte = re.sub(r"\b\d{5}\b", "[CP]", texte)

    # --- Téléphones ---
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)

    # --- Emails ---
    texte = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", texte)

    # --- Montants ---
    texte = re.sub(r"\b\d[\d\s.,]*\s?€", "[MONTANT]", texte)

    # --- Dates ---
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(
        r"\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )

    # --- Heures ---
    texte = re.sub(r"\b\d{1,2}[:h]\d{0,2}\b", "[HEURE]", texte)

    # --- Numéros de dossier (1 à 10 chiffres) ---
    texte = re.sub(
        r"\b(?:dossier|dos|d)[-_ ]?\d{1,10}\b",
        "[DOSSIER]", texte, flags=re.IGNORECASE
    )

    # --- Initiales (C.V., M.L., etc.) ---
    texte = re.sub(r"\b[A-Z]\.[A-Z]\.?", "[INITIALES]", texte)

    # --- IBAN, CB, SECU, SIRET ---
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11,30}\b", "[IBAN]", texte)
    texte = re.sub(r"\b(?:\d{4}[\s-]?){3}\d{4}\b", "[CB]", texte)
    texte = re.sub(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b", "[SECU]", texte)
    texte = re.sub(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b", "[SIRET]", texte)

    # --- Noms complets (Prénom Nom) ---
    texte = re.sub(
        r"\b[A-Z][a-zàâäéèêëïîôöùûüç]+(?:[-\s][A-Z][a-zàâäéèêëïîôöùûüç]+)+\b",
        "[NOM]", texte
    )

    # --- Prénoms automatiques ---
    texte = re.sub(
        r"\b[A-Z][a-zàâäéèêëïîôöùûüç]{2,}\b",
        "[PRENOM]",
        texte
    )

    # --- Noms en MAJUSCULES ---
    texte = re.sub(r"\b[A-Z]{2,}\b", "[NOM]", texte)

    # --- Entreprises ---
    entreprises = ["Microsoft", "Google", "Amazon", "Orange", "Total", "EDF", "Renault"]
    for ent in entreprises:
        texte = re.sub(rf"\b{ent}\b", "[ENTREPRISE]", texte, flags=re.IGNORECASE)

    # --- Villes ---
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Lille", "Bordeaux", "Nice", "Nantes"]
    for ville in villes:
        texte = re.sub(rf"\b{ville}\b", "[VILLE]", texte, flags=re.IGNORECASE)

    return texte
