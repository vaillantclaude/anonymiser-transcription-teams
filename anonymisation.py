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
            print("⚠️  TEXTE DÉJÀ ANONYMISÉ DÉTECTÉ - Aucune modification")
            return texte
    
    print("✓ Début de l'anonymisation...")
    
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
    
    # 4. ENTREPRISES ET VILLES (AVANT les adresses pour éviter conflits)
    entreprises = [
        "Orange", "SFR", "Bouygues", "Free", "EDF", "Engie", "Total", "TotalEnergies",
        "Renault", "Peugeot", "Citroën", "Carrefour", "Auchan", "Leclerc",
        "BNP", "Société Générale", "Crédit Agricole", "SNCF", "RATP", "Air France", "La Poste"
    ]
    
    for entreprise in entreprises:
        texte = re.sub(rf"\b{re.escape(entreprise)}\b", "[ENTREPRISE]", texte, flags=re.IGNORECASE)
    
    villes = [
        "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg",
        "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre",
        "Saint-Étienne", "Toulon", "Grenoble", "Dijon", "Angers", "Nîmes", "Villeurbanne"
    ]
    
    for ville in villes:
        texte = re.sub(rf"\b{re.escape(ville)}\b", "[VILLE]", texte, flags=re.IGNORECASE)
    
    # 5. ADRESSES POSTALES (maintenant les villes sont déjà remplacées)
    texte = re.sub(
        r"\b\d{1,4}(?:,?\s+(?:bis|ter|quater))?\s+(?:rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|imp\.?|allée|place|pl\.?|square|sq\.?|passage|cours|quai)\s+(?:de\s+(?:la\s+|l'|le\s+)?|du\s+|des\s+)?[A-Za-zÀ-ÿ0-9\s'\[\]-]+?(?=,|\s+\d{5}|$)",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )
    texte = re.sub(r"(?<!dossier\s)\b\d{5}\b", "[CP]", texte)
    
    # 6. DATES ET HEURES
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(r"\b\d{1,2}-\d{1,2}-\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(
        r"\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )
    texte = re.sub(r"\b(?:[01]?\d|2[0-3])[:h][0-5]\d\b", "[HEURE]", texte)
    
    # 7. MONTANTS
    texte = re.sub(r"\b\d[\d\s.,]*\s?(?:€|euros?)\b", "[MONTANT]", texte, flags=re.IGNORECASE)
    
    # 8. NUMÉROS DE DOSSIER (minimum 4 chiffres)
    texte = re.sub(
        r"\b(?:dossier|dos\.?|réf\.?|référence)[\s:-]?\d{4,10}\b",
        "[DOSSIER]", texte, flags=re.IGNORECASE
    )
    
    # 9. INITIALES
    texte = re.sub(r"\b[A-Z]\.[A-Z]\.?(?:\.[A-Z]\.?)*\b", "[INITIALES]", texte)
    
    # 10. NOMS COMPLETS AVEC CIVILITÉ
    texte = re.sub(
        r"\b(?:M\.|Mme|Monsieur|Madame|Mlle|Mademoiselle|Dr|Docteur|Pr|Professeur)\s+[A-Z][a-zàâäéèêëïîôöùûüç'-]+(?:\s+[A-Z][a-zàâäéèêëïîôöùûüç'-]+)+\b",
        "[NOM_COMPLET]", texte
    )
    
    # 11. PRÉNOMS COURANTS
    prenoms_courants = [
        "Jean", "Pierre", "Michel", "André", "Philippe", "Alain", "Jacques", "Bernard",
        "Claude", "François", "Daniel", "Christian", "Éric", "Patrick", "Nicolas",
        "Thierry", "Stéphane", "Olivier", "Laurent", "Julien", "Thomas", "Alexandre",
        "Maxime", "Lucas", "Hugo", "Louis", "Arthur", "Gabriel", "Raphaël", "Nathan",
        "Antoine", "Paul", "Marc", "Vincent", "Christophe", "Sébastien", "David",
        "Jérôme", "Frédéric", "Guillaume", "Matthieu", "Benjamin", "Romain", "Florian",
        "Marie", "Nathalie", "Isabelle", "Sylvie", "Catherine", "Françoise", "Martine",
        "Christine", "Monique", "Sophie", "Sandrine", "Valérie", "Céline", "Stéphanie",
        "Julie", "Anne", "Brigitte", "Patricia", "Nicole", "Chantal", "Hélène",
        "Camille", "Emma", "Léa", "Chloé", "Manon", "Sarah", "Laura", "Lucie",
        "Charlotte", "Amélie", "Caroline", "Émilie", "Florence", "Virginie", "Audrey"
    ]
    
    for prenom in prenoms_courants:
        texte = re.sub(
            rf"(?<!M\. )(?<!Mme )(?<!Monsieur )(?<!Madame )\b{prenom}\b(?=\s|[,.]|$)",
            "[PRENOM]", texte
        )
    
    # 12. NOMS EN MAJUSCULES (3+ lettres) - MAIS PAS les balises [XXX] déjà anonymisées
    # On exclut les mots en MAJUSCULES qui sont entre crochets
    texte = re.sub(r"(?<!\[)\b[A-Z]{3,}(?:['-][A-Z]+)*\b(?!\])", "[NOM]", texte)
    
    print("✓ Anonymisation terminée")
    return texte


if __name__ == "__main__":
    print("="*80)
    print("TEST 1 : Texte DÉJÀ PARTIELLEMENT ANONYMISÉ")
    print("="*80)
    
    texte_deja_anonymise = """Claude habite au 12 rue de [VILLE], 75015 [VILLE].Il a rendez-vous à 14h30 avec Marie.Son numéro est [TEL].Le dossier 12 doit être traité.Les initiales C.V. sont présentes.Sébastien travaille chez [ENTREPRISE]."""
    
    print("\n📝 TEXTE ORIGINAL:")
    print(texte_deja_anonymise)
    print("\n🔒 RÉSULTAT AVEC PROTECTION (par défaut):")
    resultat1 = anonymiser_transcription(texte_deja_anonymise)
    print(resultat1)
    
    print("\n" + "="*80)
    print("TEST 2 : Même texte SANS PROTECTION (forcer l'anonymisation)")
    print("="*80)
    print("\n🔓 RÉSULTAT SANS PROTECTION:")
    resultat2 = anonymiser_transcription(texte_deja_anonymise, ignorer_deja_anonymise=False)
    print(resultat2)
    
    print("\n" + "="*80)
    print("TEST 3 : Texte FRAIS (jamais anonymisé)")
    print("="*80)
    
    texte_frais = """Claude habite au 12 rue de Paris, 75015 Paris.Il a rendez-vous à 14h30 avec Marie.Son numéro est 06 12 34 56 78.Le dossier 12 doit être traité.Le dossier 12345 est urgent.Les initiales C.V. sont présentes.Sébastien travaille chez Orange."""
    
    print("\n📝 TEXTE ORIGINAL:")
    print(texte_frais)
    print("\n🔒 RÉSULTAT:")
    resultat3 = anonymiser_transcription(texte_frais)
    print(resultat3)
