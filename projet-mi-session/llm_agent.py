import os
import sys
import time
import json
import logging
import requests
import paho.mqtt.client as mqtt
import ssl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURATION MQTT ---
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
try:
    from mqtt_config import MQTT_CONFIG
except ImportError:
    logging.error("Fichier mqtt_config.py introuvable.")
    sys.exit(1)

DEVICE_ID = MQTT_CONFIG.get("device_id", "hydro-limoilou/poste-06")

# --- CONFIGURATION GROQ (LLM) ---
API_KEY = MQTT_CONFIG.get("groq_api_key", "")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
# Using a faster/reliable model from Groq
MODEL_NAME = "llama3-8b-8192" 

# --- ETAT DES CAPTEURS ---
sensor_data = {
    "lux": None,
    "ax": None,
    "ay": None,
    "az": None,
    "uptime": None,
    "mode": None
}

# --- FONCTIONS MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("[MQTT] Connecté avec succès au broker!")
        # S'abonner aux télémétries
        client.subscribe(f"{DEVICE_ID}/telemetry/#")
        client.subscribe(f"{DEVICE_ID}/status")
    else:
        logging.error(f"[MQTT] Échec de la connexion. Code={rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8', errors='ignore')
    topic = msg.topic
    
    try:
        data = json.loads(payload)
        if topic.endswith("/telemetry/light"):
            sensor_data["lux"] = data.get("value")
            
        elif topic.endswith("/telemetry/vibration"):
            sensor_data["ax"] = data.get("x")
            sensor_data["ay"] = data.get("y")
            sensor_data["az"] = data.get("z")
            
        elif topic.endswith("/status"):
            sensor_data["mode"] = data.get("link")
            sensor_data["uptime"] = data.get("uptime")
            
    except Exception as e:
        logging.warning(f"Erreur de parsing JSON sur {topic}: {e}")

# --- APPEL A GROQ ---
def call_groq_llm():
    if sensor_data["lux"] is None or sensor_data["ax"] is None:
        return "En attente des données des capteurs..."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Création du prompt basé sur les données
    prompt = f"""Tu es un agent d'analyse de données IoT pour un poste hydroélectrique.
Voici les données actuelles en direct du site :
- Lumière ambiante : {sensor_data['lux']:.1f} lux
- Vibrations : X={sensor_data['ax']:.2f}, Y={sensor_data['ay']:.2f}, Z={sensor_data['az']:.2f} (m/s²)
- Mode de communication : {sensor_data['mode']}

Règles strictes :
1. Si la lumière est > 10000 lux, signale un ensoleillement fort. Si < 10 lux, signale qu'il fait nuit.
2. Si X ou Y dépasse 5.0, signale une ALERTE CRITIQUE de vibration/inclinaison de l'antenne.
3. Rédige un seul paragraphe court (1 ou 2 phrases). N'invente pas de données. Réponds en français.
"""

    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Tu es un système de diagnostic IoT précis et concis."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        resp_json = response.json()
        content = resp_json["choices"][0]["message"]["content"].strip()
        return content
    except Exception as e:
        logging.error(f"Erreur API Groq: {e}")
        return "Erreur d'analyse LLM."

# --- PROGRAMME PRINCIPAL ---
def main():
    logging.info("Démarrage de l'agent LLM Groq...")
    
    client = mqtt.Client(client_id=f"llm-agent-{int(time.time())}", transport="websockets")
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.username_pw_set(MQTT_CONFIG.get("username"), MQTT_CONFIG.get("password"))
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_CONFIG.get("broker"), MQTT_CONFIG.get("port", 443), 60)
        client.loop_start()
    except Exception as e:
        logging.error(f"Connexion MQTT impossible: {e}")
        sys.exit(1)

    try:
        while True:
            # On génère un résumé toutes les 30 secondes
            time.sleep(30)
            
            if sensor_data["lux"] is not None:
                logging.info("Interrogation de Groq avec les dernières données...")
                llm_response = call_groq_llm()
                
                logging.info(f"Résumé LLM : {llm_response}")
                
                # Format JSON (ou texte simple, ici texte simple)
                topic_llm = f"{DEVICE_ID}/status/llm"
                client.publish(topic_llm, llm_response)
                
    except KeyboardInterrupt:
        logging.info("Arrêt de l'agent LLM...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
