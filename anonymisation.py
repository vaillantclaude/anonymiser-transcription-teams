import re

def anonymiser_transcription(texte):
    """
    Anonymise une transcription en masquant les données sensibles.
    Optimisé pour réduire les faux positifs.
    """
    
    # ==========================================
    # 1. DONNÉES STRUCTURÉES (en premier)
    # ==========================================
    
    # IBAN français
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11,30}\b", "[IBAN]", texte)
    
    # Numéro de carte bancaire (16 chiffres)
    texte = re.sub(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[CB]", texte)
    
    # Numéro de sécurité sociale (15 chiffres : 1 ou 2 + 12 chiffres + 2 chiffres clé)
    texte = re.sub(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b", "[SECU]", texte)
    
    # SIRET (14 chiffres)
    texte = re.sub(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b", "[SIRET]", texte)
    
    # ==========================================
    # 2. TÉLÉPHONES FRANÇAIS (formats multiples)
    # ==========================================
    
    # Format international : +33 X XX XX XX XX (avec espaces, points ou tirets)
    texte = re.sub(
        r"\b\+33[\s.-]?[1-9](?:[\s.-]?\d{2}){4}\b",
        "[TEL]", texte
    )
    
    # Format international sans séparateurs : +33XXXXXXXXX
    texte = re.sub(r"\b\+33[1-9]\d{8}\b", "[TEL]", texte)
    
    # Format national : 0X XX XX XX XX (X entre 1 et 9)
    texte = re.sub(
        r"\b0[1-9](?:[\s.-]?\d{2}){4}\b",
        "[TEL]", texte
    )
    
    # Format national sans séparateurs : 0XXXXXXXXX
    texte = re.sub(r"\b0[1-9]\d{8}\b", "[TEL]", texte)
    
    # Numéros courts spéciaux (3 à 4 chiffres) - optionnel selon votre besoin
    # texte = re.sub(r"\b(?:3\d{3}|1\d{3})\b", "[TEL_COURT]", texte)
    
    # ==========================================
    # 3. EMAILS
    # ==========================================
    
    texte = re.sub(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "[EMAIL]", texte
    )
    
    # ==========================================
    # 4. ADRESSES POSTALES (avant codes postaux)
    # ==========================================
    
    # Adresses complètes
    texte = re.sub(
        r"\b\d{1,4}(?:,?\s+(?:bis|ter|quater))?\s+(?:rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|imp\.?|allée|place|pl\.?|square|sq\.?|passage|cours|quai)\s+(?:de\s+(?:la\s+|l'|le\s+)?|du\s+|des\s+)?[A-Za-zÀ-ÿ0-9\s'-]+",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )
    
    # Codes postaux français (5 chiffres)
    texte = re.sub(r"\b\d{5}\b", "[CP]", texte)
    
    # ==========================================
    # 5. DATES ET HEURES
    # ==========================================
    
    # Dates au format JJ/MM/AAAA ou JJ/MM/AA
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)
    
    # Dates au format JJ-MM-AAAA
    texte = re.sub(r"\b\d{1,2}-\d{1,2}-\d{2,4}\b", "[DATE]", texte)
    
    # Dates en toutes lettres
    texte = re.sub(
        r"\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )
    
    # Heures (HH:MM ou HHhMM)
    texte = re.sub(r"\b\d{1,2}[:h]\d{2}\b", "[HEURE]", texte)
    
    # ==========================================
    # 6. MONTANTS
    # ==========================================
    
    # Mon
