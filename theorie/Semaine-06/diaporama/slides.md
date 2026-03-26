---
theme: seriph
background: https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920
title: 243-4J5-LI - Objets connectés - Semaine 6
info: |
  ## Objets connectés
  Semaine 6 - Création d'empreintes, routage PCB et finalisation

  Cégep Limoilou - Session H26
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
download: true
---

# Objets connectés
## 243-4J5-LI

Semaine 6 - Création d'empreintes, routage PCB et finalisation

<div class="pt-12">
  <span class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Francis Poisson - Cégep Limoilou - H26
  </span>
</div>

---
layout: section
---

# Dates limites
## À ne pas manquer!

---

# Dates limites du projet de mi-session

<div class="grid grid-cols-2 gap-6">

<div class="p-4 bg-red-500 bg-opacity-20 rounded-lg border-2 border-red-400">

### PCB — Fichiers Gerber

<div class="text-3xl font-bold text-red-600 mt-3">Lundi 16 mars</div>
<div class="text-xl font-bold text-red-600">à 8h00</div>

<v-click>

- La **commande groupée** est passée ce matin-là
- Note de **0** pour la partie PCB si non remis
- Vérifier les Gerbers dans un viewer **avant** de remettre

</v-click>

</div>

<div class="p-4 bg-orange-500 bg-opacity-20 rounded-lg border-2 border-orange-400">

### Projet complet

<div class="text-3xl font-bold text-orange-600 mt-3">Lundi 23 mars</div>
<div class="text-xl font-bold text-orange-600">à 8h00</div>

<v-click>

- Firmware Arduino
- Interface Python (RPi)
- Documentation complète
- Tout pushé sur GitHub

</v-click>

</div>

</div>

---
layout: section
---

# Récapitulatif
## Où en sommes-nous?

---

# État d'avancement du projet

<div class="grid grid-cols-4 gap-2 text-sm">

<div class="p-2 bg-green-500 bg-opacity-20 rounded-lg">

### Semaines 1-3

<v-click>

- Infrastructure IoT ✓
- MQTT + LTE/WiFi ✓
- Sécurité TLS ✓

</v-click>

</div>

<div class="p-2 bg-green-500 bg-opacity-20 rounded-lg">

### Semaines 4-5

<v-click>

- Workflow KiCad ✓
- Schéma du shield ✓
- ERC passé ✓

</v-click>

</div>

<div class="p-2 bg-blue-500 bg-opacity-20 rounded-lg border-2 border-blue-400">

### Cette semaine

<v-click>

- **Empreintes personnalisées**
- Routage PCB
- DRC + Gerbers
- **Remise le 16 mars!**

</v-click>

</div>

<div class="p-2 bg-gray-500 bg-opacity-20 rounded-lg">

### Semaines 7+

<v-click>

- Firmware + Interface
- PCB fabriqué
- Assemblage soudure
- Remise 23 mars

</v-click>

</div>

</div>

---
layout: section
---

# Partie 1
## Création d'empreintes personnalisées

---

# Pourquoi créer une empreinte?

<div class="grid grid-cols-2 gap-6">

<div>

### Les bibliothèques KiCad ne couvrent pas tout

<v-clicks>

- Composant **nouveau ou rare** sans empreinte existante
- Module **breakout** avec brochage spécifique
- Empreinte standard **ne correspond pas** au composant physique
- Connecteur avec **pas d'espacement personnalisé**

</v-clicks>

<v-click>

<div class="mt-4 p-2 bg-blue-500 bg-opacity-20 rounded-lg text-sm">

**Dans notre projet** : les connecteurs femelles pour le LilyGO A7670G ont un brochage précis qui doit correspondre exactement au circuit.

</div>

</v-click>

</div>

<div>

<v-click>

### Rappel : symbole ↔ empreinte

```
Symbole (schéma)    Empreinte (PCB)
─────────────────   ──────────────────
Représentation      Dimensions physiques
logique             réelles

Pas de mesures      Trous, pastilles,
physiques           courtyard, silkscreen

→ Un symbole peut avoir plusieurs empreintes possibles
```

</v-click>

</div>

</div>

---

# Anatomie d'une empreinte

<div class="grid grid-cols-2 gap-6">

<div>

### Couches d'une empreinte

<v-clicks>

- **F.Cu / B.Cu** : pastilles de cuivre (pads)
- **F.Courtyard** : zone d'exclusion (pas de chevauchement)
- **F.Fab** : contour physique du composant
- **F.SilkS** : sérigraphie (labels, repères)
- **Holes** : trous de perçage (THT)

</v-clicks>

</div>

<div>

<v-click>

### Éléments d'une empreinte THT

```
  ┌─────────────────────┐  ← F.Courtyard (zone réservée)
  │   ┌───────────┐     │
  │   │  F.Fab    │     │  ← Silhouette composant
  │   │  ○  ○  ○  │     │  ← Trous (Through-Hole)
  │   │  ○  ○  ○  │     │
  │   └───────────┘     │
  └─────────────────────┘

  ○ = Pad THT
      ├── Trou de perçage (drill)
      ├── Annular ring (cuivre autour)
      └── Paste/mask layers
```

</v-click>

</div>

</div>

---

# Lire une datasheet pour extraire les dimensions

### Exemple : potentiomètre 10 kΩ (Bourns PTV09A)

<v-click>

| Dimension | Valeur | Rôle dans l'empreinte |
|-----------|--------|----------------------|
| Pin pitch | 2.5 mm | Espacement entre trous |
| Pin diameter | 0.6 mm | Diamètre de perçage |
| Body width | 9.5 mm | Contour F.Fab |
| Body height | 12 mm | Contour F.Fab |
| Mounting tab | 5.08 mm | Trou de fixation |

</v-click>

<v-click>

### Règles de perçage

| Type | Drill | Pad diameter |
|------|-------|--------------|
| Composant fin (résistance) | 0.8 mm | 1.6 mm |
| Composant moyen (bouton, pot.) | 1.0 mm | 2.0 mm |
| Connecteur large | 1.2 mm | 2.4 mm |

</v-click>

<v-click>

<div class="mt-2 p-2 bg-orange-500 bg-opacity-20 rounded-lg text-sm text-center">

**Règle** : Pad diameter = Drill diameter × 2 (annular ring ≥ 0.3 mm de chaque côté)

</div>

</v-click>

---

# Démo : créer une empreinte dans KiCad

### Footprint Editor — étape par étape

<v-clicks>

1. **Ouvrir le Footprint Editor** : dans KiCad Manager → Footprint Editor
2. **Créer une nouvelle empreinte** : File → New Footprint → type "THT"
3. **Nommer** : ex. `Potentiometer_PTV09A_Vertical`
4. **Ajouter les pads** : Add Pad (raccourci **P**)
   - Type : Through-hole
   - Shape : Circular (ou Rect pour pin 1)
   - Drill size : 1.0 mm, Pad size : 2.0 mm
   - Pad 1 = carré (repère de sens)
5. **Positionner les pads** : selon le pitch de la datasheet
6. **Tracer le F.Courtyard** : Add Rectangle sur la couche F.Courtyard
7. **Tracer le F.Fab** : silhouette du composant
8. **Ajouter la référence** : texte sur F.SilkS
9. **Sauvegarder** dans une bibliothèque personnalisée

</v-clicks>

---

# Démo en classe : empreinte du connecteur LilyGO

### Objectif : créer l'empreinte du header 1×19 pas 2.54 mm

<div class="grid grid-cols-2 gap-6">

<div>

<v-click>

### Données du composant

| Paramètre | Valeur |
|-----------|--------|
| Nombre de pins | 19 (×2 rangées) |
| Pitch | 2.54 mm |
| Type | Femelle THT |
| Drill | 0.8 mm |
| Pad | 1.6 mm |

</v-click>

</div>

<div>

<v-click>

### Dans KiCad — raccourcis utiles

| Touche | Action |
|--------|--------|
| **P** | Ajouter un pad |
| **E** | Éditer propriétés |
| **Ctrl+D** | Dupliquer |
| **Ctrl+Z** | Annuler |
| **L** | Changer de couche |

</v-click>

<v-click>

<div class="mt-2 p-2 bg-green-500 bg-opacity-20 rounded-lg text-sm">

**Astuce** : KiCad a un assistant "Footprint Wizard" pour les connecteurs standards — utiliser **Tools → Footprint Wizard**.

</div>

</v-click>

</div>

</div>

---

# Vérifier et utiliser une empreinte personnalisée

<div class="grid grid-cols-2 gap-6">

<div>

### Vérification dans le Footprint Editor

<v-clicks>

1. **DRC de l'empreinte** : Inspect → Board Statistics
2. Vérifier que le **courtyard** entoure tous les pads
3. Vérifier que les pads ne débordent pas du courtyard
4. **Vue 3D** : View → 3D Viewer (si modèle 3D disponible)

</v-clicks>

</div>

<div>

<v-click>

### Associer au symbole dans le schéma

1. Dans l'éditeur de schéma : clic-droit sur le composant → **Properties**
2. Champ **Footprint** : sélectionner votre bibliothèque → votre empreinte
3. Ou via **Tools → Assign Footprints** (masse)

</v-click>

<v-click>

<div class="mt-2 p-2 bg-orange-500 bg-opacity-20 rounded-lg text-sm">

Les empreintes personnalisées doivent être dans une **bibliothèque partagée** avec le projet (dossier `libraries/` dans le dépôt GitHub).

</div>

</v-click>

</div>

</div>

---
layout: section
---

# Partie 2
## Routage PCB

---

# Stratégies de placement

### La clé d'un bon routage

<div class="grid grid-cols-2 gap-6">

<div>

<v-clicks>

- **Placement AVANT routage** : critique!
- Regrouper les composants par fonction
- Minimiser les croisements de pistes
- Respecter les contraintes mécaniques
- Penser au flux du signal

</v-clicks>

</div>

<div>

<v-click>

### Ordre de placement

1. **Connecteurs** : positions fixes (bord du PCB)
2. **Composants critiques** : MCU, régulateurs
3. **Composants associés** : près de leur connexion
4. **Passifs** : résistances, condensateurs
5. **Ajustements** : optimiser les chemins

</v-click>

</div>

</div>

<v-click>

<div class="mt-4 p-2 bg-blue-500 bg-opacity-20 rounded-lg text-center text-sm">

**Règle d'or** : Un bon placement = routage facile. Un mauvais placement = cauchemar!

</div>

</v-click>

---

# Placement pour le shield LilyGO

### Contraintes spécifiques

<div class="grid grid-cols-2 gap-6">

<div>

<v-click>

### Positions imposées

- **Headers femelles** : alignés avec le LilyGO
- **LEDs** : visibles sur le dessus
- **Boutons** : accessibles
- **Potentiomètres** : manipulation aisée

</v-click>

<v-click>

### Positions flexibles

- **Accéléromètre** : proche des broches I2C
- **Résistances** : près des composants associés
- **Condensateurs** : près de l'alimentation

</v-click>

</div>

<div>

<v-click>

### Vue de dessus (exemple)

- Potentiomètres en haut
- Boutons et LEDs au centre
- Accéléromètre proche des broches I2C
- Headers LilyGO en bas

</v-click>

</div>

</div>

---

# Routage 2 couches

### Top et Bottom

<div class="grid grid-cols-2 gap-6">

<div>

<v-click>

### Couche Top (rouge)

- Composants traversants
- Pistes de signal principales
- Connexions courtes
- Sérigraphie visible

</v-click>

<v-click>

### Couche Bottom (bleu)

- Plan de masse (GND)
- Pistes secondaires
- Croisements de signaux
- Soudure des composants THT

</v-click>

</div>

<div>

<v-click>

### Stratégie recommandée

**Top** : Pistes de signal horizontales, composants

**Bottom** : Plan de masse continu avec vias de connexion

</v-click>

</div>

</div>

---

# Largeur des pistes et espacement

<div class="grid grid-cols-2 gap-4">

<div>

<v-click>

### Largeur selon le courant

| Courant | Largeur min. | Usage |
|---------|--------------|-------|
| < 100 mA | 0.2 mm | Signaux logiques |
| 100-500 mA | 0.3-0.5 mm | LEDs, capteurs |
| 500 mA - 1A | 0.5-1.0 mm | Alimentation |

</v-click>

<v-click>

### Notre projet

- **Signaux GPIO** : 0.25 mm
- **Alimentation 3.3V** : 0.4-0.5 mm
- **GND** : Plan de masse

</v-click>

</div>

<div>

<v-click>

### Espacement (clearance)

**File → Board Setup → Design Rules**

```
Clearance:
├── Track to track: 0.2 mm
├── Track to pad:   0.2 mm
└── Pad to pad:     0.2 mm

Track width:
├── Default: 0.25 mm
├── Power:   0.5 mm
└── Min:     0.2 mm
```

</v-click>

</div>

</div>

---

# Plan de masse et vias

<div class="grid grid-cols-2 gap-6">

<div>

### Plan de masse

<v-clicks>

- **Référence stable** pour tous les signaux
- **Réduction du bruit** électromagnétique
- **Dissipation thermique**

</v-clicks>

<v-click>

### Créer un plan de masse

1. **Place → Add Filled Zone** (ou **B**)
2. Couche **Bottom**, net **GND**
3. Dessiner le contour du PCB
4. **B** pour remplir

</v-click>

</div>

<div>

### Vias

<v-click>

- Trou métallisé traversant le PCB
- Connecte Top ↔ Bottom
- Diamètre typique : 0.3-0.6 mm

</v-click>

<v-click>

### Raccourcis de routage

| Touche | Action |
|--------|--------|
| **X** | Commencer une piste |
| **V** | Placer un via |
| **D** | Drag (déplacer avec pistes) |
| **/** | Changer de couche |
| **B** | Remplir les zones |

</v-click>

</div>

</div>

---
layout: section
---

# Partie 3
## Fichiers de fabrication

---

# Générer les Gerbers dans KiCad

### File → Fabrication Outputs → Gerbers

<div class="grid grid-cols-2 gap-6">

<div>

<v-click>

### Couches à exporter

```
✓ F.Cu / B.Cu (Copper)
✓ F.SilkS / B.SilkS (Silkscreen)
✓ F.Mask / B.Mask (Solder Mask)
✓ Edge.Cuts (Board Outline)
```

</v-click>

<v-click>

### Options importantes

- Format : **Gerber X2**, coordinate **4.6** (mm)
- **Cocher** : Use drill/place file origin

</v-click>

</div>

<div>

<v-click>

### Fichier de perçage

**File → Fabrication Outputs → Drill Files**

- Format: **Excellon**, Units: **mm**, Zeros: Decimal

</v-click>

<v-click>

### Paramètres fabrication (JLCPCB)

| Paramètre | Valeur |
|-----------|--------|
| Couches | 2 |
| Épaisseur | 1.6 mm |
| Cuivre | 1 oz (35µm) |
| Couleur | Vert |
| Finition | HASL |

</v-click>

</div>

</div>

---

# Vérification finale avant commande

<div class="grid grid-cols-2 gap-4 text-sm">

<div>

### DRC : Inspect → Design Rules Checker

<v-click>

| Erreur DRC | Solution |
|-----------|----------|
| Clearance | Déplacer une piste |
| Unconnected | Router la connexion |
| Courtyard overlap | Espacer les composants |
| Track too thin | Augmenter la largeur |

</v-click>

<v-click>

### Checklist PCB

- [ ] DRC passé (0 erreurs)
- [ ] Plan de masse présent (Bottom GND)
- [ ] Contour Edge.Cuts fermé
- [ ] Toutes les ratsnest routées

</v-click>

</div>

<div>

<v-click>

### Vérification Gerbers

- **JLCPCB Gerber Viewer** (en ligne)
- Aperçu 3D après upload
- Vérifier : coutures, perçages, sérigraphie

</v-click>

</div>

</div>

<v-click>

### Vue 3D

**View → 3D Viewer**

- Headers orientés vers le LilyGO ✓
- LEDs visibles sur le dessus ✓
- Boutons accessibles ✓
- Potentiomètres — axe accessible ✓

</v-click>

---
layout: section
---

# Travail de la semaine
## Objectifs et livrables

---

# Objectifs du laboratoire

### Ce que vous devez accomplir cette semaine

<div class="grid grid-cols-2 gap-4">

<div>

### Priorité 1 : Empreinte

<v-clicks>

- [ ] Vérifier toutes les empreintes assignées
- [ ] Créer l'empreinte manquante si besoin
- [ ] Sauvegarder dans le dépôt GitHub
- [ ] Mettre à jour la netlist

</v-clicks>

### Priorité 2 : Routage

<v-clicks>

- [ ] Placement optimisé des composants
- [ ] Toutes les pistes routées
- [ ] Plan de masse sur Bottom
- [ ] **DRC : 0 erreurs**

</v-clicks>

</div>

<div>

### Priorité 3 : Fabrication

<v-clicks>

- [ ] Fichiers Gerber générés
- [ ] Fichier de perçage (.drl)
- [ ] Vérification dans Gerber viewer
- [ ] BOM exportée

</v-clicks>

### Priorité 4 : Documentation

<v-clicks>

- [ ] README.md à jour
- [ ] Schéma PDF exporté
- [ ] Screenshots du PCB 3D
- [ ] Topics MQTT documentés

</v-clicks>

</div>

</div>

---

# Rappel des livrables

### Projet de mi-session — 20% du cours

<div class="grid grid-cols-2 gap-3 text-sm">

<div class="p-2 bg-blue-500 bg-opacity-20 rounded-lg">

**Shield PCB (30%)**
- Schéma KiCad complet (ERC ✓)
- Routage PCB soigné (DRC ✓)
- Fichiers Gerber valides

</div>

<div class="p-2 bg-green-500 bg-opacity-20 rounded-lg">

**Programme embarqué (30%)**
- Lecture capteurs + contrôle LEDs
- Communication MQTT bidirectionnelle
- Qualité du code

</div>

<div class="p-2 bg-purple-500 bg-opacity-20 rounded-lg">

**Interface RPi (20%)**
- Affichage temps réel
- Contrôle des LEDs
- Démarrage automatique au boot

</div>

<div class="p-2 bg-orange-500 bg-opacity-20 rounded-lg">

**Documentation (20%)**
- README complet
- API MQTT documentée
- Schéma PDF + BOM

</div>

</div>

<v-click>

<div class="mt-3 p-2 bg-red-500 bg-opacity-20 rounded-lg text-center text-sm">

**PCB (Gerbers) → 16 mars à 8h00 | Projet complet → 23 mars à 8h00**

</div>

</v-click>

---
layout: center
class: text-center
---

# Questions?

<div class="text-xl mt-8">
Prochaine étape : Finaliser votre PCB et remettre les Gerbers!
</div>

<div class="mt-4 p-3 bg-red-500 bg-opacity-20 rounded-lg text-sm">
Rappel : <strong>Gerbers → lundi 16 mars à 8h00</strong> | Projet complet → lundi 23 mars à 8h00
</div>

---
layout: end
---

# Merci!

243-4J5-LI - Objets connectés

Semaine 6
