---
theme: seriph
background: https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1920
title: 243-4J5-LI - Objets connectés - Semaine 2
info: |
  ## Objets connectés
  Semaine 2 - Protocole MQTT et communication sans fil

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

Semaine 2 - Protocole MQTT et communication sans fil

<div class="pt-12">
  <span class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Francis Poisson - Cégep Limoilou - H26
  </span>
</div>

---
layout: section
---

# Récapitulatif
## Où en sommes-nous?

---

# La semaine dernière...

<div class="grid grid-cols-2 gap-6">

<div>

### Problèmes résolus

<v-clicks>

- **Programmer à distance** → RPi comme relais
- **Se connecter au RPi** → SSH
- **Pas d'IP publique** → Cloudflare Tunnel
- **Synchroniser le code** → Git
- **Coder efficacement** → Claude Code
- **Compiler sans GUI** → Arduino CLI

</v-clicks>

</div>

<div>

<v-click>

```mermaid {scale: 0.8}
graph TB
    YOU[Vous] -->|SSH via Cloudflare| RPI[RPi]
    RPI -->|Arduino CLI| LILY[LilyGO]

    style YOU fill:#6f6
    style RPI fill:#69f
    style LILY fill:#f96
```

</v-click>

<v-click>

<div class="mt-4 p-2 bg-green-500 bg-opacity-20 rounded-lg text-sm">

On peut maintenant **programmer** le LilyGO à distance!

</div>

</v-click>

</div>

</div>

---

# Mais il manque quelque chose...

<div class="grid grid-cols-2 gap-6">

<div>

### On sait programmer, mais...

<v-clicks>

- Comment le LilyGO **envoie** ses données?
- Comment le RPi **reçoit** les mesures?
- Comment **commander** le LilyGO depuis le RPi?
- Comment faire communiquer **plusieurs appareils**?

</v-clicks>

</div>

<div>

<v-click>

```mermaid {scale: 1.4}
graph LR
    LILY[LilyGO] -.->|"???"| RPI[RPi]
    RPI -.->|"???"| LILY

    style LILY fill:#f96
    style RPI fill:#69f
```

</v-click>

<v-click>

<div class="mt-4 p-2 bg-yellow-500 bg-opacity-20 rounded-lg text-sm">

**Nouveau problème** : Les appareils doivent pouvoir **communiquer** entre eux!

</div>

</v-click>

</div>

</div>

---

# Options de communication

<div class="grid grid-cols-2 gap-4">

<div>

### Ce qu'on pourrait utiliser

| Protocole | Problème |
|-----------|----------|
| HTTP REST | Lourd, polling constant |
| Raw TCP | Complexe à gérer |
| Serial USB | Pas sans fil! |
| Email | Sérieusement? |

</div>

<div>

<v-click>

### Ce qu'il nous faut

- **Léger** (batterie limitée)
- **Bidirectionnel** (envoyer ET recevoir)
- **Sans fil** (WiFi/LTE)
- **Fiable** (messages importants)
- **Sécurisé** (données sensibles)

</v-click>

<v-click>

<div class="mt-2 p-2 bg-green-500 bg-opacity-20 rounded-lg text-center">

**Solution** : MQTT

Le protocole conçu pour l'IoT!

</div>

</v-click>

</div>

</div>

---

# Notre chaîne s'agrandit

```mermaid {scale: 0.6}
graph LR
    subgraph "Semaine 1"
        YOU[Vous] -->|SSH| CF[Cloudflare]
        CF --> RPI[RPi]
        RPI -->|Arduino CLI| LILY[LilyGO]
    end

    subgraph "Semaine 2"
        LILY2[LilyGO] <-->|MQTT| MOSQ[Mosquitto]
        MOSQ <--> UI[Interface]
    end

    RPI -.-> MOSQ

    style YOU fill:#6f6
    style RPI fill:#69f
    style LILY fill:#f96
    style MOSQ fill:#f9f
```

<v-click>

<div class="mt-4 p-3 bg-blue-500 bg-opacity-20 rounded-lg text-center">

**Cette semaine** : On ajoute la **communication** entre le LilyGO et le RPi avec MQTT

</div>

</v-click>

---
layout: section
---

# Partie 1
## Introduction à MQTT

---

# MQTT - Message Queuing Telemetry Transport

<div class="grid grid-cols-2 gap-6">

<div>

### Historique

- Créé en **1999** par IBM et Arcom
- Conçu pour la **télémétrie** (pipelines pétroliers)
- Standard **OASIS** depuis 2014
- Version actuelle: **MQTT 5.0**

### Caractéristiques clés

- **Léger** - En-tête minimal (2 octets)
- **Bidirectionnel** - Pub/Sub
- **Fiable** - QoS configurable
- **Sécurisé** - TLS/SSL support

</div>

<div>

### Pourquoi MQTT pour l'IoT?

| Critère | HTTP | MQTT |
|---------|:----:|:----:|
| Overhead | ~700B | ~2B |
| Pattern | Req/Res | Pub/Sub |
| Connexion | Courte | Persistante |
| Push | Polling | Natif |
| Batterie | Élevée | Faible |

</div>

</div>

---

# Avantages du Publish/Subscribe

<div class="grid grid-cols-3 gap-4 mt-4">

<div class="p-4 bg-blue-500 bg-opacity-20 rounded-lg text-center">

### Découplage spatial

Les clients n'ont pas besoin de connaître l'adresse IP des autres

```
Publisher ─► Broker ◄─ Subscriber
```

</div>

<div class="p-4 bg-green-500 bg-opacity-20 rounded-lg text-center">

### Découplage temporel

Les messages sont livrés même si le destinataire est hors ligne

```
📤 → 💾 → 📥
     (stocké)
```

</div>

<div class="p-4 bg-purple-500 bg-opacity-20 rounded-lg text-center">

### Découplage de synchronisation

Pas de blocage pendant les opérations

```
async publish()
async subscribe()
```

</div>

</div>

---

# Topics MQTT

<div class="grid grid-cols-2 gap-6">

<div>

### Structure hiérarchique

Les topics utilisent `/` comme séparateur de niveaux.

```
maison/salon/temperature
maison/cuisine/temperature
garage/porte/etat
```

</div>

<div>

### Conventions de nommage

| ✅ Bonnes pratiques | ❌ À éviter |
|-------------------|-----------|
| `etudiant/id/sensors/temp` | `CAPTEUR_123` |
| Minuscules, tirets | Espaces, accents |
| Hiérarchie logique | Structure plate |

</div>

</div>

---

# Wildcards - Caractères joker

<div class="grid grid-cols-2 gap-6">

<div>

### `+` - Single Level Wildcard

Remplace **un seul niveau**.

```
maison/+/temperature
```

Correspond à:
- ✅ `maison/salon/temperature`
- ✅ `maison/cuisine/temperature`
- ❌ `maison/etage1/salon/temperature`

</div>

<div>

### `#` - Multi Level Wildcard

Remplace **tous les niveaux** restants.

```
maison/#
```

Correspond à:
- ✅ `maison/salon`
- ✅ `maison/salon/temperature`
- ✅ `maison/etage1/salon/lumiere`

⚠️ Doit être en fin de topic

</div>

</div>

---

# QoS - Quality of Service

<div class="grid grid-cols-3 gap-2">

<div class="text-center">

**QoS 0** - At Most Once

```mermaid {scale: 1}
graph TB
    P[Publisher] -->|Message| B[Broker]
    B -->|Message| S[Subscriber]
```

</div>

<v-click>

<div class="text-center">

**QoS 1** - At Least Once

```mermaid {scale: 1}
graph TB
    P[Publisher] -->|Message| B[Broker]
    B -->|PUBACK| P
    B -->|Message| S[Subscriber]
    S -->|PUBACK| B
```

</div>

</v-click>

<v-click>

<div class="text-center">

**QoS 2** - Exactly Once

```mermaid {scale: 0.9}
graph TB
    P[Publisher] -->|PUBLISH| B[Broker]
    B -->|PUBREC| P
    P -->|PUBREL| B
    B -->|PUBCOMP| P
```

</div>

</v-click>

</div>

---

# Comparaison des niveaux QoS

| QoS | Garantie | Messages | Latence | Usage |
|:---:|----------|:--------:|:-------:|-------|
| **0** | Au plus une fois | 1 | ⚡ Faible | Données fréquentes (capteurs) |
| **1** | Au moins une fois | ≥1 | Moyenne | Commandes importantes |
| **2** | Exactement une fois | 1 | 🐢 Élevée | Transactions critiques |

<v-click>

### Quand utiliser quel QoS?

- **QoS 0**: Température toutes les secondes (si une lecture manque, pas grave)
- **QoS 1**: Commande d'allumer une lumière (duplicata acceptable)
- **QoS 2**: Transaction de paiement, alarme incendie

</v-click>

---

# Messages retenus (Retained)

<div class="grid grid-cols-2 gap-6">

<div>

### Problème

Un nouveau subscriber ne reçoit les messages que **après** son abonnement.

```mermaid {scale: 0.6}
sequenceDiagram
    Publisher->>Broker: temp = 22°C
    Note over Subscriber: Se connecte
    Subscriber->>Broker: subscribe(temp)
    Note over Subscriber: Attend...<br/>Pas de valeur!
```

</div>

<div>

### Solution: Retained Message

```mermaid {scale: 0.6}
sequenceDiagram
    Publisher->>Broker: temp = 22°C [RETAIN]
    Note over Broker: Stocke le message
    Note over Subscriber: Se connecte
    Subscriber->>Broker: subscribe(temp)
    Broker->>Subscriber: temp = 22°C
    Note over Subscriber: Reçoit immédiatement!
```

</div>

</div>

<v-click>

```python
# Publier avec retain
client.publish("maison/salon/temp", "22", retain=True)
```

</v-click>

---

# Last Will and Testament (LWT)

### Testament en cas de déconnexion

<div class="grid grid-cols-2 gap-6">

<div>

**Problème**: Comment savoir si un appareil est hors ligne?

**Solution**: Le client configure un message "testament" à la connexion.

Si le client se déconnecte **anormalement**, le broker publie ce message.

</div>

<div>

```python
# Configuration du LWT à la connexion
client.will_set(
    topic="device/capteur1/status",
    payload="offline",
    qos=1,
    retain=True
)

client.connect(broker)

# Publier le statut online
client.publish(
    "device/capteur1/status",
    "online",
    retain=True
)
```

</div>

</div>

---
layout: section
---

# Partie 2
## Broker Mosquitto

---

# Mosquitto - Broker MQTT Open Source

<div class="grid grid-cols-2 gap-6">

<div>

### Caractéristiques

- **Open source** (Eclipse Foundation)
- **Léger** - Faible empreinte mémoire
- **Complet** - MQTT 3.1, 3.1.1, 5.0
- **Sécurisé** - TLS, authentification
- **Extensible** - Plugins

### Installation

```bash
# Ubuntu/Debian
sudo apt install mosquitto mosquitto-clients

# Vérifier le statut
sudo systemctl status mosquitto
```

</div>

<div>

### Architecture

```mermaid {scale: 0.6}
graph TB
    subgraph "Mosquitto"
        L1[Listener :1883<br/>MQTT]
        L2[Listener :8883<br/>MQTT/TLS]
        L3[Listener :9001<br/>WebSocket]
        AUTH[Auth Plugin]
        STORE[Message Store]
    end

    C1[Client MQTT] --> L1
    C2[Client sécurisé] --> L2
    C3[Browser] --> L3

    L1 --> AUTH
    L2 --> AUTH
    L3 --> AUTH
```

</div>

</div>

---

# Configuration Mosquitto

<div class="grid grid-cols-2 gap-4">

<div>

### `/etc/mosquitto/mosquitto.conf`

```bash
allow_anonymous false
password_file /etc/mosquitto/passwd

# MQTT local seulement
listener 1883 localhost

# WebSocket (tunnel)
listener 9001
protocol websockets
```

</div>

<div>

### Gestion des utilisateurs

```bash
# Créer un utilisateur
sudo mosquitto_passwd -c \
  /etc/mosquitto/passwd mon_user

# Ajouter un utilisateur
sudo mosquitto_passwd \
  /etc/mosquitto/passwd autre_user

# Redémarrer
sudo systemctl restart mosquitto
```

</div>

</div>

---

# Test avec mosquitto_pub et mosquitto_sub

<div class="grid grid-cols-2 gap-4">

<div>

### Terminal 1 - Subscriber

```bash
# S'abonner à un topic
mosquitto_sub -h localhost \
  -t "test/capteur" \
  -u mon_user -P mon_password

# Avec wildcards
mosquitto_sub -h localhost \
  -t "maison/#" \
  -u mon_user -P mon_password
```

</div>

<div>

### Terminal 2 - Publisher

```bash
# Publier un message
mosquitto_pub -h localhost \
  -t "test/capteur" \
  -m "25.5" \
  -u mon_user -P mon_password

# Message JSON
mosquitto_pub -h localhost \
  -t "test/capteur" \
  -m '{"temp": 25.5, "hum": 60}' \
  -u mon_user -P mon_password
```

</div>

</div>

---

# Problème : MQTT à travers Cloudflare?

<div class="grid grid-cols-2 gap-6">

<div>

### MQTT standard

- Port **1883** (TCP brut)
- Ou port **8883** (TLS)
- Protocole **binaire** propriétaire

### Cloudflare Tunnel

- Ne supporte que **HTTP/HTTPS**
- Port **443** uniquement
- Protocole **web** standard

</div>

<div>

<v-click>

```mermaid {scale: 0.55}
graph LR
    LILY[LilyGO] -->|"MQTT :1883"| CF[Cloudflare]
    CF -.->|"❌ Bloqué!"| MOSQ[Mosquitto]

    style CF fill:#f66
```

</v-click>

<v-click>

<div class="mt-4 p-2 bg-yellow-500 bg-opacity-20 rounded-lg text-sm">

**Problème** : Cloudflare ne laisse pas passer le protocole MQTT natif!

</div>

</v-click>

<v-click>

<div class="mt-2 p-2 bg-green-500 bg-opacity-20 rounded-lg text-sm">

**Solution** : Encapsuler MQTT dans WebSocket (protocole web)

</div>

</v-click>

</div>

</div>

---

# WebSocket - Le pont vers MQTT

### Pourquoi WebSocket?

<div class="grid grid-cols-2 gap-6">

<div>

**Le principe**

WebSocket = connexion **bidirectionnelle persistante** qui passe par le port **443** (HTTPS)

```
MQTT  →  WebSocket  →  HTTPS  →  Cloudflare  →  OK!
```

</div>

<div>

### Avantages

- **Port 443** - Passe partout (pare-feux, proxies)
- **Bidirectionnel** - Parfait pour MQTT
- **TLS natif** - Sécurisé (WSS)
- **Compatible Cloudflare** - C'est du web!

### MQTT over WebSocket

Mosquitto écoute sur le port **9001** en WebSocket, Cloudflare le tunnel vers l'extérieur.

</div>

</div>

---

# WSS - WebSocket Secure

### TLS/SSL pour WebSocket

```mermaid {scale: 0.7}
graph LR
    subgraph "Client (Browser)"
        JS[JavaScript]
    end

    subgraph "Internet"
        TLS[🔒 TLS 1.3]
    end

    subgraph "Serveur"
        WS[WebSocket :443]
        MQTT[Mosquitto]
    end

    JS -->|wss://| TLS
    TLS --> WS
    WS --> MQTT
```

<v-click>

### Configuration Mosquitto avec TLS

```bash
listener 9001
protocol websockets
certfile /etc/letsencrypt/live/domain/fullchain.pem
keyfile /etc/letsencrypt/live/domain/privkey.pem
```

</v-click>

---
layout: section
---

# Partie 3
## WiFi Enterprise (WPA-EAP)

---

# Problème : Le WiFi du Cégep

<div class="grid grid-cols-2 gap-6">

<div>

### WiFi à la maison

```cpp
// Simple!
WiFi.begin("MonWiFi", "motdepasse123");
```

<v-click>

### WiFi au Cégep

```cpp
// ???
WiFi.begin("CegepWiFi", ???);
// Un mot de passe ne suffit pas!
```

</v-click>

</div>

<div>

<v-click>

### Le problème

Le réseau du Cégep utilise **WPA-Enterprise** :
- Identifiant **personnel** (DA)
- Mot de passe **individuel**
- Pas un simple mot de passe partagé

</v-click>

<v-click>

<div class="mt-4 p-2 bg-yellow-500 bg-opacity-20 rounded-lg text-sm">

L'ESP32 doit s'authentifier avec **votre compte** du Cégep, pas juste un mot de passe WiFi!

</div>

</v-click>

</div>

</div>

---

# WPA-EAP vs WPA-PSK

<div class="grid grid-cols-2 gap-6">

<div>

### WPA-PSK (Personnel)

- **Un mot de passe** partagé
- Tous les utilisateurs = même clé
- Révocation difficile
- Usage: maison, petit bureau

```
WiFi: MonReseau
Pass: motdepasse123
(tout le monde partage)
```

</div>

<div>

### WPA-EAP (Entreprise)

- **Identifiants individuels**
- Chaque utilisateur = ses credentials
- Révocation facile
- Usage: entreprises, écoles

```
WiFi: CegepSecure
User: jean.dupont
Pass: personnel123
(identifiant unique)
```

</div>

</div>

---

# Architecture WPA-EAP

```mermaid {scale: 0.6}
graph LR
    subgraph "Client"
        DEV[Appareil WiFi]
        SUPP[Supplicant]
    end

    subgraph "Réseau"
        AP[Point d'accès]
        AUTH[Authenticator]
    end

    subgraph "Backend"
        RADIUS[Serveur RADIUS]
        LDAP[Annuaire LDAP/AD]
    end

    DEV --> SUPP
    SUPP -->|EAP| AP
    AP --> AUTH
    AUTH -->|RADIUS| RADIUS
    RADIUS --> LDAP
```

<v-click>

### Méthode utilisée: PEAP-MSCHAPv2

- **PEAP** - Protected EAP (tunnel TLS)
- **MSCHAPv2** - Microsoft Challenge-Handshake (authentification)

</v-click>

---

# Configuration WiFi Enterprise - ESP32

```cpp
#include <WiFi.h>
#include "esp_wpa2.h"

// Configuration réseau
const char* ssid = "Reseau-Entreprise";
const char* username = "mon.utilisateur";
const char* password = "monMotDePasse";

void setup() {
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();

    // Configuration EAP
    esp_wifi_sta_wpa2_ent_set_identity(
        (uint8_t*)username, strlen(username));
    esp_wifi_sta_wpa2_ent_set_username(
        (uint8_t*)username, strlen(username));
    esp_wifi_sta_wpa2_ent_set_password(
        (uint8_t*)password, strlen(password));

    esp_wifi_sta_wpa2_ent_enable();
    WiFi.begin(ssid);
}
```

---
layout: section
---

# Partie 4
## Introduction au Laboratoire 2

---

# On assemble les pièces du puzzle

<div class="text-center mb-4">

Tout ce qu'on a construit jusqu'ici va **enfin servir**!

</div>

```mermaid {scale: 0.55}
graph LR
    subgraph "Sem. 1 : Infrastructure"
        YOU[Vous] -->|SSH| CF[Cloudflare]
        CF --> RPI[RPi]
        RPI -->|Arduino CLI| CODE[Code]
    end

    subgraph "Sem. 2 : Communication"
        CODE -->|Flash| LILY[LilyGO]
        LILY <-->|"MQTT via WSS"| CF2[Cloudflare]
        CF2 <--> MOSQ[Mosquitto]
        MOSQ <--> UI[Interface]
    end

    CF -.-> CF2

    style YOU fill:#6f6
    style RPI fill:#69f
    style LILY fill:#f96
    style MOSQ fill:#f9f
```

<v-click>

<div class="mt-2 p-2 bg-green-500 bg-opacity-20 rounded-lg text-sm text-center">

Le tunnel Cloudflare sert **deux fois** : SSH pour programmer, WSS pour communiquer!

</div>

</v-click>

---

# Objectifs du Labo 2

Établir une **communication MQTT sécurisée** entre le LilyGO et le Raspberry Pi

```mermaid {scale: 0.6}
graph LR
    subgraph "LilyGO A7670G"
        ESP[ESP32 + GPIO]
    end

    subgraph "Transport"
        NET[WiFi / LTE]
        CF[Cloudflare]
    end

    subgraph "Raspberry Pi"
        MOSQ[Mosquitto]
        UI[Interface tactile]
    end

    ESP <--> NET
    NET <--> CF
    CF <--> MOSQ
    MOSQ <--> UI
```

---

# Architecture détaillée

```mermaid {scale: 0.55}
graph LR
    subgraph LILY["LilyGO A7670G"]
        ESP32[ESP32]
        GPIO[GPIO: LEDs + Boutons]
        MODEM[Modem LTE]
        ESP32 --> GPIO
        ESP32 --> MODEM
    end

    subgraph NET["Réseau"]
        WIFI[WiFi WPA-EAP]
        CELL[LTE Cat-1]
    end

    subgraph CF["Cloudflare"]
        EDGE[Edge + Tunnel]
    end

    subgraph RPI["Raspberry Pi 5"]
        MOSQ[Mosquitto :9001]
        UI[Interface Python]
        MOSQ <--> UI
    end

    ESP32 -->|WiFi| WIFI
    MODEM -->|Cellulaire| CELL
    WIFI --> EDGE
    CELL --> EDGE
    EDGE --> MOSQ
```

---

# Topics MQTT du projet

<div class="grid grid-cols-2 gap-4">

<div>

### Structure des topics

```
etudiant/{id}/
├── sensors/
│   ├── buttons  → {btn1, btn2}
│   └── status   → {uptime, rssi}
├── actuators/
│   ├── led1     ← {state}
│   └── led2     ← {state}
└── config/      ← {interval}
```

</div>

<div>

### Flux de données

| Direction | Topic |
|-----------|-------|
| LilyGO → RPi | `sensors/buttons` |
| LilyGO → RPi | `sensors/status` |
| RPi → LilyGO | `actuators/led1` |
| RPi → LilyGO | `config` |

</div>

</div>

---

# Connexion via Cloudflare Tunnel

<div class="grid grid-cols-2 gap-4">

<div>

### Sans Cloudflare

```mermaid {scale: 0.7}
graph LR
    L1[LilyGO] -->|"❌ Bloqué"| FW[NAT]
    FW -.->|"❌"| R1[RPi]
    style FW fill:#f66
```

</div>

<div>

### Avec Cloudflare

```mermaid {scale: 0.7}
graph LR
    L2[LilyGO] -->|"WSS :443"| CF[Cloudflare]
    CF -->|Tunnel| R2[RPi]
    style CF fill:#6f6
```

</div>

</div>

<v-click>

### Avantages

- ✅ Pas d'IP publique sur le RPi
- ✅ Pas de configuration routeur
- ✅ Chiffrement de bout en bout
- ✅ Fonctionne depuis n'importe où

</v-click>

---

# Configuration du tunnel MQTT

### Sur le Raspberry Pi

```bash
# Créer le tunnel pour MQTT WebSocket
cloudflared tunnel route dns mon-tunnel mqtt.mondomaine.com

# Configuration dans config.yml
ingress:
  - hostname: mqtt.mondomaine.com
    service: http://localhost:9001
  - service: http_status:404
```

<v-click>

### Connexion depuis LilyGO

```cpp
// WebSocket sécurisé via Cloudflare
const char* mqtt_host = "mqtt.mondomaine.com";
const int mqtt_port = 443;  // HTTPS/WSS

webSocket.beginSSL(mqtt_host, mqtt_port, "/", "", "mqtt");
```

</v-click>

---

# Montage électronique

<div class="grid grid-cols-2 gap-6">

<div>

### Composants

| Composant | Quantité |
|-----------|:--------:|
| LED rouge | 1 |
| LED verte | 1 |
| Résistance 220Ω | 2 |
| Bouton poussoir | 2 |
| Fils de connexion | ~10 |

</div>

<div>

### Schéma de connexion

```
GPIO 32 ──[220Ω]──[LED R]── GND
GPIO 33 ──[220Ω]──[LED V]── GND

GPIO 34 ──[BTN 1]── GND
GPIO 35 ──[BTN 2]── GND
```

⚠️ Pull-up interne activé pour les boutons

</div>

</div>

---

# Travail de la semaine

<div class="grid grid-cols-2 gap-6">

<div>

### En laboratoire

1. **Configuration Mosquitto**
   - Créer utilisateur
   - Activer WebSocket
   - Test local

2. **Configuration Cloudflare**
   - Créer tunnel MQTT
   - Configurer DNS

3. **Premier test WiFi**
   - Configuration WPA-EAP
   - Connexion MQTT

</div>

<div>

### Livrables

- Broker Mosquitto fonctionnel
- Tunnel Cloudflare configuré
- LEDs contrôlables via MQTT
- Documentation de votre configuration

</div>

</div>

<v-click>

<div class="mt-4 p-3 bg-blue-500 bg-opacity-20 rounded-lg">

📚 **Documentation**: `Labo2-communication-sans-fil-MQTT-LTE.md`

</div>

</v-click>

---

# Récapitulatif : La chaîne s'allonge

| Semaine | Problème | Solution |
|:-------:|----------|----------|
| 1 | Programmer à distance | RPi + SSH + Cloudflare |
| 1 | Synchroniser le code | Git |
| 1 | Coder efficacement | Claude Code / IA CLI |
| 1 | Compiler sans GUI | Arduino CLI |
| **2** | **Communiquer entre appareils** | **MQTT + Mosquitto** |
| **2** | **Accès MQTT sans IP publique** | **Cloudflare WSS** |

<v-click>

<div class="mt-4 p-3 bg-blue-500 bg-opacity-20 rounded-lg text-center">

**Prochaine étape** : Finaliser la communication et préparer le montage breadboard pour le PCB!

</div>

</v-click>

---
layout: center
class: text-center
---

# Questions?

<div class="text-xl mt-8">
Semaine prochaine: Finalisation communication + début montage breadboard
</div>

<div class="text-sm mt-4 opacity-70">
Évaluation "Laboratoire capteurs et Python" en semaine 3
</div>

---
layout: end
---

# Merci!

243-4J5-LI - Objets connectés

Semaine 2
