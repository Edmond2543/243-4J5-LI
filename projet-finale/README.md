# 🎮 Projet Mi-Session : Contrôle Interactif IoT (ESP32 & Raspberry Pi)

![Statut](https://img.shields.io/badge/Statut-Actif-success)
![Plateforme](https://img.shields.io/badge/Plateforme-ESP32%20%7C%20Raspberry%20Pi-blue)
![Protocole](https://img.shields.io/badge/Protocole-MQTT%20%7C%20Série-orange)

## 📑 Sommaire
1. [Description du projet](#-description-du-projet)
2. [Fonctionnalités](#-fonctionnalités)
3. [Matériel requis & Schéma de câblage](#-matériel-requis--schéma-de-câblage)
4. [Structure des fichiers](#-structure-des-fichiers)
5. [Dépendances](#-dépendances)
6. [Installation & Déploiement](#-installation--déploiement)
7. [Guide d'utilisation](#-guide-dutilisation)
8. [Dépannage (Troubleshooting)](#-dépannage-troubleshooting)
9. [Foire Aux Questions (FAQ)](#-foire-aux-questions-faq)
10. [Démonstration](#-démonstration)

---

## 🎯 Description du projet

Ce projet constitue une interface de contrôle interactive combinant un microcontrôleur **LilyGo T-SIM A7670G (ESP32)** et un **Raspberry Pi** équipé d'un écran tactile. Il démontre la capacité à établir une communication bidirectionnelle robuste en utilisant le protocole **MQTT** pour interagir avec des composants physiques (LEDs, boutons, potentiomètres, accéléromètre).

L'interface graphique sur le Raspberry Pi, développée avec `curses`, permet une visualisation en temps réel des données des capteurs et offre des contrôles tactiles pour actionner les périphériques de l'ESP32.

---

## ✨ Fonctionnalités

*   🟢 **Contrôle bidirectionnel des LEDs** : Allumez/éteignez les LEDs physiques depuis l'écran tactile, ou visualisez l'état des boutons physiques sur l'écran.
*   🎛️ **Mélangeur RVB interactif** : Trois potentiomètres physiques contrôlent en temps réel trois jauges à l'écran (Rouge, Vert, Bleu) simulant un mélangeur de couleurs.
*   🧭 **Boussole dynamique** : Un accéléromètre MPU6050 modifie l'orientation d'une boussole affichée sur l'interface graphique en fonction de l'inclinaison physique du capteur.
*   🌐 **Basculement réseau (Dual-Stack)** : Le système permet de basculer de manière transparente entre une connexion WiFi Enterprise et un réseau cellulaire LTE.
*   📡 **Monitoring en direct** : Affichage en temps réel des logs MQTT et des données série (console filaire) directement sur l'interface graphique.

---

## 🔌 Matériel requis & Schéma de câblage

### Composants
*   1x LilyGo T-SIM A7670G (ESP32)
*   1x Raspberry Pi avec écran tactile compatible
*   1x Module Accéléromètre MPU6050
*   3x Potentiomètres
*   2x Boutons poussoirs
*   2x LEDs (Rouge, Verte) + Résistances associées

### Câblage ESP32 (Tableau de connexion)

| Composant | Broche ESP32 | Type | Notes / Fonction |
| :--- | :--- | :--- | :--- |
| **LED Rouge** | `GPIO 15` | Sortie Digitale | Indicateur d'action "Touche" |
| **LED Verte** | `GPIO 27` | Sortie Digitale | Indicateur d'action "Manqué" |
| **Bouton Tir** | `GPIO 32` | Entrée Digitale | Utilisé avec `INPUT_PULLUP` interne |
| **Bouton Reset** | `GPIO 33` | Entrée Digitale | Utilisé avec `INPUT_PULLUP` interne |
| **Pot. Rouge** | `GPIO 34` | Entrée Analogique | ADC1 (Stable avec WiFi) |
| **Pot. Vert** | `GPIO 35` | Entrée Analogique | ADC1 (Stable avec WiFi) |
| **Pot. Bleu** | `GPIO 39` | Entrée Analogique | ADC1 (Stable avec WiFi) |
| **MPU SDA** | `GPIO 21` | I2C | Données I2C |
| **MPU SCL** | `GPIO 22` | I2C | Horloge I2C |

*(Assurez-vous de relier toutes les masses (GND) ensemble et d'alimenter les potentiomètres/MPU6050 en 3.3V depuis l'ESP32).*

---

## 📁 Structure des fichiers

```text
projet-mi-session/
├── projet-mi-session.ino   # Code source principal pour l'ESP32 (C++)
├── auth.h.example          # Modèle pour les identifiants WiFi/MQTT (à copier en auth.h)
├── touch_ui_mqtt.py        # Application Python principale pour l'interface du Raspberry Pi
├── mqtt_config.py          # Fichier de configuration MQTT pour le script Python
├── launch_on_screen.sh     # Script shell pour lancer l'UI proprement sur le terminal tty1
└── README.md               # Ce fichier de documentation
```

---

## 📦 Dépendances

### Pour l'ESP32 (Arduino IDE / CLI)
*   `WiFi`, `WiFiClientSecure` : Pour la connectivité réseau.
*   `PubSubClient` (v2.8) : Pour la communication MQTT.
*   `TinyGSM` : Pour le contrôle du modem LTE intégré.
*   `ESP_SSLClient` : Pour les connexions sécurisées TLS.
*   `Adafruit_MPU6050` & `Adafruit_Sensor` : Pour la lecture de l'accéléromètre.

### Pour le Raspberry Pi (Python 3)
*   `paho-mqtt` : Client MQTT Python.
*   `evdev` : Pour la lecture des événements de l'écran tactile.
*   `pyserial` : (Optionnel) Pour le monitoring filaire de secours.
*   `curses` : Bibliothèque standard Python pour l'interface terminal.

---

## 🚀 Installation & Déploiement

### 1. Configuration de l'ESP32
1.  Ouvrez le dossier `projet-mi-session`.
2.  Copiez `auth.h.example` vers `auth.h` et remplissez vos identifiants réels (SSID, Mots de passe, Broker MQTT).
3.  Compilez et téléversez le croquis sur la carte LilyGo :
    ```bash
    arduino-cli compile --fqbn esp32:esp32:esp32 projet-mi-session.ino
    arduino-cli upload -p /dev/ttyACM0 --fqbn esp32:esp32:esp32 projet-mi-session.ino
    ```

### 2. Configuration du Raspberry Pi
1.  Assurez-vous que les dépendances Python sont installées :
    ```bash
    sudo apt update
    sudo apt install -y python3-paho-mqtt python3-evdev python3-serial
    ```
2.  Vérifiez que le fichier `mqtt_config.py` contient les bons identifiants pour rejoindre le broker MQTT.
3.  Rendez le script de lancement exécutable :
    ```bash
    chmod +x launch_on_screen.sh
    ```

### 3. Lancement
Pour démarrer l'interface sur l'écran tactile du Raspberry Pi, exécutez :
```bash
sudo ./launch_on_screen.sh
```
L'interface prendra possession du terminal `tty1` et s'affichera en plein écran.

---

## 🕹️ Guide d'utilisation

Une fois le système lancé :
*   **Contrôle depuis l'écran** : Touchez les zones colorées "LED ROUGE" ou "LED VERTE" à l'écran. Les LEDs correspondantes sur votre breadboard s'allumeront/s'éteindront.
*   **Retour d'état physique** : Appuyez sur le bouton physique 32 ou 33 de votre montage. Le statut s'affichera instantanément dans la section "ÉVÉNEMENTS MQTT" de l'écran.
*   **Mélangeur de couleurs** : Tournez les trois potentiomètres. Les barres graphiques "R", "G" et "B" sous le bouton jaune réagiront en temps réel en fonction de la position des potentiomètres.
*   **Boussole** : Inclinez l'accéléromètre MPU6050 (avant/arrière, gauche/droite). L'aiguille de la boussole virtuelle à l'écran (affichant N, S, E, O) tournera pour refléter l'orientation.
*   **Changement de réseau** : Le bouton "SWITCH WIFI/LTE" permet d'ordonner à l'ESP32 de changer sa méthode de connexion. L'ESP32 redémarrera automatiquement sur le réseau demandé.

---

## 🛠️ Dépannage (Troubleshooting)

| Problème | Cause Possible | Solution |
| :--- | :--- | :--- |
| **L'écran du RPI reste noir au lancement** | Conflit avec le terminal `tty1` | Tapez `sudo pkill -9 python3`, puis relancez avec `./launch_on_screen.sh`. |
| **Les potentiomètres ne font pas bouger les barres** | Mauvais câblage ou WiFi actif sur l'ADC2 | Vérifiez que les pots sont sur les pins 34, 35, 39. Vérifiez l'alimentation 3.3V et le GND des pots. |
| **Les boutons physiques ne réagissent pas** | MQTT déconnecté | Regardez le bandeau supérieur de l'écran. Si le mode n'est pas affiché, vérifiez la configuration WiFi/LTE dans `auth.h`. |
| **Erreur d'upload `The chip stopped responding`** | Port série occupé ou mauvaise synchro | Maintenez le bouton `BOOT` de l'ESP32, appuyez sur `RESET`, relâchez `BOOT`, puis relancez la commande d'upload. |

---

## ❓ Foire Aux Questions (FAQ)

**Q: Pourquoi utiliser MQTT au lieu d'une connexion USB directe ?**
*R: MQTT permet de découpler totalement l'interface utilisateur du matériel. L'ESP32 pourrait être placé à l'autre bout de l'école (sur le WiFi ou en LTE), et le Raspberry Pi pourrait toujours le contrôler depuis une autre pièce.*

**Q: Pourquoi les pins 12, 13 et 14 n'ont pas été utilisées pour les potentiomètres ?**
*R: Ces broches font partie de l'ADC2 de l'ESP32. Par limitation matérielle du composant, l'ADC2 est inutilisable lorsque le module radio WiFi est activé. Nous avons donc basculé sur l'ADC1 (pins 34, 35, 39).*

**Q: Comment arrêter l'interface proprement ?**
*R: Appuyez sur le bouton "QUITTER" sur l'écran tactile, ou tapez "q" sur un clavier connecté au Raspberry Pi.*

---

## 🎥 Démonstration

*   **Lien vers la vidéo de démonstration :** [Vidéo Démo YouTube (Lien Fictif)](#)
*   **Captures d'écran :**
    *   *(Insérer image de l'interface `curses` avec la boussole et les jauges)*
    *   *(Insérer photo du montage sur la breadboard)*

---
*Projet réalisé dans le cadre du cours 243-4J5-LI (Objets connectés).*
