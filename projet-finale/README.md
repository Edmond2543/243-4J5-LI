# Projet Final - Surveillance d'Abris Télécom (Hydro-Limoilou)

## 📍 Description du site et Mise en situation
Ce projet s'inscrit dans le cadre du déploiement IoT d'**Hydro-Limoilou**, spécifiquement pour le **Poste 06**. Le système est conçu pour surveiller l'état et l'intégrité structurelle d'un abri de télécommunication isolé.

L'objectif est d'assurer une télémétrie en temps réel via une connexion hybride (WiFi WPA2 Enterprise par défaut, avec redondance cellulaire LTE) pour détecter des événements critiques :
- **Intégrité du bâti (Abri)** : Le capteur de luminosité (BH1750) permet de détecter si l'abri s'est effondré (lumière inexistante < 1 lux) ou si le toit a été arraché/exposé au soleil (lumière très forte > 2000 lux).
- **Intégrité de l'équipement (Rack)** : L'accéléromètre (MPU6050) surveille les vibrations violentes, les séismes ou la chute du rack d'équipement.
- **Contrôle et LLM** : Un Raspberry Pi doté d'un écran tactile permet aux techniciens sur place ou à distance de surveiller l'état, de contrôler les actionneurs (LEDs), de visualiser les alarmes et de recevoir des diagnostics rédigés par une intelligence artificielle (Groq LLM).

---

## 🔌 Schéma de câblage breadboard

Le microcontrôleur central est un **LilyGo T-SIM A7670G (ESP32)**.

| Composant | Broche ESP32 / LilyGo | Note |
| :--- | :--- | :--- |
| **MPU6050 (Vibrations)** | `SDA: 21` / `SCL: 22` | Bus I2C partagé. Alimentation en **3.3V**. |
| **BH1750 (Lumière)** | `SDA: 21` / `SCL: 22` | Bus I2C partagé. Alimentation en **3.3V**. |
| **LED Rouge (Actuator 1)** | `Pin 32` | Via résistance 220Ω vers GND. |
| **LED Verte (Actuator 2)** | `Pin 33` | Via résistance 220Ω vers GND. |
| **Bouton 1 (Vert)** | `Pin 25` | Connecté au GND (Mode `INPUT_PULLUP`). |
| **Bouton 2 (Rouge)** | `Pin 35` | Connecté au GND (Mode `INPUT_PULLUP`). |

---

## 📡 Liste des topics MQTT (Conformité contrat VM)

L'arborescence respecte la norme `hydro-limoilou/poste-06/`. Les payloads utilisent le format **JSON** strict de bout-en-bout.

| Topic | Sens (ESP32) | Payload JSON (Exemple) | Description |
| :--- | :--- | :--- | :--- |
| `.../status` | Pub | `{"uptime": 120, "rssi": -65, "link": "WIFI"}` | Statut de connexion et santé de la puce (aux 10s) |
| `.../status/llm` | RPi Pub | `Texte brut` | Analyse IA des capteurs générée par l'Agent RPi |
| `.../config/mode/set` | Sub | `WIFI` ou `LTE` (Texte) | Commande pour forcer le mode réseau |
| `.../telemetry/vibration` | Pub | `{"x": 0.05, "y": 0.02, "z": 9.81, "ts": 120}` | Données de l'accéléromètre MPU6050 (aux 10s) |
| `.../telemetry/light`| Pub | `{"value": 450.2, "unit": "lux", "ts": 120}` | Données d'ensoleillement BH1750 (aux 10s) |
| `.../telemetry/btn_1` | Pub | `{"state": "pressed", "ts": 120}` | État instantané du bouton 1 (anti-rebond 250ms) |
| `.../telemetry/btn_2` | Pub | `{"state": "released", "ts": 125}` | État instantané du bouton 2 (anti-rebond 250ms) |
| `.../actuators/led_1` | Pub/Sub | `{"state": "on", "ts": 120}` | Commande et confirmation d'état de la LED Rouge |
| `.../actuators/led_2` | Pub/Sub | `{"state": "off", "ts": 120}` | Commande et confirmation d'état de la LED Verte |
| `.../alarms/motion` | Pub | `{"status":"CRITICAL", "message":"..."}` | Alerte envoyée si vibration anormale détectée |
| `.../alarms/light` | Pub | `{"status":"WARNING", "message":"..."}` | Alerte envoyée si lumière critique détectée |

---

## 🚀 Procédure de démo et Résultats des 3 scénarios de test

### Scénario 1 : Télémétrie et Contrôle Bidirectionnel Unifié (JSON)
- **Procédure** : 
  1. Appuyer sur le Bouton 1 (Vert) physiquement.
  2. Sur l'interface tactile du Raspberry Pi (Onglet "1. CONTRÔLE"), cliquer sur le bouton de la "LED ROUGE".
- **Résultat attendu** : 
  - L'appui physique allume/éteint la LED correspondante. L'ESP32 publie un JSON standardisé avec un timestamp (`ts`). L'interface tactile se met à jour instantanément pour refléter le bon état des boutons et des LEDs.
  - Le clic sur l'écran tactile envoie le même format JSON (`{"state": "on"}`). L'ESP32 l'interprète et allume la LED physique. Le système est 100% synchronisé et respecte le contrat de payload imposé.

### Scénario 2 : Test des Alarmes Structurelles (Lumière & Mouvement)
- **Procédure** : 
  1. Cacher le capteur BH1750 avec la main pour simuler un effondrement (< 1 lux), puis l'éclairer avec une lumière forte (> 2000 lux).
  2. Secouer physiquement la breadboard pour simuler une chute du rack.
  3. Aller dans l'onglet "3. ALARMES" de l'écran tactile.
- **Résultat attendu** : 
  - L'interface tactile affiche des événements en rouge (CRITIQUE) signalant l'effondrement potentiel ou le mouvement violent, et en rouge/orange pour l'exposition lumineuse excessive. 
  - Un appui sur le bouton tactile `[ ACQUITTEMENT ]` valide l'alarme et la passe en vert pour nettoyer le panneau d'opérations.

### Scénario 3 : Agent Intelligence Artificielle (Groq LLM)
- **Procédure** : 
  1. Lancer l'agent IA (`llm_agent.py`) en tâche de fond sur le RPi.
  2. Laisser tourner le système pendant au moins 30 secondes.
  3. Vérifier les logs du serveur IA ou écouter le topic `hydro-limoilou/poste-06/status/llm`.
- **Résultat attendu** : 
  - Le script Python sur le Raspberry Pi lit les valeurs MQTT en temps réel.
  - Toutes les 30 secondes, il envoie les données environnementales brutes à l'API de Groq (Llama-3).
  - L'IA rédige un court diagnostic humain de la situation (ex: *"Les niveaux de luminosité et de vibration sont normaux, l'intégrité de l'abri est stable."*), publié en direct sur le réseau MQTT pour les opérateurs.