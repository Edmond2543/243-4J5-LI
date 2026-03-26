# Plan de séquence - Semaine 06

## Titre
Création d'empreintes personnalisées, routage PCB et finalisation

## Objectifs de la semaine
- Créer des empreintes (footprints) personnalisées dans KiCad lorsque la bibliothèque standard est insuffisante
- Finaliser le schéma électronique et s'assurer que toutes les empreintes sont assignées
- Compléter le routage du PCB 2 couches
- Générer les fichiers de fabrication (Gerbers, BOM) prêts pour la commande

## Contenu théorique

### Dates limites — à communiquer dès le début du cours
- **Gerbers (PCB) : lundi 16 mars 2026 à 8h00** — commande groupée passée ce matin-là, note de 0 si non remis
- **Projet complet : lundi 23 mars 2026 à 8h00**

### Création d'empreintes personnalisées
- Quand créer une empreinte : composant absent de la bibliothèque ou brochage non standard
- Anatomie d'une empreinte : pads (THT/SMD), courtyard, F.Fab, sérigraphie
- Lire une datasheet pour extraire les dimensions (pitch, drill, pad, courtyard)
- Règle de dimensionnement : pad ≥ drill × 2 (annular ring minimum 0.3 mm par côté)
- Démo en classe : créer l'empreinte du connecteur header LilyGO avec le Footprint Wizard

### Routage avancé
- Stratégies de placement : connecteurs en premier, puis composants critiques, puis passifs
- Routage 2 couches : Top (signaux), Bottom (plan de masse GND)
- Plan de masse : placement, thermal reliefs, vias GND
- Largeur des pistes selon le courant : 0.25 mm signaux, 0.5 mm alimentation
- Espacement minimum : 0.2 mm pour les pistes à 3.3 V
- Vias : utilisation pour changer de couche, diamètre 0.3-0.6 mm

### Fichiers de fabrication
- Standard Gerber RS-274X : un fichier par couche
- Fichiers de perçage Excellon (.drl)
- Génération dans KiCad : File → Fabrication Outputs
- BOM (Bill of Materials) : référence, valeur, quantité, empreinte
- Vérification des Gerbers : JLCPCB Viewer ou Gerbv

### Vérification finale
- DRC : Inspect → Design Rules Checker (0 erreurs requis)
- Erreurs DRC courantes : clearance, unconnected, courtyard overlap
- Vue 3D : vérification mécanique (orientation, hauteurs)
- Checklist avant envoi : ERC, DRC, plan de masse, Edge.Cuts fermé, perçages

## Activités

### Théorie (2h)
- Présentation des dates limites (16 mars et 23 mars)
- Démo création d'empreinte personnalisée (Footprint Wizard + manuel)
- Stratégies de routage et plan de masse
- Génération et vérification des Gerbers

### Laboratoire (3h)
- Vérification et création des empreintes manquantes
- Finalisation du placement des composants
- Routage complet du PCB
- Ajout du plan de masse (Bottom GND)
- Vérification DRC et corrections
- Génération des fichiers Gerber et BOM
- Vérification dans un Gerber viewer

## Travaux hors classe
- **Remettre les Gerbers avant le lundi 16 mars à 8h00**
- Vérifier les Gerbers dans un visualiseur en ligne
- Compléter la documentation technique (README.md, schéma PDF, API MQTT)
- Poursuivre le firmware et l'interface Python pour la remise du 23 mars

## Évaluation
- Suivi de progression (formatif)
- Vérification de l'état d'avancement du PCB et des Gerbers

## Ressources
- Documentation KiCad — Footprint Editor
- Documentation KiCad — Génération Gerbers
- JLCPCB Gerber Viewer (en ligne)
- Datasheet LilyGO A7670G (brochage)
- Énoncé du projet de mi-session (Evaluation-02/Projet-mi-session.md)

## Notes pour l'enseignant
- **Rappeler les dates limites en début de cours** : PCB le 16 mars à 8h, projet complet le 23 mars à 8h
- Faire la démo de création d'empreinte avec le Footprint Wizard (connecteur header 1×19)
- Vérifier les Gerbers de chaque étudiant avant la commande groupée
- Organiser la commande JLCPCB groupée pour économiser sur la livraison
- Prévoir du temps pour les corrections individuelles DRC
