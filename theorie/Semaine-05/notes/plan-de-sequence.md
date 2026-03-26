# Plan de séquence - Semaine 05

## Titre
Introduction KiCad et dessin de PCB (contenu reporté de la semaine 4)

## Objectifs de la semaine
- Comprendre les concepts fondamentaux de la conception PCB
- Maîtriser les modules principaux de KiCad 8
- Distinguer les technologies THT et SMD
- Saisir la relation symbole ↔ empreinte et savoir qu'un symbole peut avoir plusieurs empreintes
- Démarrer le schéma KiCad du shield LilyGO dans le cadre du projet de mi-session

## Contenu théorique

### Concepts PCB
- Différence entre schéma électrique et dessin PCB
- Couches d'un PCB : cuivre (Top/Bottom), sérigraphie, masque de soudure, substrat FR4
- Empreintes (footprints) : relation symbole ↔ empreinte
- Exemple : résistance — un seul symbole, plusieurs empreintes (THT, 0805, 0603, 0402)
- Vérification des règles électriques (ERC) et de conception (DRC)
- Technologies de montage : THT (Through-Hole) vs SMD (Surface Mount Device)

### Modules KiCad 8
- Éditeur de schéma (Schematic Editor) : symboles, fils, labels, annotations
- Éditeur PCB (PCB Editor) : empreintes, routage, plan de masse
- Gestionnaire d'empreintes (Footprint Editor) : bibliothèques, association symbole/empreinte
- Visionneuse 3D : vérification visuelle du résultat final

### Workflow complet : schéma → PCB → Gerbers
- Saisie du schéma et annotation des composants
- Association des empreintes (assign footprints)
- Transfert vers l'éditeur PCB (update PCB from schematic)
- Placement des composants et routage
- Génération des fichiers de fabrication (Gerbers, BOM, fichiers de perçage)

### Assignation des composants par étudiant
| Étudiant | Boutons | LEDs | Potentiomètres |
|:--------:|:-------:|:----:|:--------------:|
| 1 | 1 | 3 | 3 |
| 2 | 2 | 2 | 3 |
| 3 | 3 | 1 | 3 |
| 4 | 1 | 4 | 2 |
| 5 | 2 | 3 | 2 |
| 6 | 3 | 2 | 2 |
| 7 | 3 | 3 | 1 |
| 8 | 2 | 4 | 1 |

MPU6050 (accéléromètre I2C) + connecteurs femelles LilyGO : obligatoires pour tous.

## Activités

### Théorie (2h)
- Présentation des concepts PCB (couches, THT vs SMD, empreintes)
- Tour des modules KiCad 8 avec démonstration
- Exemple résistance : un symbole → plusieurs empreintes possibles
- Workflow complet illustré
- Introduction au Labo 05 : shield LilyGO

### Laboratoire 05 — Schéma KiCad du shield LilyGO (3h)
- Créer le projet KiCad `shield-lilygo`
- Placer les composants assignés dans l'éditeur de schéma
- Établir les connexions entre composants (fils et labels de réseau)
- Passer la vérification ERC et corriger les erreurs signalées
- Sauvegarder et pousser sur GitHub

## Travaux hors classe
- Compléter la correction des erreurs ERC si non terminée en classe
- Monter le prototype breadboard avec les composants assignés
- Assigner les empreintes (THT) à tous les composants
- Préparer les questions sur le routage (semaine 6)

## Évaluation
- Suivi de progression du schéma KiCad (formatif)
- Vérification que l'ERC passe sans erreurs bloquantes

## Ressources
- Documentation officielle KiCad 8
- Bibliothèques de symboles KiCad (standard + personnalisées du projet)
- Fichiers de départ du projet shield LilyGO sur GitHub
- Tutoriels vidéo KiCad (saisie de schéma)
- Énoncé du projet de mi-session (Evaluation-02/Projet-mi-session.md)

## Notes pour l'enseignant
- Ce cours reprend la théorie initialement prévue à la semaine 4 (non présentée)
- Insister sur la distinction schéma/PCB et symbole/empreinte, source de confusion fréquente
- S'assurer que les assignations de composants par étudiant sont confirmées avant le labo
- Prévoir du temps pour le dépannage des bibliothèques KiCad manquantes
- Le Labo 05 est la première étape concrète du projet de mi-session (shield LilyGO)
- **Annoncer les dates limites : Gerbers le lundi 16 mars à 8h00, projet complet le lundi 23 mars à 8h00**
