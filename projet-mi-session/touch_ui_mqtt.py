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

# ---------- UI ----------
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
        self.rgb_r = 0
        self.rgb_g = 0
        self.rgb_b = 0
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        self.mqtt_events = []
        self.serial_display = []
        
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
            client.subscribe(f"{self.device_id}/#")
            self._add_event("MQTT Connecté")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8', errors='ignore')
        if msg.topic.endswith("/status"):
            try:
                data = json.loads(payload)
                self.remote_mode = data.get("mode", "---")
                self.remote_sig = data.get("sig", 0)
                self.rgb_r = data.get("r", 0)
                self.rgb_g = data.get("g", 0)
                self.rgb_b = data.get("b", 0)
                self.accel_x = data.get("ax", 0)
                self.accel_y = data.get("ay", 0)
                self.accel_z = data.get("az", 0)
            except: pass
            return
        
        clean_topic = msg.topic.replace(f"{self.device_id}/", "")
        self._add_event(f"{clean_topic}: {payload}")
        
        # Sync LED depuis bouton physique
        if "/led/1/set" in msg.topic: self.led1_on = (payload == "ON")
        elif "/led/2/set" in msg.topic: self.led2_on = (payload == "ON")

    def _add_event(self, msg):
        self.mqtt_events.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
        if len(self.mqtt_events) > 30: self.mqtt_events.pop(0)

    def _draw_big_text(self, text, y, x, attr):
        font = {'O': ["███","█ █","█ █","█ █","███"], 'N': ["███","█ █","█ █","█ █","█ █"], 'F': ["███","█  ","██ ","█  ","█  "], ' ': ["   ","   ","   ","   ","   "]}
        for i in range(5):
            line = "".join([font.get(c, ["    "]*5)[i] + " " for c in text.upper()])
            try: self.stdscr.addstr(y + i, x - len(line)//2, line, attr)
            except: pass

    def _draw_rgb_mixer(self, start_y, start_x, bar_width):
        h, w = self.stdscr.getmaxyx()
        
        curses.init_pair(60, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(61, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(62, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(63, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        labels = [("R", self.rgb_r, 60), ("G", self.rgb_g, 61), ("B", self.rgb_b, 62)]
        
        for i, (lbl, val, pair) in enumerate(labels):
            y = start_y + i * 3
            fill = int((val / 4095) * bar_width)
            r_norm = int((val / 4095) * 255)
            
            if y < h:
                self.stdscr.addstr(y, start_x, f"{lbl}: {r_norm:3d} ", curses.color_pair(63) | curses.A_BOLD)
            
            for x in range(bar_width):
                col = start_x + 6 + x
                if y < h and col < w:
                    self.stdscr.addstr(y, col, "░", curses.color_pair(63))
            
            for x in range(fill):
                col = start_x + 6 + x
                if y < h and col < w:
                    self.stdscr.addstr(y, col, "█", curses.color_pair(pair))

    def _draw_compass(self, center_y, center_x, radius):
        h, w = self.stdscr.getmaxyx()
        
        # Calcul de l'angle en inversant X et Y selon l'orientation du capteur
        angle = math.atan2(self.accel_x, -self.accel_y)
        
        curses.init_pair(64, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(65, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        # Dessin du cadran
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
        
        # Dessin de l'aiguille
        needle_len = radius - 1
        for i in range(1, needle_len + 1):
            nx = center_x + int(i * 1.5 * math.sin(angle))
            ny = center_y - int(i * math.cos(angle))
            if 0 <= ny < h and 0 <= nx < w:
                char = "●" if i == needle_len else "·"
                self.stdscr.addstr(ny, nx, char, curses.color_pair(64) | curses.A_BOLD)

    def _draw(self):
        h, w = self.stdscr.getmaxyx()
        self.stdscr.erase()
        
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_CYAN)
        self.stdscr.addstr(0, 0, f" MODE: {self.remote_mode} | SIGNAL: {self.remote_sig} dBm ".ljust(w), curses.color_pair(10) | curses.A_BOLD)
        
        sep_col = w // 2
        
        # Boutons
        btns = [(2, "LED ROUGE (Pin 15)", self.led1_on, curses.COLOR_RED, "L1"),
                (10, "LED VERTE (Pin 27)", self.led2_on, curses.COLOR_GREEN, "L2"),
                (18, "SWITCH WIFI/LTE", None, curses.COLOR_BLUE, "MD"),
                (26, "QUITTER", None, curses.COLOR_YELLOW, "QT")]
        
        self.rects = []
        for i, (y, lbl, st, col, bid) in enumerate(btns):
            pair = i + 1
            curses.init_pair(pair, curses.COLOR_BLACK if col == curses.COLOR_YELLOW else curses.COLOR_WHITE, col)
            attr = curses.color_pair(pair)
            for r in range(y, y+7): 
                if r < h: self.stdscr.addstr(r, 1, " "*(sep_col-2), attr)
            self.stdscr.addstr(y+1, sep_col//2 - len(lbl)//2, lbl, attr | curses.A_BOLD)
            if st is not None: self._draw_big_text("ON" if st else "OFF", y+2, sep_col//2, attr)
            self.rects.append((y, y+7, bid))
        
        # Mélangeur RVB
        self._draw_rgb_mixer(34, 2, sep_col - 6)
        
        # Boussole
        self._draw_compass(46, sep_col // 2, 5)
        
        # Logs
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
