# 🛡️ Anonymiser toutes les transcriptions avant l'analyse d'un llm

Cet outil permet d’anonymiser automatiquement toutes les transcriptions générées lors de réunion avec Microsoft Teams, Zoom, Google Meet, Slack ou autres. Avant l'analyse d'un llm rédactionnel, il remplace les noms, prénoms et identifiants par des alias anonymes tout en conservant la structure du texte.

Il fonctionne **sans installation**, directement via un fichier `.exe` généré automatiquement par GitHub Actions.

---

## 📥 Télécharger l’outil

La dernière version de l’outil est disponible dans les **Artifacts GitHub Actions**.

➡️ **Téléchargement :**  
1. Cliquez sur l’onglet **Actions** du dépôt  
2. Sélectionnez le workflow **Build Windows EXE** le plus récent  
3. Descendez jusqu’à la section **Artifacts**  
4. Téléchargez le fichier :  
   **`anonymisation-windows.zip`**  
5. Décompressez le ZIP pour obtenir :  
   **`anonymisation.exe`**

Vous pouvez également accéder directement à la page des Actions :  
👉 https://github.com/vaillantclaude/anonymiser-transcriptions-teams/actions


---

## ▶️ Utilisation

1. Téléchargez et décompressez le fichier ZIP  
2. Double-cliquez sur **`anonymisation.exe`**  
3. Sélectionnez votre fichier de transcription Teams  
4. L’outil génère automatiquement une version anonymisée dans le même dossier

Aucune installation n’est nécessaire.  
L’outil fonctionne sur **Windows**.

---

## Fonctionnement

L’outil :
- détecte automatiquement les noms et prénoms dans la transcription  
- remplace chaque personne par un alias unique (ex : *Personne_1*, *Personne_2*, etc.)  
- conserve les timestamps, les paragraphes et la structure du fichier  
- génère un fichier anonymisé prêt à être partagé

---

## Génération automatique de l’EXE

Ce dépôt utilise **GitHub Actions** pour générer automatiquement un exécutable Windows à chaque mise à jour du code.

Le workflow :
- installe Python  
- installe PyInstaller  
- construit un `.exe`  
- le publie dans les **Artifacts**

Le fichier du workflow se trouve dans :  
`.github/workflows/build-exe.yml`

---

##  Structure du projet


