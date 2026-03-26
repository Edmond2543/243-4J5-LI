---
theme: seriph
background: https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920
title: 243-4J5-LI - Objets connectés - Semaine 10
info: |
  ## Objets connectés
  Semaine 10 - Réception et soudure PCB

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

Semaine 10 - Réception et soudure PCB

<div class="pt-12">
  <span class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Francis Poisson - Cégep Limoilou - H26
  </span>
</div>

---
layout: section
---

# Le grand jour!
## Vos PCB sont arrivés

---

# Parcours du PCB

### De la conception à la réalité

<v-click>

```mermaid {scale: 0.5}
graph LR
    A[Schéma KiCad] --> B[Routage PCB]
    B --> C[Fichiers Gerber]
    C --> D[Envoi fabricant]
    D --> E[Fabrication]
    E --> F[Livraison]
    F --> G[Inspection]
    G --> H[Soudure]
    H --> I[Tests]

    style F fill:#6f6,stroke:#333,stroke-width:2px
    style G fill:#f96
    style H fill:#69f
```

</v-click>

<v-click>

<div class="mt-4 p-2 bg-green-500 bg-opacity-20 rounded-lg text-center">

**Aujourd'hui** : Inspection → Soudure → Tests

</div>

</v-click>

---
layout: section
---

# Partie 1
## Inspection des PCB

---

# Critères de qualité visuelle

### Ce qu'il faut vérifier

<div class="grid grid-cols-2 gap-4">

<div>

<v-click>

### Surface du PCB

- Couleur uniforme du masque
- Pas de rayures profondes
- Sérigraphie lisible
- Finition des pads (HASL/ENIG)

</v-click>

<v-click>

### Pistes et cuivre

- Pistes continues (pas de coupures)
- Largeur constante
- Pas de courts-circuits visibles
- Isolation entre pistes

</v-click>

</div>

<div>

<v-click>

### Perçages

- Trous centrés dans les pads
- Diamètre correct
- Pas de bavures
- Métallisation des vias

</v-click>

<v-click>

### Dimensions

- Contour conforme au design
- Épaisseur correcte (1.6mm)
- Trous de montage présents

</v-click>

</div>

</div>

---

# Défauts courants

### Ce qui peut mal tourner

<v-click>

| Défaut | Cause possible | Action |
|--------|----------------|--------|
| Piste coupée | Erreur fabrication | Fil de pontage |
| Court-circuit | Bavure de cuivre | Gratter au cutter |
| Trou décentré | Tolérance fab | Agrandir si nécessaire |
| Pad décollé | Surchauffe | Réparer ou contourner |
| Masque manquant | Défaut fab | Acceptable si mineur |

</v-click>

<v-click>

<div class="mt-4 p-2 bg-orange-500 bg-opacity-20 rounded-lg text-center text-sm">

**La plupart des défauts mineurs peuvent être corrigés!** Ne paniquez pas.

</div>

</v-click>

---

# Checklist d'inspection

### Avant de commencer la soudure

<div class="grid grid-cols-2 gap-4 text-sm">

<div>

### Inspection visuelle

- [ ] Masque de soudure intact
- [ ] Sérigraphie lisible
- [ ] Pistes continues
- [ ] Pas de courts-circuits apparents

</div>

<div>

### Vérifications physiques

- [ ] Dimensions correctes
- [ ] Trous traversants OK
- [ ] Ajustement avec LilyGO
- [ ] Composants disponibles

</div>

</div>

<v-click>

### Test de continuité préliminaire

```
Multimètre en mode continuité:
- Vérifier GND continu
- Vérifier VCC continu
- Confirmer absence de court GND-VCC
```

</v-click>

---
layout: section
---

# Partie 2
## Techniques de soudure

---

# Équipement de soudure

### Matériel nécessaire

<div class="grid grid-cols-2 gap-6">

<div>

<v-click>

### Outils essentiels

- **Fer à souder** : 25-40W, pointe fine
- **Étain** : 0.8mm, avec flux (60/40 ou sans plomb)
- **Éponge humide** : Nettoyage de la panne
- **Support** : Pour poser le fer
- **Pince coupante** : Couper les pattes
- **Pince plate** : Tenir les composants

</v-click>

</div>

<div>

<v-click>

### Équipements optionnels

- **Loupe** ou lampe-loupe
- **Troisième main** : Maintenir le PCB
- **Flux** : Pour reprises
- **Pompe à dessouder** : Corrections
- **Tresse à dessouder** : Enlever l'excès

</v-click>

</div>

</div>

---

# Préparation du poste

### Avant de commencer

<v-clicks>

1. **Ventilation** : Travaillez dans un endroit aéré
2. **Éclairage** : Lumière directe sur le PCB
3. **Organisation** : Composants triés et identifiés
4. **Préchauffage** : Fer à ~350°C (sans plomb) ou ~320°C (plomb)
5. **Nettoyage** : Panne propre et étamée

</v-clicks>

<v-click>

<div class="mt-4 p-2 bg-red-500 bg-opacity-20 rounded-lg text-center text-sm">

**Sécurité** : Ne pas inhaler les fumées! Lavez-vous les mains après (surtout avec étain au plomb).

</div>

</v-click>

---

# Technique de soudure THT

### Composants traversants (Through-Hole)

<v-click>

### Les 5 étapes

```
1. INSÉRER    2. PLIER      3. CHAUFFER   4. APPLIQUER  5. RETIRER
   │             │             │             │             │
   ▼             ▼             ▼             ▼             ▼
┌─────┐      ┌─────┐      ┌─────┐      ┌─────┐      ┌─────┐
│  │  │      │  ╲  │      │  ╲  │ ←Fer │  ╲  │ ←Soudure  ●  │
│  │  │      │   ╲ │      │   ╲ │      │   ● │      │  ●  │
├──┼──┤      ├───╲─┤      ├───╲─┤      ├───●─┤      ├──●──┤
│  │  │      │    │       │    │       │    │       │     │
└──┴──┘      └────┘       └────┘       └────┘       └─────┘
```

</v-click>

<v-click>

### Temps de contact

- **2-3 secondes** : Suffisant pour une bonne soudure
- **> 5 secondes** : Risque de surchauffe du composant
- L'étain doit **couler** et former un cône brillant

</v-click>

---

# Bonne vs mauvaise soudure

### Reconnaître la qualité

<v-click>

```
BONNE SOUDURE          FROIDE              INSUFFISANTE        EXCÈS
     ●                   ○                     ○                 ●●
    ╱│╲                 ╱│╲                   │                 ╱│╲
   ╱ │ ╲               ╱ │ ╲                  │                ╱ │ ╲
──╱──┴──╲──          ─╱──┴──╲─            ───┴───            ╱──┴──╲
                      (terne)            (pas assez)        (trop/pont)
```

</v-click>

<v-click>

| Type | Apparence | Cause | Solution |
|------|-----------|-------|----------|
| Bonne | Brillante, conique | - | - |
| Froide | Terne, granuleuse | Pas assez chaud | Refaire |
| Insuffisante | Pas de cône | Pas assez d'étain | Ajouter |
| Excès | Boule, pont | Trop d'étain | Pompe/tresse |

</v-click>

---

# Ordre d'assemblage

### Stratégie recommandée

<v-clicks>

1. **Composants les plus bas** d'abord
   - Résistances
   - Diodes (attention polarité!)

2. **Composants moyens**
   - Condensateurs (polarité si électrolytique)
   - Circuits intégrés (sockets recommandés)

3. **Composants hauts**
   - LEDs (polarité!)
   - Boutons
   - Potentiomètres

4. **Connecteurs** en dernier
   - Headers
   - Borniers

</v-clicks>

---

# Attention aux polarités!

### Composants polarisés

<div class="grid grid-cols-2 gap-6">

<div>

<v-click>

### LED

```
    Anode (+)  Cathode (-)
       │          │
       │    ┌─────┤ (patte courte)
       └────┤     │
            │  ▼  │
            └─────┘
              │
           (méplat)
```

- Patte **longue** = Anode (+)
- **Méplat** = Cathode (-)

</v-click>

</div>

<div>

<v-click>

### Condensateur électrolytique

```
        (-) │ │ (+)
    bande → │█│
            │█│
            └─┘
```

- **Bande** = Négatif (-)
- Patte **longue** = Positif (+)

</v-click>

</div>

</div>

<v-click>

<div class="mt-4 p-2 bg-red-500 bg-opacity-20 rounded-lg text-center text-sm">

**Polarité inversée = composant grillé!** Vérifiez AVANT de souder.

</div>

</v-click>

---

# Soudure des headers

### Astuce pour l'alignement

<v-click>

### Méthode recommandée

1. Insérer le header dans le PCB
2. **Retourner** sur une surface plane
3. Souder **1 seule broche** d'abord
4. Vérifier l'alignement (90°)
5. Ajuster si nécessaire en réchauffant
6. Souder les autres broches

</v-click>

<v-click>

### Pour le shield LilyGO

- Utiliser le LilyGO comme **gabarit d'alignement**
- Insérer les headers dans le LilyGO
- Poser le PCB par-dessus
- Souder quelques points
- Retirer délicatement
- Finir les soudures

</v-click>

---
layout: section
---

# Partie 3
## Tests électriques

---

# Test de continuité

### Avant d'alimenter!

<v-click>

### Étape 1 : Vérifier l'absence de courts-circuits

```
Multimètre en mode continuité (🔊)

Test GND-VCC : Doit être OUVERT (pas de bip)
Test GND-GND : Doit être FERMÉ (bip continu)
Test VCC-VCC : Doit être FERMÉ (bip continu)
```

</v-click>

<v-click>

### Étape 2 : Vérifier les connexions critiques

- GPIO vers composants
- I2C (SDA, SCL) vers accéléromètre
- Résistances vers LEDs
- Boutons vers GPIO

</v-click>

<v-click>

<div class="mt-2 p-2 bg-red-500 bg-opacity-20 rounded-lg text-center text-sm">

**JAMAIS alimenter avant d'avoir vérifié l'absence de court-circuit GND-VCC!**

</div>

</v-click>

---

# Tests fonctionnels progressifs

### Approche méthodique

<v-clicks>

1. **Alimentation seule**
   - Brancher le LilyGO
   - Vérifier les tensions (3.3V, GND)
   - Pas de composants qui chauffent?

2. **LEDs**
   - Code simple : allumer chaque LED
   - Vérifier la luminosité correcte

3. **Boutons**
   - Code de lecture d'entrée
   - Vérifier pull-up/pull-down

4. **Potentiomètres**
   - Lecture ADC
   - Vérifier la plage complète (0-4095)

5. **Accéléromètre**
   - Scan I2C (`Wire.begin(); scanner...`)
   - Lecture des axes X, Y, Z

</v-clicks>

---

# Code de test rapide

### Validation de base

```cpp {all|1-8|10-18|20-26}
// Test LEDs
void testLEDs() {
  for (int pin : {LED1_PIN, LED2_PIN}) {
    digitalWrite(pin, HIGH);
    delay(500);
    digitalWrite(pin, LOW);
  }
}

// Test Boutons
void testButtons() {
  Serial.print("BTN1: ");
  Serial.println(digitalRead(BTN1_PIN));
  Serial.print("BTN2: ");
  Serial.println(digitalRead(BTN2_PIN));
}

// Test Potentiomètres
void testPots() {
  Serial.print("POT1: ");
  Serial.println(analogRead(POT1_PIN));
  Serial.print("POT2: ");
  Serial.println(analogRead(POT2_PIN));
}
```

---

# Scan I2C

### Trouver l'accéléromètre

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);  // SDA, SCL du LilyGO

  Serial.println("Scan I2C...");
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Trouvé à 0x");
      Serial.println(addr, HEX);
    }
  }
  Serial.println("Scan terminé.");
}

void loop() {}
```

<v-click>

<div class="mt-2 p-2 bg-green-500 bg-opacity-20 rounded-lg text-center text-sm">

**Adresse typique MPU6050** : 0x68 ou 0x69

</div>

</v-click>

---

# Dépannage courant

### Problèmes et solutions

<v-click>

| Problème | Cause probable | Solution |
|----------|----------------|----------|
| LED ne s'allume pas | Polarité inversée | Vérifier/ressouder |
| LED toujours allumée | Court-circuit | Vérifier les soudures |
| Bouton ne répond pas | Mauvaise soudure | Refaire la soudure |
| ADC bloqué à 0 | Pas de connexion | Vérifier continuité |
| ADC bloqué à 4095 | Court vers VCC | Vérifier les ponts |
| I2C non détecté | SDA/SCL inversés | Vérifier le câblage |
| Composant chauffe | Court-circuit | Débrancher immédiatement! |

</v-click>

---
layout: section
---

# Travail de la semaine
## Assemblage et validation

---

# Objectifs du laboratoire

### Transformer votre PCB en système fonctionnel

<div class="grid grid-cols-2 gap-4">

<div>

### Assemblage (2h)

<v-clicks>

- [ ] Inspection du PCB reçu
- [ ] Test de continuité préliminaire
- [ ] Soudure des résistances
- [ ] Soudure des LEDs (polarité!)
- [ ] Soudure des boutons
- [ ] Soudure des potentiomètres
- [ ] Soudure de l'accéléromètre
- [ ] Soudure des headers

</v-clicks>

</div>

<div>

### Tests (1h)

<v-clicks>

- [ ] Test de continuité final
- [ ] Vérification absence court-circuit
- [ ] Test des LEDs
- [ ] Test des boutons
- [ ] Test des potentiomètres
- [ ] Test I2C (accéléromètre)
- [ ] Documentation des résultats

</v-clicks>

</div>

</div>

---

# En cas de problème

### Ne paniquez pas!

<v-click>

### Ressources disponibles

- **Enseignant** : Pour les problèmes complexes
- **Collègues** : Entraide encouragée
- **Composants de rechange** : Disponibles
- **Outils de correction** : Pompe, tresse, flux

</v-click>

<v-click>

### Erreurs rattrapables

- Soudure froide → Refaire
- Pont de soudure → Tresse à dessouder
- Composant inversé → Dessouder et retourner
- Piste coupée → Fil de pontage

</v-click>

<v-click>

<div class="mt-4 p-2 bg-blue-500 bg-opacity-20 rounded-lg text-center text-sm">

**L'apprentissage passe par les erreurs!** C'est normal de devoir corriger.

</div>

</v-click>

---
layout: center
class: text-center
---

# Questions?

<div class="text-xl mt-8">
Prochaine étape : Assembler votre PCB!
</div>

<div class="mt-4 text-sm">
Semaine prochaine : Automatisation LLM et pipelines de données
</div>

---
layout: end
---

# Merci!

243-4J5-LI - Objets connectés

Semaine 10
