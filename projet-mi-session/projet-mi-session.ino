// LilyGO T-SIM A7670G - Version Projet Mi-Session
#define TINY_GSM_MODEM_SIM7600
#define TINY_GSM_RX_BUFFER 1024

#include <TinyGsmClient.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <esp_wpa2.h>
#include <Preferences.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

#define SSLCLIENT_INSECURE_ONLY
#include <ESP_SSLClient.h>
#include <mbedtls/base64.h>

#include "auth.h"

#define MODEM_TX 26
#define MODEM_RX 27
#define MODEM_PWRKEY 4

// --- CONFIGURATION PINS ---
const int LED_RED = 15;
const int LED_GREEN = 27;
const int BTN_RED_PIN = 32;
const int BTN_GREEN_PIN = 33;
const int POT_R_PIN = 34;
const int POT_G_PIN = 35;
const int POT_B_PIN = 39;

char STATUS_TOPIC[60];
char MODE_SET_TOPIC[60];
char LED_RED_SET_TOPIC[60];
char LED_GREEN_SET_TOPIC[60];
char BTN_RED_STATE_TOPIC[60];
char BTN_GREEN_STATE_TOPIC[60];

HardwareSerial SerialAT(1);
Preferences preferences;
Adafruit_MPU6050 mpu;
bool useWiFi = false;
bool mpuOk = false;

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
  if (strcmp(topic, LED_RED_SET_TOPIC) == 0) digitalWrite(LED_RED, (msg == "ON") ? HIGH : LOW);
  else if (strcmp(topic, LED_GREEN_SET_TOPIC) == 0) digitalWrite(LED_GREEN, (msg == "ON") ? HIGH : LOW);
  else if (strcmp(topic, MODE_SET_TOPIC) == 0) {
    bool targetWiFi = (msg == "WIFI");
    if (targetWiFi != useWiFi) {
        preferences.begin("net-cfg", false);
        preferences.putBool("mode_v3", targetWiFi);
        preferences.end();
        delay(1000); ESP.restart();
    }
  }
}

void setup() {
  Serial.begin(115200);
  preferences.begin("net-cfg", false);
  useWiFi = preferences.getBool("mode_v3", false);
  preferences.end();
  
  pinMode(LED_RED, OUTPUT); pinMode(LED_GREEN, OUTPUT);
  pinMode(BTN_RED_PIN, INPUT_PULLUP); pinMode(BTN_GREEN_PIN, INPUT_PULLUP);
  
  Wire.begin(21, 22);
  mpuOk = mpu.begin();
  if (mpuOk) mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  snprintf(STATUS_TOPIC, 60, "%s/status", MQTT_CLIENT_ID);
  snprintf(MODE_SET_TOPIC, 60, "%s/config/mode/set", MQTT_CLIENT_ID);
  snprintf(LED_RED_SET_TOPIC, 60, "%s/led/1/set", MQTT_CLIENT_ID);
  snprintf(LED_GREEN_SET_TOPIC, 60, "%s/led/2/set", MQTT_CLIENT_ID);
  snprintf(BTN_RED_STATE_TOPIC, 60, "%s/button/2/state", MQTT_CLIENT_ID);
  snprintf(BTN_GREEN_STATE_TOPIC, 60, "%s/button/1/state", MQTT_CLIENT_ID);

  if (useWiFi) {
    WiFi.mode(WIFI_STA);
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_USERNAME, strlen(EAP_USERNAME));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD));
    esp_wifi_sta_wpa2_ent_enable(); WiFi.begin(WIFI_SSID);
    unsigned long start = millis();
    while (WiFi.status() != WL_CONNECTED && millis()-start < 20000) delay(500);
    if (WiFi.status() == WL_CONNECTED) sslClient.setClient(&wifiClient);
  } else {
    pinMode(MODEM_PWRKEY, OUTPUT); digitalWrite(MODEM_PWRKEY, HIGH); delay(100); digitalWrite(MODEM_PWRKEY, LOW); delay(1000); digitalWrite(MODEM_PWRKEY, HIGH);
    SerialAT.begin(115200, SERIAL_8N1, MODEM_RX, MODEM_TX);
    if (modem.restart() && modem.waitForNetwork(45000L) && modem.gprsConnect(APN, APN_USER, APN_PASS)) {
      sslClient.setClient(&gsmClient);
    }
  }

  sslClient.setInsecure();
  mqttClient.setServer(MQTT_BROKER, 443);
  mqttClient.setCallback(mqttCallback);
}

unsigned long lastStat = 0, lastBtn = 0;
int lastR = HIGH, lastG = HIGH;

void loop() {
  if (!mqttClient.connected()) {
    if(wsClient.connect(MQTT_BROKER, 443)) {
      if(mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASS)) {
        mqttClient.subscribe(LED_RED_SET_TOPIC); mqttClient.subscribe(LED_GREEN_SET_TOPIC); mqttClient.subscribe(MODE_SET_TOPIC);
      }
    }
    if(!mqttClient.connected()) delay(5000);
  }
  mqttClient.loop();
  
  if (millis() - lastStat > 500) {
    lastStat = millis();
    int sig = useWiFi ? WiFi.RSSI() : modem.getSignalQuality();
    float ax = 0, ay = 0, az = 0;
    if (mpuOk) { 
        sensors_event_t a, g, temp; 
        mpu.getEvent(&a, &g, &temp); 
        ax = a.acceleration.x; ay = a.acceleration.y; az = a.acceleration.z; 
    }
    String s = "{\"mode\":\"" + String(useWiFi ? "WIFI" : "LTE") + "\", \"sig\":" + String(sig) + ", \"r\":" + String(analogRead(POT_R_PIN)) + ", \"g\":" + String(analogRead(POT_G_PIN)) + ", \"b\":" + String(analogRead(POT_B_PIN)) + ", \"ax\":" + String(ax, 1) + ", \"ay\":" + String(ay, 1) + ", \"az\":" + String(az, 1) + "}";
    mqttClient.publish(STATUS_TOPIC, s.c_str());
  }
  
  if (millis() - lastBtn > 50) {
    lastBtn = millis();
    int r = digitalRead(BTN_RED_PIN), g = digitalRead(BTN_GREEN_PIN);
    if (r != lastR) { lastR = r; mqttClient.publish(BTN_RED_STATE_TOPIC, (r == LOW) ? "PRESSED" : "RELEASED"); if(r==LOW) { digitalWrite(LED_RED, !digitalRead(LED_RED)); mqttClient.publish(LED_RED_SET_TOPIC, digitalRead(LED_RED) ? "ON" : "OFF"); } }
    if (g != lastG) { lastG = g; mqttClient.publish(BTN_GREEN_STATE_TOPIC, (g == LOW) ? "PRESSED" : "RELEASED"); if(g==LOW) { digitalWrite(LED_GREEN, !digitalRead(LED_GREEN)); mqttClient.publish(LED_GREEN_SET_TOPIC, digitalRead(LED_GREEN) ? "ON" : "OFF"); } }
  }
}
