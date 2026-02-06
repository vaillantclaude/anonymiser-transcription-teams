# Anonymiser les transcriptions avant analyse LLM

Cet outil permet d’anonymiser automatiquement les transcriptions générées lors de réunions Microsoft Teams, Zoom, Google Meet, Slack ou autres.  
Avant toute analyse par un modèle rédactionnel, il remplace les noms, prénoms et identifiants par des alias anonymes tout en conservant la structure du texte.

L’outil fonctionne **sans installation**, via un fichier `.exe` généré automatiquement par GitHub Actions.

---

## Sommaire

- [Téléchargement](#téléchargement)
- [Utilisation](#utilisation)
- [Fonctionnement](#fonctionnement)
- [Génération automatique de lEXE](#génération-automatique-de-lexe)
- [Structure du projet](#structure-du-projet)

---

## Téléchargement

La dernière version de l’outil est disponible dans les **Artifacts GitHub Actions**.

### Étapes :

1. Ouvrir l’onglet **Actions** du dépôt  
2. Sélectionner le workflow **Build Windows EXE** le plus récent  
3. Descendre jusqu’à la section **Artifacts**  
4. Télécharger le fichier :  
   **`anonymisation-windows.zip`**  
5. Décompresser le ZIP pour obtenir :  
   **`anonymisation.exe`**

Accès direct aux Actions :  
https://github.com/vaillantclaude/anonymiser-transcription-teams/actions

---

## Utilisation

1. Télécharger et décompresser le fichier ZIP  
2. Lancer **`anonymisation.exe`**  
3. Sélectionner le fichier de transcription Teams  
4. Une version anonymisée est générée automatiquement dans le même dossier

Aucune installation n’est nécessaire.  
Compatible **Windows**.

---

## Fonctionnement

L’outil :

- détecte automatiquement les noms et prénoms dans la transcription  
- remplace chaque personne par un alias unique (ex. : `Personne_1`, `Personne_2`, etc.)  
- conserve les timestamps, paragraphes et structure du fichier  
- génère un fichier anonymisé prêt à être partagé  

---

## Génération automatique de l’EXE

Le dépôt utilise **GitHub Actions** pour générer automatiquement un exécutable Windows à chaque mise à jour du code.

Le workflow :

- installe Python  
- installe PyInstaller  
- construit un `.exe`  
- publie l’exécutable dans les **Artifacts**

Le fichier du workflow se trouve dans :  
`.github/workflows/build-exe.yml`

---

## Structure du projet


