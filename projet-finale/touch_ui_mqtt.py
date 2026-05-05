import threading
import time
import os
import sys
import json
from queue import Queue
import logging
import math
import curses
import paho.mqtt.client as mqtt
import ssl
import serial
from evdev import InputDevice, ecodes, list_devices

logging.basicConfig(filename='/tmp/mqtt_ui_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
try:
    from mqtt_config import MQTT_CONFIG
except ImportError:
    sys.exit(1)

# ---------- LECTURE SÉRIE ----------
class SerialReader(threading.Thread):
    def __init__(self, log_queue):
        super().__init__(daemon=True)
        self.log_queue = log_queue
    def run(self):
        while True:
            try:
                if os.path.exists('/dev/ttyACM0'):
                    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
                        self.log_queue.put("--- Port Série Connecté ---")
                        while True:
                            line = ser.readline().decode('utf-8', errors='ignore').strip()
                            if line: self.log_queue.put(line)
                else: time.sleep(2)
            except: time.sleep(2)

# ---------- TOUCH ----------
class TouchReader(threading.Thread):
    def __init__(self, event_queue):
        super().__init__(daemon=True)
        self.event_queue = event_queue
        self.device = self._find_touch_device()
        self.min_x, self.max_x = 0, 800
        self.min_y, self.max_y = 0, 480
        if self.device:
            try:
                abs_x = self.device.absinfo(ecodes.ABS_MT_POSITION_X)
                abs_y = self.device.absinfo(ecodes.ABS_MT_POSITION_Y)
                self.min_x, self.max_x = abs_x.min, abs_x.max
                self.min_y, self.max_y = abs_y.min, abs_y.max
            except: pass
        self.current_x = (self.min_x + self.max_x) // 2
        self.current_y = (self.min_y + self.max_y) // 2

    def _find_touch_device(self):
        for path in list_devices():
            dev = InputDevice(path)
            if "touch" in dev.name.lower() or "goodix" in dev.name.lower():
                return dev
        return None

    def run(self):
        if not self.device: return
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_ABS:
                    if event.code == ecodes.ABS_MT_POSITION_X: self.current_x = event.value
                    elif event.code == ecodes.ABS_MT_POSITION_Y: self.current_y = event.value
                elif event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH:
                    if event.value == 1: self.event_queue.put(("tap", self.current_x, self.current_y))
        except: pass

# ---------- UI AVEC ONGLETS ----------
class MQTTControlUI:
    def __init__(self, stdscr, touch_reader, event_queue, serial_logs):
        self.stdscr = stdscr
        self.touch_reader = touch_reader
        self.event_queue = event_queue
        self.serial_logs = serial_logs
        self.running = True
        
        self.device_id = MQTT_CONFIG.get("device_id", "hydro-limoilou/poste-06")

        # États des capteurs / actuateurs
        self.led1_on = False
        self.led2_on = False
        self.btn1_state = "RELEASED"
        self.btn2_state = "RELEASED"
        
        self.remote_mode = "---"
        self.remote_sig = 0
        self.uptime = 0
        
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 9.81
        
        self.light_lux = 0.0
        
        self.mqtt_events = []
        self.alarms = [] # dicts: {"msg": str, "ts": time, "ack": bool}
        
        # Onglets
        self.pages = ["1. CONTRÔLE", "2. TÉLÉMÉTRIE", "3. ALARMES", "4. RÉSEAU"]
        self.current_page = 0
        self.tabs_rects = []
        self.buttons_rects = []
        
        self.client = mqtt.Client(client_id=f"pi-gui-{int(time.time())}", transport="websockets")
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
        self.client.username_pw_set(MQTT_CONFIG.get("username"), MQTT_CONFIG.get("password"))
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        try:
            self.client.connect(MQTT_CONFIG.get("broker"), 443, 60)
            self.client.loop_start()
        except: pass

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(f"{self.device_id}/#")
            self._add_event("MQTT Connecté")

    def _add_alarm(self, msg):
        # Vérifie si l'alarme existe déjà non-acquittée
        for a in self.alarms:
            if a["msg"] == msg and not a["ack"]:
                return
        self.alarms.insert(0, {"msg": msg, "ts": time.time(), "ack": False})

    def _check_alarms(self):
        # Seuils basiques
        if self.light_lux > 10000:
            self._add_alarm("Luminosité TRÈS FORTE (> 10000 lux)")
        if abs(self.accel_x) > 5.0 or abs(self.accel_y) > 5.0:
            self._add_alarm("Vibration / Inclinaison excessive détectée")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8', errors='ignore')
        topic = msg.topic
        
        if topic.endswith("/status"):
            try:
                data = json.loads(payload)
                self.remote_mode = data.get("link", "LTE").upper()
                self.remote_sig = data.get("rssi", 0)
                self.uptime = data.get("uptime", 0)
            except: pass
        
        elif topic.endswith("/telemetry/vibration"):
            try:
                data = json.loads(payload)
                self.accel_x = data.get("x", 0.0)
                self.accel_y = data.get("y", 0.0)
                self.accel_z = data.get("z", 9.81)
                self.uptime = data.get("ts", self.uptime)
                self._check_alarms()
            except: pass
            
        elif topic.endswith("/telemetry/light"):
            try:
                data = json.loads(payload)
                self.light_lux = data.get("value", 0.0)
                self._check_alarms()
            except: pass
            
        elif "/actuators/led_1" in topic:
            try:
                data = json.loads(payload)
                self.led1_on = (data.get("state", "").lower() == "on")
            except:
                self.led1_on = (payload == "ON")
        elif "/actuators/led_2" in topic:
            try:
                data = json.loads(payload)
                self.led2_on = (data.get("state", "").lower() == "on")
            except:
                self.led2_on = (payload == "ON")
            
        elif "/buttons/1/state" in topic:
            try:
                data = json.loads(payload)
                self.btn1_state = data.get("state", "unknown").upper()
            except:
                self.btn1_state = payload
        elif "/buttons/2/state" in topic:
            try:
                data = json.loads(payload)
                self.btn2_state = data.get("state", "unknown").upper()
            except:
                self.btn2_state = payload
                
        elif "/alarms/" in topic:
            try:
                data = json.loads(payload)
                self._add_alarm(f"[{data.get('status', 'ALERTE')}] {data.get('message', 'Alarme capteur')}")
            except:
                self._add_alarm(payload)

        self._add_event(f"{topic.split('/')[-1]}: {payload}")

    def _add_event(self, msg):
        self.mqtt_events.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        if len(self.mqtt_events) > 15: self.mqtt_events.pop(0)

    def _draw_big_text(self, text, y, x, attr):
        font = {'O': ["███","█ █","█ █","█ █","███"], 'N': ["███","█ █","█ █","█ █","█ █"], 'F': ["███","█  ","██ ","█  ","█  "], ' ': ["   ","   ","   ","   ","   "]}
        for i in range(5):
            line = "".join([font.get(c, ["    "]*5)[i] + " " for c in text.upper()])
            try: self.stdscr.addstr(y + i, x - len(line)//2, line, attr)
            except: pass

    def _draw_tabs(self, w):
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        self.tabs_rects = []
        tab_w = w // len(self.pages)
        for i, title in enumerate(self.pages):
            attr = curses.color_pair(10) if i == self.current_page else curses.color_pair(11)
            # Bouton de tabulation plus gros (3 lignes de haut)
            label = f" {title} "
            start_x = i * tab_w
            end_x = start_x + tab_w - 1
            
            pad = (tab_w - len(label)) // 2
            
            for row in range(3):
                try:
                    if row == 1:
                        self.stdscr.addstr(row, start_x, " "*pad + label + " "*(tab_w - pad - len(label)), attr | curses.A_BOLD)
                    else:
                        self.stdscr.addstr(row, start_x, " "*tab_w, attr | curses.A_BOLD)
                except: pass
            
            self.tabs_rects.append((0, start_x, 2, end_x, i)) # row_start, col_start, row_end, col_end, tab_index

    def _draw_page_control(self, h, w):
        # LEDs
        btns = [(3, "LED ROUGE (Actuator 1)", self.led1_on, curses.COLOR_RED, "L1"),
                (12, "LED VERTE (Actuator 2)", self.led2_on, curses.COLOR_GREEN, "L2"),
                (21, f"BASCULER LE MODE", "SW", curses.COLOR_BLUE, "MD")]
        
        for i, (y, lbl, st, col, bid) in enumerate(btns):
            pair = i + 1
            curses.init_pair(pair, curses.COLOR_WHITE, col)
            attr = curses.color_pair(pair)
            
            for r in range(y, y+7):
                if r < h: self.stdscr.addstr(r, 2, " "*30, attr)
            
            self.stdscr.addstr(y+1, 17 - len(lbl)//2, lbl, attr | curses.A_BOLD)
            if isinstance(st, bool):
                self._draw_big_text("ON" if st else "OFF", y+2, 17, attr)
            else:
                self._draw_big_text(str(st), y+2, 17, attr)
            self.buttons_rects.append((y, 2, y+6, 32, bid)) # rs, cs, re, ce, id
            
        # Physical Buttons state
        curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.stdscr.addstr(3, 40, "ÉTAT DES BOUTONS PHYSIQUES", curses.color_pair(12) | curses.A_BOLD)
        self.stdscr.addstr(5, 40, f"BOUTON 1 (Vert) : {self.btn1_state}")
        self.stdscr.addstr(7, 40, f"BOUTON 2 (Rouge): {self.btn2_state}")
        
        # Events
        self.stdscr.addstr(12, 40, "--- DERNIERS ÉVÉNEMENTS MQTT ---", curses.A_BOLD | curses.A_UNDERLINE)
        for i, m in enumerate(self.mqtt_events[-10:]):
            try: self.stdscr.addstr(13+i, 40, m[:w-42])
            except: pass
            
    def _draw_compass(self, center_y, center_x, radius):
        h, w = self.stdscr.getmaxyx()
        angle = math.atan2(self.accel_x, -self.accel_y)
        curses.init_pair(64, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(65, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        for a in range(0, 360, 30):
            rad = math.radians(a)
            dx = int(radius * 1.5 * math.sin(rad))
            dy = int(radius * math.cos(rad))
            row = center_y + dy
            col = center_x + dx
            if 0 <= row < h and 0 <= col < w:
                if a == 0: self.stdscr.addstr(row, col, "N", curses.color_pair(64) | curses.A_BOLD)
                elif a == 90: self.stdscr.addstr(row, col, "E", curses.color_pair(64) | curses.A_BOLD)
                elif a == 180: self.stdscr.addstr(row, col, "S", curses.color_pair(64) | curses.A_BOLD)
                elif a == 270: self.stdscr.addstr(row, col, "O", curses.color_pair(64) | curses.A_BOLD)
                else: self.stdscr.addstr(row, col, ".", curses.color_pair(65))
        
        needle_len = radius - 1
        for i in range(1, needle_len + 1):
            nx = center_x + int(i * 1.5 * math.sin(angle))
            ny = center_y - int(i * math.cos(angle))
            if 0 <= ny < h and 0 <= nx < w:
                char = "●" if i == needle_len else "·"
                self.stdscr.addstr(ny, nx, char, curses.color_pair(64) | curses.A_BOLD)

    def _draw_page_telemetry(self, h, w):
        curses.init_pair(20, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        # Lumière
        self.stdscr.addstr(3, 5, "CAPTEUR DE LUMIÈRE (BH1750)", curses.color_pair(20) | curses.A_BOLD)
        self.stdscr.addstr(5, 5, f"Valeur : {self.light_lux:.1f} lux")
        
        # Jauge Lumière (Log scale)
        bar_len = 30
        lux_log = math.log10(max(1, self.light_lux))
        fill = int(min(1.0, lux_log / 5.0) * bar_len) # max scale around 100,000 lux
        self.stdscr.addstr(7, 5, "[" + "█"*fill + " "*(bar_len-fill) + "]")
        
        # Vibrations
        self.stdscr.addstr(12, 5, "VIBRATIONS & INCLINAISON (MPU6050)", curses.color_pair(20) | curses.A_BOLD)
        self.stdscr.addstr(14, 5, f"Axe X : {self.accel_x:6.2f} m/s²")
        self.stdscr.addstr(15, 5, f"Axe Y : {self.accel_y:6.2f} m/s²")
        self.stdscr.addstr(16, 5, f"Axe Z : {self.accel_z:6.2f} m/s²")
        
        # Boussole (Inclinaison)
        self._draw_compass(15, 50, 6)

    def _draw_page_alarms(self, h, w):
        curses.init_pair(30, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(31, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(32, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        
        self.stdscr.addstr(3, 2, "HISTORIQUE DES ALARMES", curses.A_BOLD | curses.A_UNDERLINE)
        
        # ACK ALL Bouton
        ack_btn_y = 3
        ack_btn_x = w - 20
        self.stdscr.addstr(ack_btn_y, ack_btn_x, " [ ACQUITTEMENT ] ", curses.color_pair(32) | curses.A_BOLD)
        self.buttons_rects.append((ack_btn_y, ack_btn_x, ack_btn_y, ack_btn_x+18, "ACK"))
        
        if not self.alarms:
            self.stdscr.addstr(6, 2, "Aucune alarme enregistrée.", curses.color_pair(31))
            return
            
        for i, al in enumerate(self.alarms[:15]):
            ts_str = time.strftime('%H:%M:%S', time.localtime(al["ts"]))
            ack_str = "[ACK]" if al["ack"] else "[!]"
            attr = curses.color_pair(31) if al["ack"] else curses.color_pair(30)
            self.stdscr.addstr(6+i, 2, f"{ts_str} {ack_str} {al['msg']}", attr | curses.A_BOLD)

    def _draw_page_network(self, h, w):
        curses.init_pair(40, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.stdscr.addstr(3, 2, "ÉTAT DU LIEN DE COMMUNICATION", curses.color_pair(40) | curses.A_BOLD)
        
        self.stdscr.addstr(5, 5, f"Identifiant Station : {self.device_id}")
        self.stdscr.addstr(7, 5, f"Mode réseau         : {self.remote_mode}")
        self.stdscr.addstr(8, 5, f"Qualité Signal (RSSI): {self.remote_sig} dBm")
        
        # Format Uptime
        hrs = self.uptime // 3600
        mins = (self.uptime % 3600) // 60
        secs = self.uptime % 60
        self.stdscr.addstr(10, 5, f"Temps de service    : {hrs:02d}h {mins:02d}m {secs:02d}s")
        
        # Jauge signal
        sig_val = min(31, max(0, int(self.remote_sig))) # Pour GSM: 0-31
        bar_len = 31
        fill = sig_val
        self.stdscr.addstr(12, 5, "Niveau RF: [" + "█"*fill + " "*(bar_len-fill) + "]")

        # Bouton quitter la GUI
        quit_y = h - 3
        quit_x = w // 2 - 5
        curses.init_pair(41, curses.COLOR_WHITE, curses.COLOR_RED)
        self.stdscr.addstr(quit_y, quit_x, " QUITTER ", curses.color_pair(41) | curses.A_BOLD)
        self.buttons_rects.append((quit_y, quit_x, quit_y, quit_x+8, "QT"))

    def _draw(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        self.buttons_rects.clear()
        
        self._draw_tabs(w)
        
        if self.current_page == 0: self._draw_page_control(h, w)
        elif self.current_page == 1: self._draw_page_telemetry(h, w)
        elif self.current_page == 2: self._draw_page_alarms(h, w)
        elif self.current_page == 3: self._draw_page_network(h, w)
        
        self.stdscr.refresh()

    def run(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        while self.running:
            self._draw()
            ch = self.stdscr.getch()
            if ch == ord('q'): break
            elif ch == curses.KEY_RIGHT: self.current_page = (self.current_page + 1) % 4
            elif ch == curses.KEY_LEFT: self.current_page = (self.current_page - 1) % 4
            
            while not self.event_queue.empty():
                ev = self.event_queue.get_nowait()
                if ev[0] == "tap":
                    h, w = self.stdscr.getmaxyx()
                    dx = max(1, self.touch_reader.max_x - self.touch_reader.min_x)
                    dy = max(1, self.touch_reader.max_y - self.touch_reader.min_y)
                    tx = int(((ev[1] - self.touch_reader.min_x) / dx) * (w-1))
                    ty = int(((ev[2] - self.touch_reader.min_y) / dy) * (h-1))
                    
                    # Verif Tabs
                    for rs, cs, re, ce, idx in self.tabs_rects:
                        if rs <= ty <= re and cs <= tx <= ce:
                            self.current_page = idx
                            
                    # Verif Boutons de la page active
                    for rs, cs, re, ce, bid in self.buttons_rects:
                        if rs <= ty <= re and cs <= tx <= ce:
                            if bid == "L1":
                                cmd = '{"state": "off"}' if self.led1_on else '{"state": "on"}'
                                self.client.publish(f"{self.device_id}/actuators/led_1", cmd)
                            elif bid == "L2":
                                cmd = '{"state": "off"}' if self.led2_on else '{"state": "on"}'
                                self.client.publish(f"{self.device_id}/actuators/led_2", cmd)
                            elif bid == "MD":
                                nm = "LTE" if self.remote_mode == "WIFI" else "WIFI"
                                self.client.publish(f"{self.device_id}/config/mode/set", nm)
                                self._add_event(f"ACTION: Mode -> {nm}")
                            elif bid == "ACK":
                                for a in self.alarms: a["ack"] = True
                            elif bid == "QT":
                                self.running = False
            time.sleep(0.05)

def main(stdscr):
    eq, sl = Queue(), Queue()
    tr = TouchReader(eq)
    tr.start()
    SerialReader(sl).start()
    MQTTControlUI(stdscr, tr, eq, sl).run()

if __name__ == "__main__":
    curses.wrapper(main)
