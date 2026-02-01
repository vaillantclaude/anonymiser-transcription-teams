import re

def anonymiser_transcription(texte, ignorer_deja_anonymise=True):
    """
    Anonymise une transcription en masquant les données sensibles.
    
    Args:
        texte (str): Le texte à anonymiser
        ignorer_deja_anonymise (bool): Si True, ignore les textes déjà anonymisés
    
    Returns:
        str: Texte anonymisé
    """
    
    # Protection contre double anonymisation
    if ignorer_deja_anonymise:
        if re.search(r'\[(?:ADRESSE|CP|TEL|EMAIL|MONTANT|DATE|HEURE|DOSSIER|IBAN|CB|SECU|SIRET|NOM|PRENOM|VILLE|ENTREPRISE|INITIALES|NOM_COMPLET)\]', texte):
            return texte
    
    # 1. DONNÉES STRUCTURÉES
    texte = re.sub(r"\bFR\d{2}[A-Z0-9]{11,30}\b", "[IBAN]", texte)
    texte = re.sub(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[CB]", texte)
    texte = re.sub(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b", "[SECU]", texte)
    texte = re.sub(r"\b\d{3}\s?\d{3}\s?\d{3}\s?\d{5}\b", "[SIRET]", texte)
    
    # 2. TÉLÉPHONES FRANÇAIS
    texte = re.sub(r"\b\+33[\s.-]?[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)
    texte = re.sub(r"\b\+33[1-9]\d{8}\b", "[TEL]", texte)
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)
    texte = re.sub(r"\b0[1-9]\d{8}\b", "[TEL]", texte)
    
    # 3. EMAILS
    texte = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", texte)
    
    # 4. ADRESSES POSTALES
    texte = re.sub(
        r"\b\d{1,4}(?:,?\s+(?:bis|ter|quater))?\s+(?:rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|imp\.?|allée|place|pl\.?|square|sq\.?|passage|cours|quai)\s+(?:de\s+(?:la\s+|l'|le\s+)?|du\s+|des\s+)?[A-Za-zÀ-ÿ0-9\s'\[\]-]+?(?=,|\s+\d{5}|$)",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )
    texte = re.sub(r"(?<!dossier\s)\b\d{5}\b", "[CP]", texte)
    
    # 5. DATES ET HEURES
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(r"\b\d{1,2}-\d{1,2}-\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(
        r"\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )
    texte = re.sub(r"\b(?:[01]?\d|2[0-3])[:h][0-5]\d\b", "[HEURE]", texte)
    
    # 6. MONTANTS
    texte = re.sub(r"\b\d[\d\s.,]*\s?(?:€|euros?)\b", "[MONTANT]", texte, flags=re.IGNORECASE)
    
    # 7. NUMÉROS DE DOSSIER (minimum 4 chiffres)
    texte = re.sub(
        r"\b(?:dossier|dos\.?|réf\.?|référence)[\s:-]?\d{4,10}\b",
        "[DOSSIER]", texte, flags=re.IGNORECASE
    )
    
    # 8. INITIALES
    texte = re.sub(r"\b[A-Z]\.[A-Z]\.?(?:\.[A-Z]\.?)*\b", "[INITIALES]", texte)
    
    # 9. NOMS COMPLETS AVEC CIVILITÉ
    texte = re.sub(
        r"\b(?:M\.|Mme|Monsieur|Madame|Mlle|Mademoiselle|Dr|Docteur|Pr|Professeur)\s+[A-Z][a-zàâäéèêëïîôöùûüç'-]+(?:\s+[A-Z][a-zàâäéèêëïîôöùûüç'-]+)+\b",
        "[NOM_COMPLET]", texte
    )
    
    # 10. PRÉNOMS COURANTS
    prenoms_courants = [
        "Jean", "Pierre", "Michel", "André", "Philippe", "Alain", "Jacques", "Bernard",
        "Claude", "François", "Daniel", "Christian", "Éric", "Patrick", "Nicolas",
        "Thierry", "Stéphane", "Olivier", "Laurent", "Julien", "Thomas", "Alexandre",
        "Maxime", "Lucas", "Hugo", "Louis", "Arthur", "Gabriel", "Raphaël", "Nathan",
        "Antoine", "Paul", "Marc", "Vincent", "Christophe", "Sébastien", "David",
        "Jérôme", "Frédéric", "Guillaume", "Matthieu", "Benjamin", "Romain", "Florian",
        "Marie", "Nathalie", "Isabelle", "Sylvie", "Catherine", "Françoise", "Martine",
        "Christine", "M
