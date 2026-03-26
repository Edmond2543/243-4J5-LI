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
| **Département** | Technologie du génie électrique |
| **Programme** | Technologie du génie électrique : Réseaux et télécommunications |
| **Établissement** | Cégep Limoilou |

### Contact

| | |
|---|---|
| **Enseignant** | Francis Poisson |

---

## 1. PRÉSENTATION DU COURS

Ce cours, de quatrième session, vous permettra de concevoir et programmer des objets connectés dans le cadre du programme de Technologie du génie électrique : Réseaux et télécommunications, au sein du fil conducteur « Systèmes électroniques ». Il s'appuie sur les acquis des cours de systèmes analogiques, numériques, signaux analogiques, communication numérique ainsi que signaux radio et modulations. Il vise à développer les capacités suivantes : Concevoir et programmer des objets connectés et Maîtriser les protocoles de communication IdO, afin de réaliser des systèmes IdO intégrés et déployables en réseau.

Vous serez amené à intégrer des circuits électroniques, à programmer en Python, à mettre en œuvre des protocoles tels que MQTT et HTTP, à sécuriser les échanges de données et à conduire un projet complet allant jusqu'à la préparation d'un PCB et la mise en service dans un environnement de télécommunications.

### Place et rôle du cours dans le programme

Le cours "243-4J5-LI – Objets connectés" s'inscrit en tant que cours du fil conducteur "Systèmes électroniques" dans le programme de Technologie du génie électrique : Réseaux et télécommunications. Il occupe la session 4 de la grille de cours.

Au cours des sessions précédentes, les personnes étudiantes ont acquis des connaissances fondamentales dans plusieurs domaines clés:

- **Session 1:**
  - 243-1J5-LI – Systèmes analogiques: principes de base des circuits analogiques
  - 243-1N5-LI – Systèmes numériques: compréhension des systèmes numériques et leur fonctionnement

- **Session 2:**
  - 243-2J5-LI – Signaux analogiques: approfondissement de la compréhension des signaux analogiques
  - 243-2N5-LI – Communication numérique: principes des communications numériques

- **Session 3:**
  - 243-3J5-LI – Signaux radio et modulations: techniques de modulation radio

Ces connaissances préalables sont essentielles pour aborder les sujets avancés du cours "Objets connectés".

### Objectif terminal du cours

À la fin de ce cours, vous serez capable de concevoir et programmer des objets connectés en intégrant des circuits électroniques, d'analyser les informations techniques et d'assurer leur installation et leur mise en service dans des réseaux de télécommunications.

---

## 2. ORGANISATION DU COURS

### 2.1 Apprentissages clés (capacités, thèmes et contenu)

#### Capacité 1 : Concevoir et programmer des objets connectés (60%)

| Savoirs | Savoir-faire | Savoir-être |
|---------|--------------|-------------|
| • Concepts fondamentaux de l'IdO et architectures des systèmes | • Concevoir le schéma fonctionnel d'un objet connecté | • Agir de manière responsable dans la sphère numérique |
| • Composants matériels des objets connectés (capteurs, actionneurs, GPIO) | • Assembler les composants matériels | • Développer sa curiosité intellectuelle et son sens de l'organisation |
| • Programmation Python et bonnes pratiques | • Programmer en Python pour interagir avec des capteurs | • S'investir dans son apprentissage |
| • Formats de données (JSON, CSV) | • Lire, interpréter, traiter et filtrer les données | |
| • Principes de filtration et traitement des données | • Enregistrer les données dans des formats appropriés | |
| • Création d'interfaces utilisateur pour la visualisation | • Créer une interface utilisateur en temps réel | |
| | • Dépanner les problèmes matériels et logiciels | |
| | • Documenter le processus de conception | |
| | • Concevoir un PCB pour l'interfaçage capteurs/actionneurs | |

#### Capacité 2 : Maîtriser les protocoles de communication IdO (40%)

| Savoirs | Savoir-faire | Savoir-être |
|---------|--------------|-------------|
| • Principes des protocoles HTTP, MQTT et CoAP (avantages/inconvénients) | • Implémenter MQTT pour la communication entre appareils | • Agir de manière responsable dans la sphère numérique |
| • Fonctionnement d'un courtier MQTT et niveaux de QoS | • Configurer un courtier MQTT (Mosquitto) | • Développer sa curiosité intellectuelle et son sens de l'organisation |
| • Méthodes de sécurisation et d'authentification réseau | • Programmer des scripts Python pour publier/souscrire via MQTT | • S'investir dans son apprentissage |
| • API REST et leur rôle dans l'IdO | • Implémenter une communication sécurisée (TLS/SSL) | |
| • Bibliothèques Python pour les communications réseau | • Utiliser les API REST pour interagir avec des services web | |
| | • Surveiller et optimiser les performances réseau | |
| | • Configurer les paramètres de QoS selon les besoins | |
| | • Utiliser des LLM pour automatiser le traitement de données | |

### 2.2 Organisation du cours et méthodes pédagogiques

Le cours "Objets connectés" (243-4J5-LI) inclut chaque semaine:
- 2 heures de théorie
- 3 heures de travaux pratiques ou de laboratoire
- 2 heures de travail personnel

Les séances théoriques visent à préparer la mise en pratique au laboratoire et porteront sur les fondements de l'IdO, les architectures des systèmes connectés et les protocoles de communication (MQTT, HTTP, API REST), incluant des aspects de sécurisation des échanges.

Les activités pratiques progressent en cinq phases sur 15 semaines:

1. **Phase 1 (Semaines 1-3):** Mise en place du Raspberry Pi 5 comme serveur (exposition sécurisée via Cloudflare Tunnel), configuration des services (courtier MQTT Mosquitto avec WSS/TLS) et prise en main de la carte LilyGO A7670G avec module cellulaire LTE et GPS; réalisation de communications MQTT sans fil (WiFi/LTE), interface tactile Python et bases de programmation IoT

2. **Phase 2 (Semaines 4-7):** Apprentissage du workflow KiCad (schéma → PCB → Gerbers); réalisation du projet de mi-session: conception d'un shield PCB pour le LilyGO A7670G (2 DELs, 2 boutons, 2 potentiomètres, accéléromètre) avec prototype breadboard, schéma, routage et documentation

3. **Phase 3 (Semaines 7-9):** Introduction au réseau mesh LoRa avec Meshtastic (LilyGO T-Beam SUPREME); configuration réseau mesh décentralisé; paramètres radio (SF/BW/CR); gateway WiFi autonome; tests terrain et cartographie de couverture; intégration LoRa + LTE + MQTT dans une architecture unifiée

4. **Phase 4 (Semaines 10-12):** Réception et assemblage du PCB (soudure, tests électriques); automatisation des flux de données avec LLM; infrastructure (API, brokers, monitoring); exploration de l'apport des modèles de langage à l'automatisation et au traitement de données

5. **Phase 5 (Semaines 13-15):** Réalisation d'un projet IdO complet avec PCB assemblé, intégration Meshtastic, tests de performance (QoS, autonomie énergétique), documentation technique et présentation finale

Au fil des semaines, vous travaillerez en laboratoire sur la conception, l'assemblage, la programmation, les essais et la documentation technique, avec des évaluations formatives régulières pour soutenir la progression avant les remises sommatives.

### Pratiques inclusives

Il arrive que le temps supplémentaire (généralement 33%) relatif à la durée prescrite pour une évaluation de type théorique soit offert, pourvu que cela n'interfère pas avec ce qui est visé par l'évaluation. Pour offrir des conditions favorables à l'ensemble du groupe, il est possible que j'offre des mesures inclusives pour tous lors d'une évaluation comme la disponibilité de bouchons, l'utilisation de votre portable ou du temps supplémentaire pour tous.

Il est possible alors que la mesure inclusive accordée à l'ensemble du groupe permette le respect de vos mesures d'accommodement. Cette pratique est en cohérence avec l'approche inclusive et l'accès au temps supplémentaire.

**Définitions:**
- **Durée prescrite:** temps que je juge nécessaire pour compléter l'évaluation
- **Durée permise:** temps que je laisse à l'ensemble du groupe pour compléter l'évaluation et qui pourrait surpasser la durée prescrite
- **Accommodements (mesures des Services adaptés):** temps supplémentaire permis à la durée prescrite d'une évaluation de type « théorique »

Les accommodements ne s'appliquent pas à une démonstration pratique des apprentissages.

### Calendrier des activités

**À noter que le calendrier est à titre indicatif**

| Sem. | Sujets | Activités | Travaux hors classe | Évaluations |
|------|--------|-----------|---------------------|-------------|
| 1 | Labo 1 – Introduction à l'IdO et architecture: Raspberry Pi 5 serveur (Cloudflare Tunnel) | Rappels des acquis; configuration du Raspberry Pi 5 comme serveur; installation du courtier MQTT Mosquitto et exposition via Cloudflare Tunnel; prise en main de la carte LilyGO A7670G (ESP32 + LTE + GPS); configuration Arduino CLI; bases de Python et interface tactile. | Installation des outils, création des comptes nécessaires, lecture sur les architectures IdO et la sécurité d'exposition, exercices Python de base. | Diagnostic initial (formatif) |
| 2 | Labo 2 – Communication MQTT sans fil (WiFi et LTE) | Configuration MQTT avec WSS/TLS; communication MQTT via WiFi et LTE avec le LilyGO A7670G; interface tactile Python pour contrôle de LEDs; tests d'envoi/réception de messages; bonnes pratiques de validation des données. | Finaliser la communication MQTT bidirectionnelle; mise à jour du cahier de laboratoire et de la documentation technique initiale. | Mini-vérifications en laboratoire (formatif) |
| 3 | Labo 2 – Intégration complète et montage breadboard | Chaîne acquisition→serveur (Pi 5 ↔ LilyGO A7670G) via MQTT; intégration boutons/LEDs; finalisation du montage breadboard pour l'interface capteurs/actionneurs; tests de robustesse. | Finaliser le montage breadboard et la documentation technique de base. | **Évaluation sommative:** Laboratoire capteurs et Python — Mise en œuvre d'une chaîne d'acquisition sur Raspberry Pi 5/LilyGO (15%) |
| 4 | Labo 3 – Workflow complet KiCad (pratique uniquement) | Workflow complet de conception PCB en laboratoire : saisie de schéma dans KiCad, bibliothèques, ERC; placement/routage 2 couches, plan de masse, DRC; génération des Gerbers/BOM. Aucune présentation théorique cette semaine. | Revoir le workflow KiCad; identifier les composants du projet; créer le dépôt GitHub du projet. | Vérification ciblée des notions (formatif) |
| 5 | Introduction théorique KiCad + Début dessin PCB | Présentation théorique : concepts PCB (schéma, empreintes, ERC/DRC, THT vs SMD); modules KiCad; début de la capture schématique du shield LilyGO A7670G selon les assignations individuelles. | Compléter le schéma KiCad (ERC sans erreurs); monter le prototype breadboard. | Suivi de progression (formatif) |
| 6 | Projet de mi-session – Prototype breadboard + Routage PCB | Validation du prototype breadboard (I2C accéléromètre MPU6050, ADC potentiomètres); finalisation du schéma KiCad; routage PCB 2 couches; génération des Gerbers/BOM; documentation technique. | Finaliser tous les livrables du projet de mi-session. | Suivi de progression (formatif) |
| 7 | Remise projet de mi-session + Introduction LoRa/Meshtastic | Remise du projet de mi-session; introduction à Meshtastic et au réseau mesh LoRa; flash du firmware sur T-Beam SUPREME; configuration de base (région, canaux). | Lecture sur LoRa et Meshtastic; préparation tests de portée. | **Évaluation sommative:** Projet de mi-session — Shield PCB pour LilyGO A7670G (20%: 15% Capacité 1 + 5% Capacité 2) |
| 8 | LilyGO T-Beam SUPREME – Configuration avancée et réseau mesh | Paramètres radio LoRa (SF/BW/CR); configuration rôles mesh (Router, Router-Critical); réseau multi-nœuds (4-6 nœuds); tests comparatifs SF7/SF9/SF12; mise en place d'un relais fixe; optimisation portée/consommation. | Itérations tests SF; documentation comparative; installation relais permanent. | Revue de progression (formatif) |
| 9 | LilyGO T-Beam SUPREME – Gateway WiFi autonome + Tests terrain | Configuration T-Beam SUPREME comme gateway WiFi→MQTT (connexion directe au broker Mosquitto existant); tests bidirectionnels LoRa ↔ MQTT; tests sur le terrain (portée, latence, stabilité); cartographie de couverture avec GPS; dashboard Node-RED (optionnel); intégration architecture complète (LoRa + LTE + MQTT). | Finalisation gateway WiFi; collecte données GPS terrain; cartographie couverture; documentation tests. | **Évaluation sommative:** TP Intégration LLM et automatisation — Flux capteurs→traitement→action (20%: 15% Capacité 1 + 5% Capacité 2) |
| 10 | Réception et soudure PCB; correctifs éventuels | Réception/inspection, revue par les pairs, plan d'assemblage, préparation BOM/stencil; début de la soudure et tests électriques. | Révisions de routage au besoin; préparation de l'atelier de soudure et des procédures de test. | Contrôle des livrables PCB (formatif) |
| 11 | Automatisation LLM et infrastructure – déclencheurs et pipelines | Automatisation des flux de données avec LLM; infrastructure (API, brokers, monitoring), scripts d'intégration. | Plan de tests détaillé et mise à jour de la documentation. | Dépôt formatif: schéma/PCB et architecture du projet final |
| 12 | Automatisation LLM et infrastructure – fiabilité et sécurité | Mise en production des automatisations, gestion des erreurs, observabilité, sécurité des secrets et accès. | Implantation des communications et journal des anomalies. | Point d'étape projet (formatif) |
| 13 | Projet final Meshtastic – intégration matérielle/logicielle | Assemblage complet, intégration Meshtastic, tests de performance, QoS et autonomie énergétique. | Rédaction de la documentation et préparation de la démonstration. | Dépôt formatif: prototype fonctionnel et documentation préliminaire |
| 14 | Projet final Meshtastic – validation et préparation de la présentation | Tests finaux, corrections et répétition de la présentation. | Finition du rapport et des supports de présentation. | Répétition évaluée (formatif) |
| 15 | Projet final Meshtastic – présentation et remise | Démonstration, remise du rapport et rétroaction. | Aucune (fin de session) | **Évaluation sommative:** Projet final IdO avec PCB et déploiement (30%: 10% Capacité 1 + 20% Capacité 2) |

---

## 3. MODALITÉS D'ÉVALUATION DES APPRENTISSAGES

### 3.1 Évaluation formative des apprentissages

Sur une base régulière, il vous sera proposé des exercices formatifs à réaliser en classe, en équipe ou individuellement. L'évaluation formative est continue et intégrée aux activités d'apprentissage et d'enseignement.

L'évaluation formative se fait:
- **Au début du cours ou d'une séquence:** activité diagnostique permettant de situer leurs acquis et les apprentissages à réaliser ou à approfondir
- **De façon immédiate, à tout moment:** pour guider une personne étudiante, une équipe, le groupe dans son apprentissage, à partir d'observations faites pendant les activités d'apprentissage et d'enseignement
- **À des moments clés du cours:** pour analyser les acquis du groupe et de chaque personne et pour communiquer l'information utile à l'orientation de leurs apprentissages et réajuster les stratégies au besoin et les adapter aux besoins du groupe
- **À la fin d'un cours:** pour vérifier l'état du système (sa fonctionnalité) sur lequel l'étudiant a travaillé

### 3.2 Évaluation sommative des apprentissages

#### Paramètres de l'évaluation sommative – Plan général d'évaluation sommative

**Capacité 1 : Concevoir et programmer des objets connectés (60%)**

| Cible (Niveau optimal) | Seuil de réussite (Niveau minimal) | Méthodes d'évaluation |
|------------------------|-----------------------------------|----------------------|
| • Concevoir un schéma fonctionnel complet d'un objet connecté intégrant plusieurs capteurs | • Concevoir un schéma fonctionnel élémentaire d'un objet connecté avec un capteur | • Projet pratique de conception et programmation d'un objet connecté |
| • Assembler correctement tous les composants matériels nécessaires à l'objet connecté | • Assembler les composants matériels de base de l'objet connecté | • Évaluation en laboratoire sur l'interaction avec les capteurs via Python |
| • Programmer des scripts Python avancés pour la gestion de multiples capteurs | • Programmer des scripts Python simples pour lire les données d'un capteur | • Présentation orale du projet réalisé |
| • Lire et interpréter avec précision les données de différents capteurs | • Lire les données de base d'un capteur | • Rapport de documentation technique du projet |
| • Mettre en œuvre des algorithmes de traitement et de filtrage avancés | • Appliquer des techniques de filtrage simples aux données | |
| • Enregistrer les données dans des formats adaptés pour différentes applications | • Enregistrer les données dans un format standard tel que CSV | |
| • Développer une interface utilisateur interactive pour la visualisation des données | • Créer une interface de base pour afficher les données collectées | |
| • Identifier et résoudre efficacement les problèmes complexes | • Identifier et résoudre les problèmes simples courants | |
| • Rédiger une documentation complète et détaillée du projet | • Fournir une documentation de base couvrant les aspects essentiels | |
| • Travailler de manière efficace et proactive au sein de l'équipe | • Participer aux tâches en équipe de manière acceptable | |
| • PCB fonctionnel avec un routage optimisé, connecteurs adaptés aux capteurs/actionneurs, bonne disposition des composants | • Concevoir un PCB presque fonctionnel avec un schéma correct et un routage partiellement opérationnel | |

**Capacité 2 : Maîtriser les protocoles de communication IdO (40%)**

| Cible (Niveau optimal) | Seuil de réussite (Niveau minimal) | Méthodes d'évaluation |
|------------------------|-----------------------------------|----------------------|
| • Implémenter efficacement MQTT pour des communications fiables entre plusieurs appareils | • Mettre en place une communication de base en MQTT entre deux appareils | • Travaux pratiques sur l'implémentation des protocoles de communication |
| • Configurer un courtier MQTT sécurisé et optimisé pour les besoins du réseau | • Installer et configurer un courtier MQTT fonctionnel | • Examen en laboratoire sur la configuration d'un courtier MQTT sécurisé |
| • Programmer des scripts avancés gérant les publications et les souscriptions avec différents niveaux de QoS | • Programmer des scripts basiques permettant de publier et recevoir des messages via MQTT | • Projet de communication entre objets connectés utilisant différents protocoles |
| • Configurer une communication entièrement sécurisée avec authentification et chiffrement | • Mettre en place un chiffrement basique pour sécuriser les communications | • Rapport de configuration et optimisation des communications réseau |
| • Intégrer des API REST complexes pour enrichir les fonctionnalités de l'objet connecté | • Effectuer des appels API simples pour récupérer des données externes | |
| • Analyser et améliorer les performances en ajustant les paramètres réseau | • Surveiller les performances de base des communications | |
| • Diagnostiquer et résoudre des problèmes complexes de communication | • Identifier et résoudre des problèmes de communication courants | |
| • Fournir une documentation détaillée des configurations utilisées | • Documenter les configurations principales des protocoles | |
| • Optimiser les paramètres de QoS pour un équilibre entre performance et fiabilité | • Configurer les paramètres de QoS par défaut appropriés | |
| • Mettre en place une authentification robuste pour assurer la sécurité des données | • Implémenter une méthode d'authentification basique | |
| • Automatisation partielle de tâches de traitement de données avec des résultats fonctionnels mais perfectibles | • Automatisation de tâches de traitement de données, avec des résultats cohérents et adaptés aux besoins spécifiques | |

### 3.3 Évaluation de l'expression et de la communication en français

Dans un souci de valorisation de la langue, l'évaluation de l'expression et de la communication en français se fera de manière constante, que ce soit à l'oral ou à l'écrit. Cette évaluation se fera de façon formative tout au long du cours. Cependant, pour la documentation du processus de conception et de programmation, l'évaluation sera sommative.

Elle sera évaluée dans le rapport de documentation technique du projet. Les critères d'évaluation pour cette capacité se trouvent dans le plan général d'évaluation sommative présenté à la section précédente.

Les modalités spécifiques pour la valorisation de l'expression et de la communication en français sont encadrées par les dispositions particulières de l'article 6.6 de la PIEA (Politique institutionnelle d'évaluation des apprentissages).

### 3.4 Seuil de réussite du cours

La réussite du cours (243-4J5-LI – Objets connectés) est atteinte à partir de **60%** sur l'ensemble du cours.

La pondération par capacités est la suivante:
- **Concevoir et programmer des objets connectés:** 60%
- **Maîtriser les protocoles de communication IdO:** 40%

La note finale par capacité ne correspond pas nécessairement à la moyenne arithmétique des résultats des différentes évaluations : elle reflète un jugement global fondé sur des observations continues en cours de session et sur l'atteinte des capacités visées.

#### Répartition des évaluations sommatives

| Évaluations sommatives | Capacité 1 (60%) | Capacité 2 (40%) |
|------------------------|--------------------|--------------------|
| Laboratoire capteurs et Python | 15% | - |
| Projet mi-session | 20% | 10% |
| Laboratoire intégration LLM | 15% | 5% |
| Projet final | 10% | 25% |

---

## 4. MATÉRIEL OBLIGATOIRE

1. Un compte payant de premier niveau Claude, Gemini ou ChatGPT (environ 30$/mois ou gratuit pour étudiant Gemini pendant 1 an)
2. Un compte Cloudflare (gratuit)
3. Un nom de domaine public enregistré chez Cloudflare (environ 15$ pour un an) – on va faire ça en classe
4. Le kit de pièce X (Y$)

---

## 5. RÈGLES DÉPARTEMENTALES

### Règles d'éthique et de comportement à respecter durant les cours théoriques et au laboratoire

- Durant les cours théoriques, soyez concentrés et évitez de discuter avec vos voisins. Une bonne pratique pour garder l'attention est de prendre des notes (même si elles sont incomplètes et que vous ne les relirez plus jamais, le fait de prendre des notes garde votre attention sur le cours)

- Demandez la parole si vous avez une question ou quelque chose à dire

- Il est interdit de manger dans les laboratoires près des ordinateurs du cégep

- Soyez respectueux envers les gens et le matériel

- L'usage de l'ordinateur durant les laboratoires est essentiel, mais uniquement pour compléter vos activités (pas de Facebook, YouTube, jeux ou autres distractions inutiles durant le laboratoire) et ce, tant que le cours n'est pas terminé

- L'utilisation du cellulaire et l'envoi de textos sont interdits durant les cours, à moins que cela ne soit expressément demandé par le professeur pour une activité pédagogique. Pour toute autre urgence, vous devez vous éloigner de la salle de classe ou de la zone de laboratoire afin de ne pas perturber vos collègues

- Assistez à tous les cours, cela favorise l'accès à la disponibilité de votre professeur

- À la fin d'une activité, les équipements doivent être réinitialisés, ne laissez pas de solutions dans les équipements utilisés

- À la fin d'une activité gardez l'espace de travail rangé et propre

- Advenant des séances à distance (avec TEAMS ou Zoom) vous devrez avoir une caméra que vous allumerez, pour refléter le plus possible une salle de classe avec des interactions entre tous. Vous devrez avoir accès à un micro, des écouteurs ou haut-parleur

- Avec TEAMS votre micro devra être fermé à moins que vous ne posiez une question

---

## 6. MODALITÉS D'APPLICATION PARTICULIÈRES DE LA PIEA

### Article 6.6 : L'évaluation de l'expression et de la communication en français

Considérant qu'il est de la responsabilité des personnes étudiantes d'utiliser un français de qualité lorsqu'il leur faut démontrer leurs compétences afin que celles-ci puissent être évaluées avec justesse. Le département de génie électrique précise que:

- L'évaluation de la qualité du français fait partie intégrante de toutes les évaluations réalisées

- Le poids accordé à l'évaluation de la qualité du français lors des évaluations dépend du contexte dans lequel se font ces évaluations

- Les poids accordés à l'évaluation de la qualité du français pour les différentes évaluations d'un cours sont précisés dans le plan du cours ou dans la description même des travaux qui sont évalués

- Un travail qui ne respecte pas les exigences minimales est refusé dans un premier temps. La personne étudiante doit y apporter des correctifs significatifs dans un délai de 48 heures pour que le travail soit corrigé. À la deuxième remise, le travail doit répondre aux exigences minimales. Dans la situation contraire, le travail n'est pas retenu et il y a absence de résultat pour cet élément

- Les exigences minimales relatives à la qualité des textes pour la remise d'un travail sont les suivantes:
  - **L'orthographe, la syntaxe et la justesse des mots utilisés:** des faiblesses sont évidentes, mais ne nuisent pas à l'intelligibilité du texte (ou à la compréhension du texte)
  - **La clarté, la cohérence et la structure:** malgré la présence de plusieurs lacunes, il est possible de se représenter ce dont il est question sans devoir pallier l'absence d'une information essentielle à la compréhension de ce qui est exposé

### Article 12.3 : La remise en retard de réalisations servant à l'évaluation sommative des apprentissages

Considérant qu'il est de la responsabilité de la personne étudiante de compléter les travaux sommatifs dans le temps alloué afin de démontrer ses compétences de manière juste, le département de génie électrique précise que:

- Tout travail remis en retard est pris en considération dans l'évaluation, mais une pénalité est appliquée. Celle-ci est de **10% par jour de retard** (incluant les fins de semaine), à moins d'une entente préalable avec la personne enseignante

- La remise d'une évaluation servant à l'évaluation sommative est refusée si les copies corrigées ont été transmises aux autres personnes étudiantes ou pour tout retard excédant 5 jours. Cela entraine automatiquement une absence de résultat ou la note zéro. Une rétroaction formative est toutefois formulée. À moins d'une situation particulière et communiquée aux personnes étudiantes, un délai de 5 jours devra être respecté avant la remise des copies corrigées par la personne enseignante

### Article 13.1 : Le réexamen d'un résultat attribué pour une tâche

Le réexamen d'un résultat attribué pour une tâche comprend les étapes suivantes:

1. L'étudiant qui reçoit un résultat qu'il juge inadéquat demande à l'enseignant concerné de procéder à la révision de ce résultat dans les **5 jours ouvrables** qui suivent

2. L'enseignant répond à la demande de l'étudiant dans les **5 jours ouvrables** qui suivent

3. L'étudiant qui juge que le résultat révisé est inadéquat en informe la coordination départementale par courriel dans les **2 jours ouvrables** qui suivent

4. Le coordonnateur qui reçoit un courriel de contestation dirige dans les **5 jours ouvrables** qui suivent une rencontre de réexamen du résultat révisé à laquelle participe:
   - L'étudiant
   - L'enseignant qui a attribué le résultat contesté
   - Un autre enseignant du département
   - Le coordonnateur du département

5. Le comité de révision fait part de son verdict à l'étudiant dans les **2 jours ouvrables** qui suivent

**Note importante:** Bien que la présence et la participation aux cours ne puissent être des objets d'évaluation sommative, il se peut que des absences répétées ou une participation insuffisante à un cours empêchent l'enseignant de collecter suffisamment de données en contexte contrôlé pour qu'il puisse établir avec justesse un résultat global pour chaque objet essentiel et sa note finale pour le cours. Ce facteur sera pris en considération par le comité de révision le cas échéant.

---

## 7. MÉDIAGRAPHIE

Cloudflare. (s.d.). *Cloudflare Tunnel documentation*. Cloudflare Developers. https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

Eclipse Foundation. (s.d.). *Eclipse Paho MQTT Python client library*. https://eclipse.dev/paho/files/paho.mqtt.python/html/

Eclipse Foundation. (s.d.). *Eclipse Mosquitto: An open source MQTT broker*. https://mosquitto.org/documentation/

Espressif Systems. (s.d.). *ESP-IDF programming guide*. https://docs.espressif.com/projects/esp-idf/en/latest/esp32/

HiveMQ. (s.d.). *MQTT essentials*. https://www.hivemq.com/mqtt-essentials/

KiCad. (s.d.). *KiCad documentation*. https://docs.kicad.org/

LilyGO. (s.d.). *T-A7670X [Dépôt GitHub]*. https://github.com/Xinyuan-LilyGO/T-A7670X

LilyGO. (s.d.). *LilyGo-LoRa-Series [Dépôt GitHub]*. https://github.com/Xinyuan-LilyGO/LilyGo-LoRa-Series

LoRa Alliance. (s.d.). *About LoRaWAN*. https://lora-alliance.org/about-lorawan/

Meshtastic. (s.d.). *Meshtastic documentation*. https://meshtastic.org/docs/

OASIS Open. (s.d.). *MQTT specification*. https://mqtt.org/mqtt-specification/

Python Software Foundation. (s.d.). *Python 3 documentation*. https://docs.python.org/3/

Raspberry Pi Foundation. (s.d.). *Raspberry Pi documentation*. https://www.raspberrypi.com/documentation/

---

## 8. DISPONIBILITÉS

Pour des rencontres, du dépannage ou toute question pouvant survenir pendant la session, vous pouvez prendre rendez-vous, en personne, par OMNIVOX ou par TEAMS. Vous trouverez mon horaire sur la porte de mon bureau.

Les rencontres peuvent se faire en personne ou par TEAMS.
