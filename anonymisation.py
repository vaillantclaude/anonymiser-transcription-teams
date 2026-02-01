import re

def anonymiser_transcription(texte):
    """
    Anonymise une transcription en masquant les données sensibles.
    Optimisé pour réduire les faux positifs.
    """
    
    # ==========================================
    # PROTECTION : Ne pas ré-anonymiser du texte déjà anonymisé
    # ==========================================
    
    # Si le texte contient déjà des balises [XXX], on l'ignore
    if re.search(r'\[(?:ADRESSE|CP|TEL|EMAIL|MONTANT|DATE|HEURE|DOSSIER|IBAN|CB|SECU|SIRET|NOM|PRENOM|VILLE|ENTREPRISE|INITIALES)\]', texte):
        return texte  # Texte déjà anonymisé, on ne le modifie pas
    
    # ==========================================
    # 1. DONNÉES STRUCTURÉES (en premier)
    # ==========================================
    
    # IBAN français
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11,30}\b", "[IBAN]", texte)
    
    # Numéro de carte bancaire (16 chiffres)
    texte = re.sub(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[CB]", texte)
    
    # Numéro de sécurité sociale
    texte = re.sub(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b", "[SECU]", texte)
    
    # SIRET (14 chiffres)
    texte = re.sub(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b", "[SIRET]", texte)
    
    # ==========================================
    # 2. TÉLÉPHONES FRANÇAIS
    # ==========================================
    
    # Format international : +33 X XX XX XX XX
    texte = re.sub(r"\b\+33[\s.-]?[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)
    texte = re.sub(r"\b\+33[1-9]\d{8}\b", "[TEL]", texte)
    
    # Format national : 0X XX XX XX XX
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)
    texte = re.sub(r"\b0[1-9]\d{8}\b", "[TEL]", texte)
    
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
    
    # Adresses complètes (avec numéro de rue)
    texte = re.sub(
        r"\b\d{1,4}(?:,?\s+(?:bis|ter|quater))?\s+(?:rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|imp\.?|allée|place|pl\.?|square|sq\.?|passage|cours|quai)\s+(?:de\s+(?:la\s+|l'|le\s+)?|du\s+|des\s+)?[A-Za-zÀ-ÿ0-9\s'-]+?(?=,|\s+\d{5}|$)",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )
    
    # Codes postaux français (5 chiffres) - UNIQUEMENT si non précédé de "dossier"
    texte = re.sub(r"(?<!dossier\s)\b\d{5}\b", "[CP]", texte)
    
    # ==========================================
    # 5. DATES ET HEURES
    # ==========================================
    
    # Dates au format JJ/MM/AAAA
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(r"\b\d{1,2}-\d{1,2}-\d{2,4}\b", "[DATE]", texte)
    
    # Dates en toutes lettres
    texte = re.sub(
        r"\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )
    
    # Heures (HH:MM ou HHhMM) - UNIQUEMENT si format valide
    texte = re.sub(r"\b(?:[01]?\d|2[0-3])[:h][0-5]\d\b", "[HEURE]", texte)
    
    # ==========================================
    # 6. MONTANTS
    # ==========================================
    
    texte = re.sub(r"\b\d[\d\s.,]*\s?(?:€|euros?)\b", "[MONTANT]", texte, flags=re.IGNORECASE)
    
    # ==========================================
    # 7. NUMÉROS DE DOSSIER (au moins 4 chiffres)
    # ==========================================
    
    texte = re.sub(
        r"\b(?:dossier|dos\.?|réf\.
