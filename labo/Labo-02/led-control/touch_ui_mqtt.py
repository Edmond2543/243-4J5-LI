import threading
import time
import os
import sys
import json
from queue import Queue
import logging

import curses
import paho.mqtt.client as mqtt
import ssl
import serial # Pour lire les logs filaires
from evdev import InputDevice, ecodes, list_devices

# Configurer le logging
logging.basicConfig(filename='/tmp/mqtt_ui_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration MQTT
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
try:
    from mqtt_config import MQTT_CONFIG
    logging.info("Config MQTT OK")
except ImportError:
    logging.error("Config MQTT manquante")
    sys.exit(1)

# ---------- LECTURE SÉRIE (FILAIRE) ----------

class SerialReader(threading.Thread):
    def __init__(self, log_queue: Queue):
        super().__init__(daemon=True)
        self.log_queue = log_queue
        self.port = '/dev/ttyACM0'
        
    def run(self):
        logging.info(f"Démarrage SerialReader sur {self.port}")
        while True:
            try:
                if os.path.exists(self.port):
                    with serial.Serial(self.port, 115200, timeout=1) as ser:
                        self.log_queue.put("--- Port Série Connecté ---")
                        while True:
                            line = ser.readline().decode('utf-8', errors='ignore').strip()
                            if line:
                                self.log_queue.put(line)
                else:
                    time.sleep(2)
            except Exception as e:
                logging.error(f"Erreur SerialReader: {e}")
                time.sleep(2)

# ---------- GESTION DU TOUCH ----------

class TouchReader(threading.Thread):
    def __init__(self, event_queue: Queue):
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
                logging.info(f"Touch calibré: {self.min_x}-{self.max_x}")
            except: pass
        self.current_x = (self.min_x + self.max_x) // 2
        self.current_y = (self.min_y + self.max_y) // 2

    def _find_touch_device(self):
        try:
            for path in list_devices():
                dev = InputDevice(path)
                if "touch" in dev.name.lower() or "goodix" in dev.name.lower():
                    return dev
        except: pass
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

# ---------- UI CURSES ----------

class MQTTControlUI:
    def __init__(self, stdscr, touch_reader, event_queue, serial_logs):
        self.stdscr = stdscr
        self.touch_reader = touch_reader
        self.event_queue = event_queue
        self.serial_logs = serial_logs
        self.running = True
        
        self.led1_on = False
        self.led2_on = False
        self.remote_mode = "---"
        self.remote_sig = 0
        self.mqtt_events = []
        self.serial_display = []
        
        # MQTT
        self.client = mqtt.Client(client_id=f"pi-gui-{int(time.time())}", transport="websockets")
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
        self.client.username_pw_set(MQTT_CONFIG.get("username"), MQTT_CONFIG.get("password"))
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        self.device_id = MQTT_CONFIG.get("device_id")
        self.topic_mode = f"{self.device_id}/config/mode/set"
        
        try:
            self.client.connect(MQTT_CONFIG.get("broker"), 443, 60)
            self.client.loop_start()
        except: pass

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.subscribe(f"{self.device_id}/#")
            self._add_event("MQTT Connecté")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8', errors='ignore')
        if msg.topic.endswith("/status"):
            try:
                data = json.loads(payload)
                self.remote_mode = data.get("mode", "---")
                self.remote_sig = data.get("sig", 0)
            except: pass
            return
        
        clean_topic = msg.topic.replace(f"{self.device_id}/", "")
        self._add_event(f"{clean_topic}: {payload}")
        
        # Sync local state
        if "/led/1/" in msg.topic: self.led1_on = (payload == "ON")
        elif "/led/2/" in msg.topic: self.led2_on = (payload == "ON")

    def _add_event(self, msg):
        self.mqtt_events.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        if len(self.mqtt_events) > 30: self.mqtt_events.pop(0)

    def _draw_big_text(self, text, y, x, attr):
        font = {'O': ["███","█ █","█ █","█ █","███"], 'N': ["███","█ █","█ █","█ █","█ █"], 'F': ["███","█  ","██ ","█  ","█  "], ' ': ["   ","   ","   ","   ","   "]}
        for i in range(5):
            line = "".join([font.get(c, ["    "]*5)[i] + " " for c in text.upper()])
            try: self.stdscr.addstr(y + i, x - len(line)//2, line, attr)
            except: pass

    def _draw(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        
        # Header
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_CYAN)
        self.stdscr.addstr(0, 0, f" MODE: {self.remote_mode} | SIGNAL: {self.remote_sig} dBm ".ljust(w), curses.color_pair(10) | curses.A_BOLD)
        
        sep_col = w // 2
        # Zone Gauche (Boutons)
        btns = [(2, "LED ROUGE (32)", self.led1_on, curses.COLOR_RED, "L1"),
                (11, "LED VERTE (33)", self.led2_on, curses.COLOR_GREEN, "L2"),
                (20, "SWITCH WIFI/LTE", None, curses.COLOR_BLUE, "MD"),
                (29, "QUITTER", None, curses.COLOR_YELLOW, "QT")]
        
        self.rects = []
        for i, (y, lbl, st, col, bid) in enumerate(btns):
            pair = i + 1
            curses.init_pair(pair, curses.COLOR_BLACK if col == curses.COLOR_YELLOW else curses.COLOR_WHITE, col)
            attr = curses.color_pair(pair)
            for r in range(y, y+8): 
                if r < h: self.stdscr.addstr(r, 1, " "*(sep_col-2), attr)
            self.stdscr.addstr(y+1, sep_col//2 - len(lbl)//2, lbl, attr | curses.A_BOLD)
            if st is not None: self._draw_big_text("ON" if st else "OFF", y+2, sep_col//2, attr)
            self.rects.append((y, y+8, bid))

        # Zone Droite (Logs)
        mid_h = h // 2
        self.stdscr.addstr(1, sep_col+2, "--- ÉVÉNEMENTS MQTT ---", curses.A_BOLD | curses.A_UNDERLINE)
        for i, m in enumerate(self.mqtt_events[-(mid_h-3):]):
            try: self.stdscr.addstr(2+i, sep_col+2, m[:w-sep_col-3])
            except: pass
        
        self.stdscr.addstr(mid_h, sep_col+2, "--- CONSOLE SÉRIE (FILAIRE) ---", curses.A_BOLD | curses.A_UNDERLINE)
        while not self.serial_logs.empty():
            self.serial_display.append(self.serial_logs.get_nowait())
            if len(self.serial_display) > 100: self.serial_display.pop(0)
        
        for i, m in enumerate(self.serial_display[-(h-mid_h-2):]):
            try: self.stdscr.addstr(mid_h+1+i, sep_col+2, m[:w-sep_col-3])
            except: pass

        for r in range(1, h): 
            try: self.stdscr.addstr(r, sep_col, "│")
            except: pass
        self.stdscr.refresh()

    def run(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        while self.running:
            self._draw()
            ch = self.stdscr.getch()
            if ch == ord('q'): break
            while not self.event_queue.empty():
                ev = self.event_queue.get_nowait()
                if ev[0] == "tap":
                    h, w = self.stdscr.getmaxyx()
                    dx = max(1, self.touch_reader.max_x - self.touch_reader.min_x)
                    dy = max(1, self.touch_reader.max_y - self.touch_reader.min_y)
                    tx = int(((ev[1] - self.touch_reader.min_x) / dx) * (w-1))
                    ty = int(((ev[2] - self.touch_reader.min_y) / dy) * (h-1))
                    if tx < w // 2:
                        for s, e, bid in self.rects:
                            if s <= ty <= e:
                                if bid == "L1": 
                                    cmd = "OFF" if self.led1_on else "ON"
                                    self.client.publish(f"{self.device_id}/led/1/set", cmd)
                                elif bid == "L2": 
                                    cmd = "OFF" if self.led2_on else "ON"
                                    self.client.publish(f"{self.device_id}/led/2/set", cmd)
                                elif bid == "MD": 
                                    nm = "LTE" if self.remote_mode == "WIFI" else "WIFI"
                                    self._add_event(f"ACTION: Switch vers {nm}")
                                    self.client.publish(self.topic_mode, nm)
                                elif bid == "QT": self.running = False
            time.sleep(0.05)

def main(stdscr):
    eq, sl = Queue(), Queue()
    tr = TouchReader(eq)
    tr.start()
    SerialReader(sl).start()
    MQTTControlUI(stdscr, tr, eq, sl).run()

if __name__ == "__main__":
    curses.wrapper(main)
