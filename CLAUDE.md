Guide du projet - Cours techniques
Ce projet contient du matériel pédagogique pour des cours techniques : présentations théoriques (Slidev) et documents de laboratoire.

Structure du projet
/
├── theorie/
│   └── Semaine-XX/
│       ├── notes/           # Plans de séquence, notes de cours
│       ├── diaporama/       # Présentation Slidev
│       │   ├── slides.md
│       │   ├── components/  # Composants Vue interactifs
│       │   └── public/      # Images et ressources
│       └── exercices/       # Exercices et problèmes
│
├── labo/
│   └── Labo-XX/
│       └── Laboratoire XX - *.md
│
├── evaluations/             # Évaluations sommatives et formatives
│   └── Evaluation-XX/
│       └── *.md
│
├── moodle/                  # Contenus pour Moodle (source)
│   └── resumes-hebdomadaires.md
│
├── docs/                    # GitHub Pages
│   ├── index.md
│   └── moodle/              # Résumés HTML par semaine
│       ├── index.md
│       └── semaine-XX.html
│
├── Plan de cours - *.md     # Plan de cours global
└── CLAUDE.md
Présentations Slidev (diaporama/)
Gestionnaire de paquets
Utiliser **pnpm** pour toutes les opérations liées aux diaporamas Slidev :
```bash
# Installation des dépendances
pnpm install

# Lancement du serveur de développement
pnpm dev

# Build pour production
pnpm build
```

Composants Vue interactifs
Les composants interactifs doivent être optimisés pour l'affichage en présentation (résolution 1920x1080, ratio 16:9).

Dimensions et mise en page
Conteneur principal : Utiliser flexbox avec gap: 8-10px
Graphiques SVG : Dimensions recommandées 300-450px, jamais plus de 500px de hauteur
Panneaux de contrôle : Largeur fixe 140-200px pour éviter les débordements
Padding global : 4-8px pour maximiser l'espace utile
Tailles de police dans les SVG
Les tailles doivent être proportionnelles au viewBox, pas à l'affichage CSS :

Élément	Taille recommandée
Titres principaux	4-5
Labels d'axes	5-6
Valeurs numériques	3.5-5
Annotations	3-4
Éléments SVG
Traits d'axes : stroke-width="1"
Vecteurs/lignes importantes : stroke-width="1.5-2"
Grilles : stroke-width="0.5", couleur #e8e8e8
Points interactifs : rayon r="4-6"
Marqueurs de flèches : markerWidth="6" markerHeight="4"
Contrôles interactifs
/* Sliders */
input[type="range"] {
  width: 100%;
  height: 4px;
}

/* Boutons */
button {
  padding: 4-6px 8px;
  font-size: 10px;
  border-radius: 4px;
}

/* Labels */
label {
  font-size: 9-10px;
}
Structure CSS type
<style scoped>
.demo-container {
  font-family: 'Segoe UI', system-ui, sans-serif;
  padding: 4px;
  background: #fafafa;
  border-radius: 8px;
  font-size: 10px;
}

.main-container {
  display: flex;
  gap: 8-10px;
}

.graph-area {
  flex: 1;
  min-width: 300px;
}

.controls {
  width: 150px;
  flex-shrink: 0;
}

.section {
  background: white;
  padding: 5px;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  margin-bottom: 4px;
}

.section h4 {
  margin: 0 0 3px 0;
  font-size: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 2px;
}
</style>
Palette de couleurs
Usage	Couleur	Hex
Principal/Vecteurs	Bleu	#2196F3
Positif/Succès	Vert	#4CAF50
Négatif/Erreur	Rouge	#F44336
Avertissement	Orange	#FF9800
Accent/Angle	Violet	#9C27B0
Texte principal	Gris foncé	#333
Texte secondaire	Gris	#666
Bordures	Gris clair	#ddd
Fond sections	Blanc	#fff
Fond général	Gris très clair	#fafafa
Bonnes pratiques Slidev
Utiliser <style scoped> pour isoler les styles
Préfixer les IDs SVG avec le nom du composant pour éviter les conflits
Utiliser Vue 3 Composition API (<script setup>)
Limiter les animations CSS pour la performance
Tester sur la résolution cible (1920x1080)
Documents de laboratoire (labo/)
Format Markdown
Les laboratoires utilisent le format Markdown avec :

En-tête : titre, objectifs, matériel
Sections numérotées : Introduction, Matériel, Procédure, Questions
Formules : Notation LaTeX entre $...$ ou $$...$$
Tableaux : Format Markdown standard pour les mesures
Images : Stockées dans le même dossier ou sous-dossier images/
Structure type d'un laboratoire
# Laboratoire XX - Titre

## Objectifs
- Objectif 1
- Objectif 2

## Matériel requis
- Équipement 1
- Équipement 2

## Théorie
Rappels théoriques avec formules.

## Procédure

### Partie 1 : Titre
1. Étape 1
2. Étape 2

### Partie 2 : Titre
...

## Questions d'analyse
1. Question 1
2. Question 2

## Annexes (si nécessaire)
Conventions pour les formules
Utiliser j (pas i) pour l'unité imaginaire en électronique
Angles en degrés avec symbole °
Unités SI avec espaces : 50 Ω, 155 MHz
Notation ingénieur pour les grands/petits nombres
Notes de cours (notes/)
Les plans de séquence et notes de cours suivent ce format :

# Plan de séquence - Semaine XX

## Objectifs de la semaine
- Objectif 1
- Objectif 2

## Contenu théorique
### Thème 1
...

### Thème 2
...

## Activités
- Activité 1
- Activité 2

## Évaluation
...

Évaluations (evaluations/)
Les évaluations sont organisées par dossier dans `evaluations/Evaluation-XX/`.

Structure type d'une évaluation
# Évaluation XX - Titre

## Informations
- **Date** : JJ/MM/AAAA
- **Durée** : XX minutes
- **Pondération** : XX%
- **Documents permis** : ...

## Objectifs évalués
- Objectif 1
- Objectif 2

## Questions

### Question 1 (XX points)
...

### Question 2 (XX points)
...

## Barème de correction
...

Conventions générales
Langue
Contenu en français
Toujours utiliser les accents français (é, è, ê, à, ù, ç, etc.) dans tous les fichiers, y compris les fichiers HTML
Termes techniques anglais acceptés entre parenthèses si nécessaire
Pas d'emojis sauf si explicitement demandé
Nommage des fichiers
Semaines : Semaine-XX/ (avec zéro de remplissage)
Laboratoires : Labo-XX/Laboratoire XX - Titre descriptif.md
Évaluations : Evaluation-XX/Evaluation XX - Titre descriptif.md
Composants Vue : PascalCase.vue (ex: SmithChartDemo.vue)
Images : kebab-case.png
Git
Commits en français
Messages descriptifs du contenu modifié
Un commit par fonctionnalité/correction logique

## Textes Moodle

### Résumé hebdomadaire pour Moodle

Lors de la création d'un résumé de semaine pour Moodle, générer un texte HTML structuré respectant ces critères :

- **Format** : Bloc `<div>` avec style de police, contenant paragraphes et listes
- **Structure** : Introduction, liste de concepts clés, paragraphes thématiques, résumé du labo, **section "À faire pour la semaine prochaine"**
- **Style** : Police Segoe UI, line-height 1.6
- **Contenu** : Résumer les concepts clés de la présentation Slidev de la semaine
- **Mise en forme** : Utiliser `<strong>` pour les termes techniques, tirets cadratins (—) dans les listes
- **Source** : Se baser sur le fichier `theorie/Semaine-XX/diaporama/slides.md`
- **Destination** : Ajouter dans `moodle/resumes-hebdomadaires.md`

#### Sections obligatoires

1. **Introduction** : Paragraphe d'accroche avec les concepts principaux en gras
2. **Concepts clés** : Listes à puces thématiques
3. **Labo** : Résumé des activités pratiques
4. **À faire pour la semaine prochaine** : Liste des préparations requises (sauf semaine 15)
5. **Prochaine évaluation** : Informations sur l'évaluation à venir (si applicable)

#### Exemple

```html
<div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.6;">
  <p>Introduction au protocole <strong>MQTT</strong>, le standard de communication pour l'IoT. Architecture <strong>publish/subscribe</strong> avec découplage spatial et temporel.</p>
  <p><strong>Concepts clés :</strong></p>
  <ul style="margin: 10px 0;">
    <li><strong>Topics hiérarchiques</strong> — structure avec séparateur /</li>
    <li><strong>QoS</strong> — trois niveaux de fiabilité (0, 1, 2)</li>
  </ul>
  <p><strong>Labo :</strong> configurer Mosquitto et établir une communication bidirectionnelle.</p>
  <div style="margin-top: 15px; padding: 10px; background: #e3f2fd; border-left: 4px solid #2196F3; border-radius: 4px;">
    <p style="margin: 0 0 8px 0;"><strong>À faire pour la semaine prochaine :</strong></p>
    <ul style="margin: 0; padding-left: 20px;">
      <li>Finaliser la communication MQTT bidirectionnelle</li>
      <li>Préparer le montage breadboard (LEDs, boutons)</li>
      <li>Se préparer pour l'évaluation sommative</li>
    </ul>
  </div>
  <p style="margin-top: 15px; padding: 10px; background: #fff3e0; border-left: 4px solid #ff9800; border-radius: 4px;">
    <strong>Prochaine évaluation :</strong> Évaluation sommative 2 — semaine 10<br>
    <em>Matière couverte :</em> MQTT, topics, QoS, communication bidirectionnelle<br>
    <em>Format :</em> Démonstration pratique (30 min)
  </p>
</div>
```

## Plan de cours

Le fichier `Plan de cours - 243-4J5-LI.md` suit une structure standardisée.

### Structure de l'en-tête

L'en-tête utilise des titres H3 suivis de tableaux à 2 colonnes (pas de titre H1) :

```markdown
### Cours

| | |
|---|---|
| **Numéro** | 243-4J5-LI |
| **Titre** | Objets connectés |
| **Session** | H26 |

### Structure

| | |
|---|---|
| **Pondération** | 2-3-2 |
| **Unités** | 2.33 |

### Organisation

| | |
|---|---|
| **Département** | ... |
| **Programme** | ... |
| **Établissement** | ... |

### Contact

| | |
|---|---|
| **Enseignant** | ... |
```

### Section 2.1 — Apprentissages clés

Les capacités utilisent un tableau à 3 colonnes avec les éléments alignés :

```markdown
#### Capacité X : Titre (XX%)

| Savoirs | Savoir-faire | Savoir-être |
|---------|--------------|-------------|
| • Élément 1 | • Élément 1 | • Élément 1 |
| • Élément 2 | • Élément 2 | • Élément 2 |
| • Élément 3 | • Élément 3 | |
```

### Section 3.2 — Évaluation sommative

Les tableaux d'évaluation utilisent 3 colonnes côte à côte :

```markdown
| Cible (Niveau optimal) | Seuil de réussite (Niveau minimal) | Méthodes d'évaluation |
|------------------------|-----------------------------------|----------------------|
| • Critère cible 1 | • Critère seuil 1 | • Méthode 1 |
| • Critère cible 2 | • Critère seuil 2 | • Méthode 2 |
```

- Chaque critère sur sa propre ligne pour faciliter la comparaison
- Les méthodes d'évaluation uniquement dans les premières lignes
- Cellules vides permises pour l'alignement

### Grilles d'évaluation

Les grilles d'évaluation utilisent une **échelle de notation de 0 à 5** avec des descripteurs alignés sur les capacités et savoir-faire du plan de cours.

#### Échelle de notation standard

| Niveau | Description | Équivalence |
|:------:|-------------|:-----------:|
| **0** | Aucun travail remis ou travail non fonctionnel | 0% |
| **1** | Travail incomplet avec lacunes majeures | 40% |
| **2** | Travail partiel, en dessous du seuil | 50% |
| **3** | **Seuil de réussite** — Exigences minimales atteintes | 60% |
| **4** | Travail de bonne qualité, au-delà des attentes | 80% |
| **5** | Travail excellent, niveau optimal atteint | 100% |

#### Structure d'une grille d'évaluation

```markdown
# Grille d'évaluation — Titre

**Cours:** 243-4Q5-LI – Communication radio
**Évaluation:** Description de l'évaluation
**Pondération totale:** XX% (Capacité X : XX%, Capacité Y : XX%)

---

## Échelle de notation
[Tableau standard ci-dessus]

---

## Partie X : Titre (XX%)

### Critère X.1 : Titre du critère (XX%)

*Capacité X : [Nom de la capacité du plan de cours]*
*Savoir-faire évalué : [Savoir-faire spécifique du plan de cours]*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Description niveau 0 |
| **1** | Description niveau 1 |
| **2** | Description niveau 2 |
| **3** | **Seuil :** Description du seuil de réussite |
| **4** | Description niveau 4 |
| **5** | Description niveau 5 (niveau optimal) |

---

## Tableau récapitulatif

| Partie | Critère | Pondération | Note /5 | Points |
|--------|---------|:-----------:|:-------:|:------:|
| **X. Titre** | X.1 Critère | XX% | /5 | |
| | **TOTAL** | **100%** | | **/100** |

---

## Calcul de la note finale

Pour chaque critère :
$\text{Points} = \text{Note sur 5} \times \frac{\text{Pondération}}{5}$

---

## Correspondance avec les capacités du cours

| Capacité | Critères associés | Pondération |
|----------|-------------------|:-----------:|
| **Capacité X** : Nom | X.1, X.2 | XX% |

---

## Livrables attendus
- [ ] Livrable 1
- [ ] Livrable 2
```

#### Principes de rédaction des descripteurs

- **Niveau 3 (seuil)** : Correspond aux critères du seuil de réussite du plan de cours
- **Niveau 5 (optimal)** : Correspond aux critères de la cible (niveau optimal) du plan de cours
- Chaque critère doit référencer explicitement un savoir-faire du plan de cours
- Les descripteurs doivent être observables et mesurables

## Workflows test-chatkit

Les workflows de laboratoire utilisent le format JSON de test-chatkit (edxo). Les fichiers sont stockés dans le dossier `workflows/`.

### Synchronisation labo/workflow

**IMPORTANT** : Les documents de laboratoire (`labo/`) et leurs workflows associés (`workflows/`) doivent toujours être synchronisés.

- Toute modification à un laboratoire doit être répercutée dans le workflow correspondant
- Toute modification à un workflow doit être répercutée dans le laboratoire correspondant
- Lors d'une demande de modification, toujours vérifier si l'autre document doit être mis à jour
- Nommage cohérent : `Labo-XX/` correspond à `workflows/LaboXX.json`

### Type de questions dans les workflows

**Priorité aux checkpoints techniques (Option A)**

Les questions dans les workflows doivent être axées sur le matériel devant l'étudiant, pas sur la compréhension conceptuelle. Privilégier la validation de l'exécution des tâches.

#### Types de checkpoints techniques (prioritaires)

| Type | Exemple | Validation par l'agent |
|------|---------|------------------------|
| **Sortie de commande** | "Tape `ip -br a` et colle le résultat" | Format, mots-clés, valeurs attendues |
| **Mesure physique** | "Quelle tension mesures-tu aux bornes de R1?" | Valeur dans la plage attendue, unité correcte |
| **Photo/capture** | "Envoie une photo de ton montage" | Présence des composants, connexions visibles |
| **Valeur calculée** | "Quel est le gain mesuré en dB?" | Cohérence avec les mesures précédentes |

#### Critères de validation pour l'agent

L'agent doit vérifier des éléments observables :
- Format de la sortie (colonnes, structure)
- Présence de mots-clés attendus
- Valeurs dans les plages attendues (tensions, courants, fréquences)
- Unités correctes (V, mA, dB, Hz, etc.)
- Cohérence avec le contexte du laboratoire
- Pour les photos : présence des éléments requis du montage

#### Hybride (Option B, si nécessaire)

Si une question d'interprétation est requise, elle doit suivre un checkpoint et porter sur les données spécifiques de l'étudiant :

```
1. Checkpoint: "Quelle tension mesures-tu aux bornes de C1?"
2. Question liée: "Cette valeur correspond-elle à ce que tu attendais? Pourquoi?"
```

**À éviter** : Questions conceptuelles déconnectées du travail en cours
- "Qu'est-ce qu'une adresse IP?"
- "Explique le modèle OSI"
- "Pourquoi utilise-t-on un condensateur de découplage?"

### Structure d'un workflow

Un workflow est composé de deux tableaux principaux : `nodes` (nœuds) et `edges` (connexions).

```json
{
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

### Types de nœuds (kind)

| Kind | Description | Paramètres clés |
|------|-------------|-----------------|
| `start` | Point de départ du workflow | `auto_start` |
| `end` | Point de fin du workflow | `message`, `status.type`, `status.reason` |
| `assistant_message` | Message affiché à l'étudiant | `message`, `simulate_stream_delay_ms` |
| `widget` | Widget interactif (boutons, formulaires) | `widget.slug`, `widget.source`, `widget.variables` |
| `condition` | Branchement conditionnel | `mode`, `path` |
| `wait_for_user_input` | Attente d'une réponse utilisateur | - |
| `agent` | Appel à un agent IA | `model`, `instructions`, `model_provider`, `response_format` |
| `state` | Manipulation de variables d'état | `state[].target`, `state[].expression` |

### Structure d'un nœud

```json
{
  "id": 140,
  "slug": "assistant-message-1764990850626",
  "kind": "assistant_message",
  "display_name": "Message d'introduction",
  "agent_key": null,
  "parent_slug": null,
  "position": 2,
  "is_enabled": true,
  "parameters": {
    "message": "Contenu du message...",
    "simulate_stream_delay_ms": 5
  },
  "metadata": {
    "order": 2
  }
}
```

### Structure d'une connexion (edge)

```json
{
  "id": 150,
  "source": "condition-1764990982539",
  "target": "assistant-message-1764990850626",
  "condition": "true",
  "metadata": {
    "label": "true",
    "order": 2
  }
}
```

### Champs des nœuds

| Champ | Type | Description |
|-------|------|-------------|
| `id` | integer | Identifiant unique |
| `slug` | string | Identifiant textuel unique (référencé par les edges) |
| `kind` | string | Type du nœud (voir tableau ci-dessus) |
| `display_name` | string | Nom affiché dans l'éditeur |
| `position` | integer | Ordre d'affichage |
| `is_enabled` | boolean | Nœud actif ou désactivé |
| `parameters` | object | Configuration spécifique au type |
| `metadata` | object | Métadonnées (ordre, position visuelle) |

### Champs des edges

| Champ | Type | Description |
|-------|------|-------------|
| `id` | integer | Identifiant unique |
| `source` | string | Slug du nœud source |
| `target` | string | Slug du nœud cible |
| `condition` | string/null | Valeur pour les branchements (`"true"`, `"false"`, valeur spécifique) |
| `metadata.label` | string | Label affiché sur la connexion |

### Patterns courants

#### Boucle de validation avec compteur
```
state (init compteur=0) → wait_for_user_input → agent (évaluation)
    → condition (ok?)
        → true: assistant_message (succès)
        → false: state (compteur++) → condition (compteur >= 3?)
            → oui: assistant_message (appeler enseignant)
            → non: agent (rétroaction) → wait_for_user_input (boucle)
```

#### Widget de confirmation
```
widget (bouton "Prêt?") → condition (value)
    → true: continuer
    → autre: end (abandonné)
```

#### Agent avec réponse structurée
```json
{
  "kind": "agent",
  "parameters": {
    "model": "gpt-5-nano",
    "instructions": "Instructions pour l'agent...",
    "model_provider": "openai",
    "response_format": {
      "type": "json_schema",
      "schema": {
        "type": "object",
        "required": ["ok"],
        "properties": {
          "ok": { "type": "boolean" }
        }
      },
      "strict": true
    }
  }
}
```

### Accès aux données dans les conditions

| Path | Description |
|------|-------------|
| `input.action.raw_payload.value.` | Valeur d'un widget |
| `input.user_message` | Message texte de l'utilisateur |
| `input.output_structured.ok` | Réponse structurée d'un agent |
| `state.compteur` | Variable d'état personnalisée |

### Expressions d'état

Les expressions `state[].expression` utilisent la syntaxe Python :
```python
"0"                                    # Valeur littérale
"(state.get('compteur', 0) or 0) + 1" # Incrémentation
