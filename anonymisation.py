import re

def anonymiser_transcription(texte):

    # --- Informations sensibles numériques ---
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)  # Téléphones
    texte = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", texte)  # Emails
    texte = re.sub(r"\b\d[\d\s.,]*\s?€", "[MONTANT]", texte)  # Montants €
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)  # Dates 12/01/2024
    texte = re.sub(
        r"\b\d{1,2}\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )  # Dates
