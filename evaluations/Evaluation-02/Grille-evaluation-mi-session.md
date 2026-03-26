# Grille d'évaluation — Projet de mi-session

**Cours:** 243-4J5-LI – Objets connectés
**Évaluation:** Projet de mi-session — Shield PCB pour LilyGO A7670G
**Pondération totale:** 20% (15% Capacité 1 + 5% Capacité 2)

---

## Échelle de notation

| Niveau | Description | Équivalence |
|:------:|-------------|:-----------:|
| **0** | Aucun travail remis ou travail non fonctionnel | 0% |
| **1** | Travail incomplet avec lacunes majeures | 40% |
| **2** | Travail partiel, en dessous du seuil | 50% |
| **3** | **Seuil de réussite** — Exigences minimales atteintes | 60% |
| **4** | Travail de bonne qualité, au-delà des attentes | 80% |
| **5** | Travail excellent, niveau optimal atteint | 100% |

---

## Partie 1 : Shield PCB (30%)

### Critère 1.1 : Schéma électrique (10%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun schéma remis |
| **1** | Schéma incomplet : composants manquants ou symboles incorrects; erreurs ERC majeures non corrigées |
| **2** | Schéma partiellement complet : la majorité des composants présents mais avec des erreurs de connexion; quelques erreurs ERC |
| **3** | **Seuil :** Schéma fonctionnel avec tous les composants assignés (boutons, LEDs, accéléromètre, connecteurs); ERC sans erreurs critiques; connexions logiques correctes |
| **4** | Schéma bien organisé avec labels clairs; annotations pertinentes; hiérarchie logique des connexions; utilisation appropriée des symboles d'alimentation |
| **5** | Schéma professionnel : organisation exemplaire, annotations complètes, valeurs des composants justifiées, documentation des choix de conception |

### Critère 1.2 : Routage PCB (10%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun routage ou fichier PCB non fonctionnel |
| **1** | Routage très incomplet : pistes manquantes, violations DRC majeures, placement anarchique |
| **2** | Routage partiel : la majorité des pistes présentes mais avec des violations DRC; placement non optimisé |
| **3** | **Seuil :** Routage complet avec DRC sans erreurs critiques; placement fonctionnel des composants; largeur de pistes acceptable; plan de masse présent |
| **4** | Routage optimisé : placement logique facilitant l'assemblage; pistes courtes et directes; bon découplage; contour de carte approprié |
| **5** | Routage professionnel : optimisation de l'espace, séparation signaux analogiques/numériques, silkscreen informatif, design for manufacturing respecté |

### Critère 1.3 : Fichiers de fabrication (5%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun fichier de fabrication généré |
| **1** | Fichiers Gerbers incomplets ou corrompus; BOM absente |
| **2** | Gerbers générés mais avec couches manquantes; BOM incomplète |
| **3** | **Seuil :** Gerbers complets et valides (toutes les couches nécessaires); BOM avec références et quantités; fichiers prêts pour fabrication |
| **4** | Fichiers bien organisés dans un dossier dédié; BOM avec fournisseurs suggérés; fichier README explicatif |
| **5** | Package de fabrication professionnel : Gerbers vérifiés, BOM détaillée avec alternatives, instructions d'assemblage, rendu 3D inclus |

### Critère 1.4 : Prototype breadboard (5%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun prototype réalisé |
| **1** | Prototype non fonctionnel; composants mal connectés |
| **2** | Prototype partiellement fonctionnel; certains composants ne répondent pas |
| **3** | **Seuil :** Prototype fonctionnel avec tous les composants assignés opérationnels; câblage identifiable; communication I2C avec l'accéléromètre validée |
| **4** | Prototype soigné avec câblage organisé par couleur; étiquetage des connexions; facilement reproductible |
| **5** | Prototype exemplaire : montage professionnel, documentation photographique, schéma de câblage annoté |

---

## Partie 2 : Programme embarqué (30%)

### Critère 2.1 : Lecture des capteurs (10%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun code de lecture des capteurs |
| **1** | Code non fonctionnel; erreurs de compilation ou d'exécution |
| **2** | Lecture partielle : seulement certains capteurs fonctionnent (ex: boutons OK mais pas accéléromètre) |
| **3** | **Seuil :** Lecture fonctionnelle de tous les capteurs assignés; état des boutons détecté; données de l'accéléromètre (X, Y, Z) lues correctement |
| **4** | Lecture robuste avec debouncing des boutons; calibration de l'accéléromètre; gestion des erreurs de lecture |
| **5** | Code optimisé : interruptions pour les boutons, filtrage des données accéléromètre, détection d'événements (secousse, inclinaison) |

### Critère 2.2 : Contrôle des actionneurs (5%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun contrôle des LEDs |
| **1** | Code non fonctionnel; LEDs ne répondent pas |
| **2** | Contrôle partiel : certaines LEDs fonctionnent, pas toutes |
| **3** | **Seuil :** Toutes les LEDs assignées contrôlables (ON/OFF); réponse aux commandes MQTT |
| **4** | Contrôle avancé : PWM pour variation d'intensité; patterns lumineux; feedback visuel de l'état système |
| **5** | Contrôle sophistiqué : animations, séquences programmables, intégration complète avec la logique applicative |

### Critère 2.3 : Communication MQTT (15%)

*Capacité 2 : Maîtriser les protocoles de communication IdO*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucune communication MQTT implémentée |
| **1** | Connexion au broker échoue; erreurs de protocole |
| **2** | Connexion établie mais communication unidirectionnelle seulement (publication OU souscription) |
| **3** | **Seuil :** Communication bidirectionnelle fonctionnelle via LTE; publication des données capteurs; réception des commandes pour LEDs; structure de topics cohérente |
| **4** | Communication robuste : reconnexion automatique, QoS approprié, format JSON bien structuré, gestion des erreurs réseau |
| **5** | Communication optimale : TLS/WSS sécurisé, heartbeat/status régulier, gestion complète des déconnexions, topics bien documentés |

---

## Partie 3 : Interface Raspberry Pi (20%)

### Critère 3.1 : Affichage des données (10%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucune interface développée |
| **1** | Interface ne s'exécute pas ou n'affiche rien |
| **2** | Affichage partiel : certaines données seulement; mise à jour incohérente |
| **3** | **Seuil :** Interface fonctionnelle affichant l'état des boutons et les données de l'accéléromètre en temps réel; mise à jour automatique via MQTT |
| **4** | Interface bien conçue : visualisation claire (jauges, graphiques), disposition ergonomique, feedback visuel des changements |
| **5** | Interface professionnelle : design soigné, animations fluides, historique des données, adaptation à l'écran tactile optimale |

### Critère 3.2 : Contrôle des actionneurs (5%)

*Capacité 2 : Maîtriser les protocoles de communication IdO*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucun contrôle depuis l'interface |
| **1** | Boutons de contrôle présents mais non fonctionnels |
| **2** | Contrôle partiel : certaines LEDs contrôlables, pas toutes |
| **3** | **Seuil :** Boutons tactiles permettant de contrôler toutes les LEDs à distance; feedback visuel de l'état actuel |
| **4** | Contrôle avancé : sliders pour PWM, boutons avec états visuels, confirmation des commandes |
| **5** | Contrôle sophistiqué : scénarios préprogrammés, interface intuitive, gestion des erreurs de communication |

### Critère 3.3 : Logique applicative (5%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucune logique applicative |
| **1** | Logique présente mais non fonctionnelle |
| **2** | Logique basique : affichage simple sans interactivité significative |
| **3** | **Seuil :** Application cohérente avec le projet choisi; utilisation pertinente des boutons, LEDs et accéléromètre; interaction fonctionnelle |
| **4** | Application bien pensée : expérience utilisateur fluide, cas d'utilisation complets, feedback approprié |
| **5** | Application créative et aboutie : concept original, utilisation innovante des capteurs, expérience engageante |

---

## Partie 4 : Documentation (20%)

### Critère 4.1 : README et description du projet (8%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucune documentation |
| **1** | README minimal sans informations utiles |
| **2** | Documentation incomplète : description vague, instructions manquantes |
| **3** | **Seuil :** README complet avec description du projet, instructions d'installation, dépendances listées, structure des fichiers expliquée |
| **4** | Documentation claire et bien structurée : schémas inclus, exemples d'utilisation, troubleshooting de base |
| **5** | Documentation exemplaire : guide complet, captures d'écran, vidéo de démonstration, FAQ |

### Critère 4.2 : Documentation technique (8%)

*Capacité 1 : Concevoir et programmer des objets connectés*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Aucune documentation technique |
| **1** | Documentation technique très insuffisante |
| **2** | Documentation partielle : schémas présents mais non annotés; brochage incomplet |
| **3** | **Seuil :** Schéma électrique exporté, brochage GPIO documenté, topics MQTT listés, BOM complète |
| **4** | Documentation technique détaillée : justification des choix, calculs (résistances LEDs), diagramme de flux |
| **5** | Documentation professionnelle : datasheet personnalisée, guide de dépannage, analyse des performances |

### Critère 4.3 : Qualité du français (4%)

*Expression et communication en français*

| Niveau | Descripteur |
|:------:|-------------|
| **0** | Texte illisible ou en langue étrangère uniquement |
| **1** | Nombreuses fautes nuisant à la compréhension; structure incohérente |
| **2** | Fautes fréquentes mais texte compréhensible; organisation déficiente |
| **3** | **Seuil :** Français acceptable avec quelques fautes mineures; texte clair et structuré; termes techniques appropriés |
| **4** | Français de bonne qualité; texte bien rédigé et organisé; vocabulaire technique précis |
| **5** | Français excellent; rédaction professionnelle; aucune faute; style clair et concis |

---

## Tableau récapitulatif

| Partie | Critère | Pondération | Note /5 | Points |
|--------|---------|:-----------:|:-------:|:------:|
| **1. Shield PCB** | 1.1 Schéma électrique | 10% | /5 | |
| | 1.2 Routage PCB | 10% | /5 | |
| | 1.3 Fichiers de fabrication | 5% | /5 | |
| | 1.4 Prototype breadboard | 5% | /5 | |
| **2. Programme embarqué** | 2.1 Lecture des capteurs | 10% | /5 | |
| | 2.2 Contrôle des actionneurs | 5% | /5 | |
| | 2.3 Communication MQTT | 15% | /5 | |
| **3. Interface RPi** | 3.1 Affichage des données | 10% | /5 | |
| | 3.2 Contrôle des actionneurs | 5% | /5 | |
| | 3.3 Logique applicative | 5% | /5 | |
| **4. Documentation** | 4.1 README et description | 8% | /5 | |
| | 4.2 Documentation technique | 8% | /5 | |
| | 4.3 Qualité du français | 4% | /5 | |
| | **TOTAL** | **100%** | | **/100** |

---

## Calcul de la note finale

Pour chaque critère :
$$\text{Points} = \text{Note sur 5} \times \frac{\text{Pondération}}{5}$$

**Exemple :** Critère 2.3 Communication MQTT (15%), note 4/5
$$\text{Points} = 4 \times \frac{15}{5} = 4 \times 3 = 12 \text{ points}$$

**Note finale du projet :** Somme des points sur 100, puis ×0.20 pour la pondération dans le cours.

---

## Correspondance avec les capacités du cours

| Capacité | Critères associés | Pondération |
|----------|-------------------|:-----------:|
| **Capacité 1** : Concevoir et programmer des objets connectés | 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 3.1, 3.3, 4.1, 4.2 | ~65% |
| **Capacité 2** : Maîtriser les protocoles de communication IdO | 2.3, 3.2 | ~20% |
| **Expression française** | 4.3 | ~4% |

---

**Date de remise :** 23 mars 2026 à 8h00 (lundi matin)

> **Important :** Les fichiers Gerber (PCB) doivent être remis au plus tard le **lundi 16 mars 2026 à 8h00**. Une note de **0** sera appliquée pour les critères 1.2 et 1.3 (Routage PCB et Fichiers de fabrication) si les Gerbers ne sont pas remis à temps, car la commande groupée des PCB est passée ce matin-là.

**Mode de remise :** Git (branche `prenom-nom/projet-mi-session`)
