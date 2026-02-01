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
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11
    
