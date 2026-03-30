# Projet Mi-Session: Contrôle Interactif (ESP32 + RPI)

Ce projet permet de contrôler des composants physiques via une interface tactile sur un Raspberry Pi et un microcontrôleur ESP32, en utilisant le protocole MQTT et une liaison Série.

## Fonctionnalités

1. **Contrôle des LEDs** : L'interface tactile permet d'allumer et d'éteindre les LEDs branchées sur l'ESP32.
2. **Boutons physiques** : Appuyer sur les boutons physiques met à jour l'interface en temps réel.
3. **Mélangeur RVB (RGB)** : Trois potentiomètres contrôlent en temps réel l'affichage de trois jauges colorées sur l'écran.
4. **Boussole interactive** : Un accéléromètre (MPU6050) fait bouger une aiguille de boussole sur l'écran en fonction de l'inclinaison.
5. **Basculement Réseau** : Possibilité de passer du réseau WiFi au réseau cellulaire (LTE) via l'interface.

## Matériel (Câblage ESP32)

| Composant | Pin ESP32 | Notes |
| :--- | :--- | :--- |
| LED Rouge | 15 | |
| LED Verte | 27 | |
| Bouton Tir | 32 | Pull-up interne |
| Bouton Reset| 33 | Pull-up interne |
| Pot. Rouge | 34 | ADC1 |
| Pot. Vert | 35 | ADC1 |
| Pot. Bleu | 39 | ADC1 |
| MPU6050 SDA | 21 | I2C |
| MPU6050 SCL | 22 | I2C |

## Lancement

**Sur l'ESP32 :**
Téléversez le fichier `projet-mi-session.ino`.

**Sur le Raspberry Pi :**
Exécutez le script de lancement pour afficher l'interface sur l'écran tactile :
```bash
sudo pkill -9 python3
cd ~/243-4J5-LI/labo/Labo-02/led-control/
sudo ./launch_on_screen.sh
```
