// LilyGO T-SIM A7670G - Hybride WiFi / LTE - Site #6
#define TINY_GSM_MODEM_SIM7600
#define TINY_GSM_RX_BUFFER 1024

#include <TinyGsmClient.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <BH1750.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <esp_wpa2.h>
#include <Preferences.h>

#define SSLCLIENT_INSECURE_ONLY
#include <ESP_SSLClient.h>
#include <mbedtls/base64.h>

#include "auth.h"

#define MODEM_TX 26
#define MODEM_RX 27
#define MODEM_PWRKEY 4

const int LED_RED = 32;       // Actuator led_1
const int LED_GREEN = 33;     // Actuator led_2
const int BTN_GREEN_PIN = 25; // Button 1
const int BTN_RED_PIN = 35;   // Button 2

// Topics MQTT - Convention poste-06
const char* STATUS_TOPIC = "hydro-limoilou/poste-06/status";
const char* MODE_SET_TOPIC = "hydro-limoilou/poste-06/config/mode/set";
const char* TELEMETRY_VIBRATION_TOPIC = "hydro-limoilou/poste-06/telemetry/vibration";
const char* TELEMETRY_LIGHT_TOPIC = "hydro-limoilou/poste-06/telemetry/light";
const char* LED_1_SET_TOPIC = "hydro-limoilou/poste-06/actuators/led_1";
const char* LED_2_SET_TOPIC = "hydro-limoilou/poste-06/actuators/led_2";
const char* BTN_1_STATE_TOPIC = "hydro-limoilou/poste-06/buttons/1/state";
const char* BTN_2_STATE_TOPIC = "hydro-limoilou/poste-06/buttons/2/state";

HardwareSerial SerialAT(1);
Preferences preferences;
bool useWiFi = true; // Mode par défaut

// Capteurs I2C
Adafruit_MPU6050 mpu;
BH1750 lightMeter(0x23);

// WebSocket Wrapper
class WebSocketClient : public Client {
private:
  Client* _base; bool _ws = false; uint8_t _buf[512]; size_t _len = 0, _pos = 0;
  String genKey() { uint8_t k[16]; for(int i=0;i<16;i++) k[i]=random(0,256); size_t ol; unsigned char out[64]; mbedtls_base64_encode(out,64,&ol,k,16); return String((char*)out); }
  bool readFrame() {
    if(!_base->available()) return false;
    uint8_t b1=_base->read(), b2=_base->read();
    size_t pl = b2 & 0x7F;
    if(pl==126) pl=(_base->read()<<8)|_base->read();
    else if(pl==127) { pl=0; for(int i=0;i<8;i++) pl=(pl<<8)|_base->read(); }
    uint8_t m[4]={0}; if(b2&0x80) for(int i=0;i<4;i++) m[i]=_base->read();
    if((b1&0x0F)==0x08) { _ws=false; return false; }
    if((b1&0x0F)<0x03) {
      _len = pl < 512 ? pl : 512;
      for(size_t i=0; i<_len; i++) { _buf[i]=_base->read(); if(b2&0x80) _buf[i]^=m[i%4]; }
      _pos=0; return true;
    }
    return false;
  }
public:
  WebSocketClient(Client* b) : _base(b) {}
  int connect(IPAddress ip, uint16_t p) override { return 0; }
  int connect(const char* h, uint16_t p) override {
    if(!_base->connect(h, p)) return 0;
    _base->print("GET / HTTP/1.1\r\nHost: "+String(h)+"\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: "+genKey()+"\r\nSec-WebSocket-Protocol: mqtt\r\nSec-WebSocket-Version: 13\r\n\r\n");
    unsigned long t=millis(); while(!_base->available() && millis()-t<5000) delay(10);
    String r=""; while(_base->available()){ char c=_base->read(); r+=c; if(r.endsWith("\r\n\r\n")) break; }
    if(r.indexOf("101")>0) { _ws=true; return 1; } return 0;
  }
  size_t write(const uint8_t* b, size_t s) override {
    if(!_ws) return 0; uint8_t h[14]={0x82}; int hl=2;
    if(s<126) h[1]=0x80|s; else { h[1]=0x80|126; h[2]=s>>8; h[3]=s&0xFF; hl=4; }
    uint8_t m[4]; for(int i=0;i<4;i++){ m[i]=random(0,256); h[hl+i]=m[i]; } hl+=4;
    _base->write(h,hl); for(size_t i=0; i<s; i++){ uint8_t mb=b[i]^m[i%4]; _base->write(&mb,1); } return s;
  }
  size_t write(uint8_t b) override { return write(&b,1); }
  int available() override { if(_pos<_len) return _len-_pos; if(_base->available() && readFrame()) return _len-_pos; return 0; }
  int read() override { if(_pos<_len) return _buf[_pos++]; if(_base->available() && readFrame()) return _buf[_pos++]; return -1; }
  int read(uint8_t* b, size_t s) override { size_t c=0; while(c<s){ int v=read(); if(v<0) break; b[c++]=v; } return c; }
  int peek() override { return (_pos<_len)?_buf[_pos]:-1; }
  void flush() override { _base->flush(); }
  void stop() override { _ws=false; _base->stop(); }
  uint8_t connected() override { return _ws && _base->connected(); }
  operator bool() { return _ws; }
};

TinyGsm modem(SerialAT);
TinyGsmClient gsmClient(modem, 0);
WiFiClient wifiClient;
ESP_SSLClient sslClient;
WebSocketClient wsClient(&sslClient);
PubSubClient mqttClient(wsClient);

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg = ""; for(int i=0; i<length; i++) msg += (char)payload[i];
  Serial.println("[MQTT] Rx: " + String(topic) + " = " + msg);
  
  if (strcmp(topic, LED_1_SET_TOPIC) == 0 || strcmp(topic, LED_2_SET_TOPIC) == 0) {
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, msg);
    if (!error && doc.containsKey("state")) {
      String state = doc["state"].as<String>();
      state.toLowerCase();
      bool isOn = (state == "on");
      if (strcmp(topic, LED_1_SET_TOPIC) == 0) digitalWrite(LED_RED, isOn ? HIGH : LOW);
      else digitalWrite(LED_GREEN, isOn ? HIGH : LOW);
    } else {
      // Fallback au cas ou un msg brut est envoye
      msg.toLowerCase();
      bool isOn = (msg.indexOf("on") >= 0);
      if (strcmp(topic, LED_1_SET_TOPIC) == 0) digitalWrite(LED_RED, isOn ? HIGH : LOW);
      else digitalWrite(LED_GREEN, isOn ? HIGH : LOW);
    }
  }
  else if (strcmp(topic, MODE_SET_TOPIC) == 0) {
    bool targetWiFi = (msg == "WIFI");
    if (targetWiFi != useWiFi) { // PROTECTION BOUCLE : On ne reboot que si différent
        preferences.begin("net-cfg", false);
        preferences.putBool("mode_v4", targetWiFi);
        preferences.end();
        Serial.println("[SYSTEM] Changement de mode demandé vers " + msg + ". Reboot...");
        delay(1000); ESP.restart();
    } else {
        Serial.println("[SYSTEM] Déjà en mode " + msg + ". Ignoré.");
    }
  }
}

void setup() {
  Serial.begin(115200); delay(1000);
  Serial.println("\n\n=== HYDRO LIMOILOU - POSTE 06 ===");
  
  preferences.begin("net-cfg", false);
  useWiFi = preferences.getBool("mode_v4", true); // WiFi par défaut
  preferences.end();
  
  pinMode(LED_RED, OUTPUT); pinMode(LED_GREEN, OUTPUT);
  pinMode(BTN_RED_PIN, INPUT_PULLUP); pinMode(BTN_GREEN_PIN, INPUT_PULLUP);
  
  Wire.begin();
  if (!mpu.begin(0x68)) {
    Serial.println("[I2C] Erreur MPU6050");
  } else {
    Serial.println("[I2C] MPU6050 OK");
  }
  
  if (!lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("[I2C] Erreur BH1750");
  } else {
    Serial.println("[I2C] BH1750 OK");
  }

  bool ok = false;
  if (useWiFi) {
    Serial.println("[MODE] WIFI ENTERPRISE");
    WiFi.disconnect(true); WiFi.mode(WIFI_STA);
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_USERNAME, strlen(EAP_USERNAME));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD));
    esp_wifi_sta_wpa2_ent_enable(); 
    WiFi.begin(WIFI_SSID);
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    Serial.println("\n[WIFI] OK! IP: " + WiFi.localIP().toString()); 
    ok = true; 
    sslClient.setClient(&wifiClient);
  } else {
    Serial.println("[MODE] LTE CELLULAIRE");
    pinMode(MODEM_PWRKEY, OUTPUT); digitalWrite(MODEM_PWRKEY, HIGH); delay(100); digitalWrite(MODEM_PWRKEY, LOW); delay(1000); digitalWrite(MODEM_PWRKEY, HIGH);
    SerialAT.begin(115200, SERIAL_8N1, MODEM_RX, MODEM_TX);
    if (modem.restart() && modem.waitForNetwork(45000L) && modem.gprsConnect(APN, APN_USER, APN_PASS)) {
      Serial.println("[LTE] OK! IP: " + modem.localIP().toString()); ok = true; sslClient.setClient(&gsmClient);
    }
  }

  if(!ok) { Serial.println("[ERREUR] Connexion impossible. Reboot dans 10s."); delay(10000); ESP.restart(); }

  sslClient.setInsecure();
  mqttClient.setServer(MQTT_BROKER, 443);
  mqttClient.setCallback(mqttCallback);
}

unsigned long lastTelemetry = 0, lastBtn = 0;
int lastR = HIGH, lastG = HIGH;

void loop() {
  if (!mqttClient.connected()) {
    if(wsClient.connect(MQTT_BROKER, 443)) {
      if(mqttClient.connect("poste-06-client", MQTT_USER, MQTT_PASS)) {
        Serial.println("[MQTT] Connecté");
        mqttClient.subscribe(LED_1_SET_TOPIC); 
        mqttClient.subscribe(LED_2_SET_TOPIC);
        mqttClient.subscribe(MODE_SET_TOPIC);
      }
    }
    if(!mqttClient.connected()) delay(5000);
  }
  mqttClient.loop();
  
  // Publication toutes les 10 secondes (capteurs I2C et statut)
  if (millis() - lastTelemetry > 10000) {
    lastTelemetry = millis();
    unsigned long uptime = millis() / 1000;
    
    // 1. Status Payload
    int sig = useWiFi ? WiFi.RSSI() : modem.getSignalQuality();
    String modeStr = useWiFi ? "WIFI" : "LTE";
    String statusPayload = "{\"uptime\":" + String(uptime) + ", \"rssi\":" + String(sig) + ", \"link\":\"" + modeStr + "\"}";
    mqttClient.publish(STATUS_TOPIC, statusPayload.c_str());
    
    // 2. Vibration Payload (MPU6050)
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    String vibPayload = "{\"x\":" + String(a.acceleration.x) + 
                        ", \"y\":" + String(a.acceleration.y) + 
                        ", \"z\":" + String(a.acceleration.z) + 
                        ", \"ts\":" + String(uptime) + "}";
    mqttClient.publish(TELEMETRY_VIBRATION_TOPIC, vibPayload.c_str());
    
    // 3. Light Payload (BH1750)
    float lux = lightMeter.readLightLevel();
    String lightPayload = "{\"value\":" + String(lux) + 
                          ", \"unit\":\"lux\"" + 
                          ", \"ts\":" + String(uptime) + "}";
    mqttClient.publish(TELEMETRY_LIGHT_TOPIC, lightPayload.c_str());
    
    // 4. Alarmes (Light & Motion)
    if (lux < 1.0) {
      mqttClient.publish("hydro-limoilou/poste-06/alarms/light", "{\"status\":\"CRITICAL\",\"message\":\"Lumiere inexistante. Abris potentiellement effondre !\"}");
    } else if (lux > 15000.0) {
      mqttClient.publish("hydro-limoilou/poste-06/alarms/light", "{\"status\":\"WARNING\",\"message\":\"Lumiere tres forte. Abris expose au soleil !\"}");
    }

    if (abs(a.acceleration.x) > 3.0 || abs(a.acceleration.y) > 3.0 || a.acceleration.z < 6.0 || a.acceleration.z > 13.0) {
      mqttClient.publish("hydro-limoilou/poste-06/alarms/motion", "{\"status\":\"CRITICAL\",\"message\":\"Mouvement violent ou chute du rack detectee !\"}");
    }
  }
  
  // Lecture des boutons non-bloquante
  if (millis() - lastBtn > 250) {
    lastBtn = millis();
    int r = digitalRead(BTN_RED_PIN);
    int g = digitalRead(BTN_GREEN_PIN);
    
    if (r != lastR) { 
      lastR = r; 
      String btnState = (r == LOW) ? "{\"state\": \"pressed\"}" : "{\"state\": \"released\"}";
      mqttClient.publish(BTN_2_STATE_TOPIC, btnState.c_str()); 
      if(r == LOW) {
        digitalWrite(LED_RED, !digitalRead(LED_RED)); 
        String ledState = digitalRead(LED_RED) ? "{\"state\": \"on\"}" : "{\"state\": \"off\"}";
        mqttClient.publish(LED_1_SET_TOPIC, ledState.c_str());
      }
    }
    if (g != lastG) { 
      lastG = g; 
      String btnState = (g == LOW) ? "{\"state\": \"pressed\"}" : "{\"state\": \"released\"}";
      mqttClient.publish(BTN_1_STATE_TOPIC, btnState.c_str()); 
      if(g == LOW) {
        digitalWrite(LED_GREEN, !digitalRead(LED_GREEN)); 
        String ledState = digitalRead(LED_GREEN) ? "{\"state\": \"on\"}" : "{\"state\": \"off\"}";
        mqttClient.publish(LED_2_SET_TOPIC, ledState.c_str());
      }
    }
  }
}
