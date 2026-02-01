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
    texte = re.sub(r"\+33[\s.-]?[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)
    texte = re.sub(r"\+33[1-9]\d{8}\b", "[TEL]", texte)
    texte = re.sub(r"\b0[1-9](?:[\s.-]?\d{2}){4}\b", "[TEL]", texte)
    texte = re.sub(r"\b0[1-9]\d{8}\b", "[TEL]", texte)
    
    # 3. EMAILS
    texte = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", texte)
    
    # 4. ENTREPRISES (AVANT les adresses pour éviter conflits)
    entreprises = [
        "Orange", "SFR", "Bouygues", "Free", "EDF", "Engie", "Total", "TotalEnergies",
        "Renault", "Peugeot", "Citroën", "Carrefour", "Auchan", "Leclerc",
        "BNP", "Société Générale", "Crédit Agricole", "SNCF", "RATP", "Air France", "La Poste"
    ]
    
    for entreprise in entreprises:
        texte = re.sub(rf"\b{re.escape(entreprise)}\b", "[ENTREPRISE]", texte, flags=re.IGNORECASE)
    
    # 5. VILLES FRANÇAISES (liste complète des principales villes)
    villes = [
        # Grandes villes (>100k habitants)
        "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier",
        "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble",
        "Dijon", "Angers", "Nîmes", "Villeurbanne", "Saint-Denis", "Le Mans", "Aix-en-Provence",
        "Clermont-Ferrand", "Brest", "Limoges", "Tours", "Amiens", "Perpignan", "Metz", "Besançon",
        "Orléans", "Boulogne-Billancourt", "Mulhouse", "Rouen", "Caen", "Nancy", "Argenteuil",
        "Saint-Paul", "Montreuil", "Roubaix", "Tourcoing", "Nanterre", "Avignon", "Créteil",
        "Dunkerque", "Poitiers", "Asnières-sur-Seine", "Courbevoie", "Versailles", "Colombes",
        "Fort-de-France", "Aulnay-sous-Bois", "Saint-Pierre", "Rueil-Malmaison", "Pau", "Aubervilliers",
        "Le Tampon", "Champigny-sur-Marne", "Antibes", "La Rochelle", "Saint-Maur-des-Fossés",
        "Calais", "Cannes", "Béziers", "Colmar", "Bourges", "Drancy", "Mérignac", "Saint-Nazaire",
        "Valence", "Ajaccio", "Issy-les-Moulineaux", "Villeneuve-d'Ascq", "Levallois-Perret",
        "Noisy-le-Grand", "Quimper", "La Seyne-sur-Mer", "Antony", "Troyes", "Neuilly-sur-Seine",
        "Sarcelles", "Niort", "Chambéry", "Le Blanc-Mesnil", "Maisons-Alfort", "Saint-Quentin",
        "Beauvais", "Épinay-sur-Seine", "Meaux", "Fréjus", "Narbonne", "Pessac", "Laval",
        "Ivry-sur-Seine", "Cergy", "Cayenne", "Clichy", "Charleville-Mézières", "Cholet",
        "Pantin", "Sartrouville", "Sevran", "Vitry-sur-Seine", "Hyères", "La Roche-sur-Yon",
        "Grasse", "Montauban", "Arles", "Vincennes", "Clamart", "Vaulx-en-Velin", "Saint-Ouen",
        "Fontenay-sous-Bois", "Bondy", "Évreux", "Suresnes", "Martigues", "Bayonne", "Cagnes-sur-Mer",
        "Wattrelos", "Belfort", "Saint-Brieuc", "Saint-Malo", "Vannes", "Charleville", "Chelles",
        "Massy", "Albi", "Châteauroux", "Bobigny", "La Courneuve", "Saint-Laurent-du-Maroni",
        "Blois", "Istres", "Douai", "Livry-Gargan", "Castres", "Compiègne", "Vénissieux",
        "Évry", "Lorient", "Annecy", "Salon-de-Provence", "Draguignan", "Angoulême", "Tarbes",
        "Brive-la-Gaillarde", "Joué-lès-Tours", "Arras", "Chalon-sur-Saône", "Bourg-en-Bresse",
        "Échirolles", "Rezé", "Garges-lès-Gonesse", "Colomiers", "Nevers", "Alès", "Stains",
        "Talence", "Le Cannet", "Châlons-en-Champagne", "Montluçon", "Cambrai", "Valenciennes",
        "Romans-sur-Isère", "Gennevilliers", "Six-Fours-les-Plages", "Lens", "Thionville",
        "Melun", "Les Abymes", "Mâcon", "Chartres", "Anglet", "Marcq-en-Barœul", "Poissy",
        "Auxerre", "Saint-Denis", "Haguenau", "Épinal", "Montrouge", "Villejuif", "Gagny",
        "Schiltigheim", "Conflans-Sainte-Honorine", "Pontault-Combault", "Bagnolet", "Savigny-sur-Orge",
        "Villiers-sur-Marne", "Alfortville", "Châtenay-Malabry", "La Ciotat", "Thonon-les-Bains",
        "Saint-Priest", "Rosny-sous-Bois", "Francheville", "Meudon", "Nouméa", "Chatou",
        "Lambersart", "Villepinte", "Tremblay-en-France", "Charleville", "Soissons", "Mantes-la-Jolie",
        "Saint-Germain-en-Laye", "Montigny-le-Bretonneux", "Hénin-Beaumont", "Romainville",
        "Sainte-Geneviève-des-Bois", "Yutz", "Lisieux", "Viry-Châtillon", "Athis-Mons",
        "Carcassonne", "Vienne", "Saint-Chamond", "Villefranche-sur-Saône", "Armentières",
        "Cenon", "La Garde", "Cherbourg", "Rillieux-la-Pape", "Caluire-et-Cuire", "Périgueux",
        "Saint-Herblain", "Liévin", "Corbeil-Essonnes", "Plaisir", "Maubeuge", "Gap",
        "Bastia", "Thiais", "Bron", "Cachan", "Saint-Raphaël", "Olivet", "Boulogne-sur-Mer",
        "Puteaux", "Lens", "Agen", "Villenave-d'Ornon", "Bagneux", "Charenton-le-Pont",
        "Savigny-le-Temple", "Pontoise", "Palaiseau", "Vandœuvre-lès-Nancy", "Sotteville-lès-Rouen",
        "Herblay", "Décines-Charpieu", "Dreux", "Sainte-Marie", "Creil", "Agde", "Montélimar",
        "Nogent-sur-Marne", "Châtellerault", "Chaumont", "Vanves", "Goussainville", "Saumur",
        "Bergerac", "Dieppe", "Chatillon", "Saint-Médard-en-Jalles", "Baie-Mahault", "Vigneux-sur-Seine"
    ]
    
    for ville in villes:
        texte = re.sub(rf"\b{re.escape(ville)}\b", "[VILLE]", texte, flags=re.IGNORECASE)
    
    # 6. ADRESSES POSTALES (maintenant les villes sont déjà remplacées)
    texte = re.sub(
        r"\b\d{1,4}(?:,?\s+(?:bis|ter|quater))?\s+(?:rue|avenue|av\.?|boulevard|bd\.?|chemin|route|impasse|imp\.?|allée|place|pl\.?|square|sq\.?|passage|cours|quai)\s+(?:de\s+(?:la\s+|l'|le\s+)?|du\s+|des\s+)?[A-Za-zÀ-ÿ0-9\s'\[\]-]+?(?=,|\s+\d{5}|$)",
        "[ADRESSE]", texte, flags=re.IGNORECASE
    )
    texte = re.sub(r"(?<!dossier\s)\b\d{5}\b", "[CP]", texte)
    
    # 7. DATES ET HEURES
    texte = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(r"\b\d{1,2}-\d{1,2}-\d{2,4}\b", "[DATE]", texte)
    texte = re.sub(
        r"\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b",
        "[DATE]", texte, flags=re.IGNORECASE
    )
    texte = re.sub(r"\b(?:[01]?\d|2[0-3])[:h][0-5]\d\b", "[HEURE]", texte)
    
    # 8. MONTANTS
    texte = re.sub(r"\d+[\d\s.,]*\s?(?:€|euros?)", "[MONTANT]", texte, flags=re.IGNORECASE)
    
    # 9. NUMÉROS DE DOSSIER (minimum 4 chiffres)
    texte = re.sub(
        r"\b(?:dossier|dos\.?|réf\.?|référence)[\s:-]?\d{4,10}\b",
        "[DOSSIER]", texte, flags=re.IGNORECASE
    )
    
    # 10. INITIALES
    texte = re.sub(r"\b[A-Z]\.[A-Z]\.?(?:\.[A-Z]\.?)*\b", "[INITIALES]", texte)
    
    # 11. NOMS COMPLETS AVEC CIVILITÉ
    texte = re.sub(
        r"\b(?:M\.|Mme|Monsieur|Madame|Mlle|Mademoiselle|Dr|Docteur|Pr|Professeur)\s+[A-Za-zÀ-ÿ][a-zàâäéèêëïîôöùûüç'-]+(?:\s+[A-Za-zÀ-ÿ][a-zàâäéèêëïîôöùûüç'-]+)+\b",
        "[NOM_COMPLET]", texte, flags=re.IGNORECASE
    )
    
    # 12. PRÉNOMS COURANTS (liste étendue - minuscules et majuscules acceptés)
    prenoms_courants = [
        # Prénoms masculins très courants
        "Jean", "Pierre", "Michel", "André", "Philippe", "Alain", "Jacques", "Bernard",
        "Claude", "François", "Daniel", "Christian", "Éric", "Patrick", "Nicolas",
        "Thierry", "Stéphane", "Olivier", "Laurent", "Julien", "Thomas", "Alexandre",
        "Maxime", "Lucas", "Hugo", "Louis", "Arthur", "Gabriel", "Raphaël", "Nathan",
        "Antoine", "Paul", "Marc", "Vincent", "Christophe", "Sébastien", "David",
        "Jérôme", "Frédéric", "Guillaume", "Matthieu", "Benjamin", "Romain", "Florian",
        "Yves", "Henri", "Georges", "Robert", "René", "Maurice", "Roger", "Guy",
        "Charles", "Marcel", "Gérard", "Raymond", "André", "Lucien", "Fernand",
        "Serge", "Joseph", "Albert", "Émile", "Jacques", "Gaston", "Léon", "Édouard",
        "Dominique", "Pascal", "Didier", "Bruno", "Gilles", "Denis", "Hervé", "Francis",
        "Gilbert", "Christian", "Richard", "Fabrice", "Pascal", "Ludovic", "Cédric",
        "Arnaud", "Éric", "Benoît", "Samuel", "Mickaël", "Kévin", "Alexis", "Clément",
        "Adrien", "Simon", "Théo", "Tom", "Enzo", "Léo", "Adam", "Noah", "Ethan",
        "Jules", "Malo", "Gabin", "Timéo", "Sacha", "Robin", "Mathis", "Nolan",
        "Baptiste", "Dylan", "Valentin", "Corentin", "Quentin", "Aurélien", "Tristan",
        "Rémi", "Loïc", "Anthony", "Jonathan", "Jérémy", "Kilian", "Morgan", "Evan",
        
        # Prénoms féminins très courants
        "Marie", "Nathalie", "Isabelle", "Sylvie", "Catherine", "Françoise", "Martine",
        "Christine", "Monique", "Sophie", "Sandrine", "Valérie", "Céline", "Stéphanie",
        "Julie", "Anne", "Brigitte", "Patricia", "Nicole", "Chantal", "Hélène",
        "Camille", "Emma", "Léa", "Chloé", "Manon", "Sarah", "Laura", "Lucie",
        "Charlotte", "Amélie", "Caroline", "Émilie", "Florence", "Virginie", "Audrey",
        "Jeanne", "Marguerite", "Madeleine", "Simone", "Louise", "Denise", "Marcelle",
        "Jacqueline", "Suzanne", "Colette", "Paulette", "Germaine", "Yvonne", "Andrée",
        "Odette", "Mireille", "Danielle", "Christiane", "Janine", "Josiane", "Michèle",
        "Joséphine", "Thérèse", "Claire", "Dominique", "Laurence", "Corinne", "Véronique",
        "Karine", "Laetitia", "Estelle", "Jessica", "Jennifer", "Mélanie", "Aurélie",
        "Pauline", "Marine", "Justine", "Anaïs", "Mathilde", "Clémence", "Alexandra",
        "Agathe", "Elise", "Alice", "Inès", "Jade", "Zoé", "Clara", "Lisa", "Lola",
        "Rose", "Anna", "Nina", "Julia", "Lou", "Mila", "Lily", "Elena", "Juliette",
        "Louane", "Romy", "Margot", "Iris", "Eva", "Élise", "Maëlys", "Océane",
        "Solène", "Morgane", "Romane", "Élodie", "Angélique", "Ophélie", "Noémie",
        "Chloé", "Maëlle", "Léna", "Inaya", "Lina", "Apolline", "Constance", "Victoire"
    ]
    
    # Anonymiser d'abord les noms complets avec civilité pour éviter de les casser
    for prenom in prenoms_courants:
        # Pattern pour "M. Prénom Nom" - on garde intact pour la règle suivante
        pass
    
    # Maintenant anonymiser les prénoms restants (simples, sans civilité)
    for prenom in prenoms_courants:
        texte = re.sub(rf"\b{prenom}\b", "[PRENOM]", texte, flags=re.IGNORECASE)
    
    # 13. NOMS DE FAMILLE en minuscules (2-15 lettres) - après un prénom
    # Éviter les verbes courants en excluant certains mots
    mots_a_exclure = r"(?!avec|dans|chez|pour|sans|sous|vers|habite|vit|dit|fait|doit)"
    texte = re.sub(rf"\[PRENOM\]\s+{mots_a_exclure}([a-z]{{2,15}})\b", r"[PRENOM] [NOM]", texte)
    
    # 14. NOMS EN MAJUSCULES (3 à 15 lettres) - MAIS PAS les balises [XXX] déjà anonymisées
    # On exclut les mots en MAJUSCULES qui sont entre crochets
    texte = re.sub(r"(?<!\[)\b[A-Z]{3,15}(?:['-][A-Z]+)*\b(?!\])", "[NOM]", texte)
    
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
    
    texte_frais = """claude habite au 12 rue de Paris, 75015 Paris.Il a rendez-vous à 14h30 avec marie et SÉBASTIEN.Son numéro est 06 12 34 56 78.Le dossier 12 doit être traité.Le dossier 12345 est urgent.Les initiales C.V. sont présentes.Sébastien travaille chez Orange.Il habite à Valenciennes."""
    
    print("\n📝 TEXTE ORIGINAL:")
    print(texte_frais)
    print("\n🔒 RÉSULTAT:")
    resultat3 = anonymiser_transcription(texte_frais)
    print(resultat3)
    
    print("\n" + "="*80)
    print("TEST 4 : Test noms longs")
    print("="*80)
    
    texte_noms = """DUPONT a rencontré MARTINEZMENDEZ et CONSTANTINOPOLIS hier."""
    
    print("\n📝 TEXTE ORIGINAL:")
    print(texte_noms)
    print("\n🔒 RÉSULTAT:")
    resultat4 = anonymiser_transcription(texte_noms)
    print(resultat4)
