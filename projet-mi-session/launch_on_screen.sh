#!/bin/bash
# Script pour lancer l'interface de contrôle MQTT sur l'écran tactile

echo "Lancement de l'interface MQTT sur l'écran tactile..."
echo "Pour revenir au bureau: Ctrl+Alt+F7 ou 'sudo chvt 7' depuis SSH"
echo ""

# Passer sur tty1
sudo chvt 1

# Arreter getty pour liberer tty1
sudo systemctl stop getty@tty1.service

# Lancer le programme sur tty1
sudo setsid sh -c "export TERM=linux && exec </dev/tty1 >/dev/tty1 2>&1 python3 /home/admin/243-4J5-LI/projet-mi-session/touch_ui_mqtt.py"
