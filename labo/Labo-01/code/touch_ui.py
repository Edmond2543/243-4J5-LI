import threading
import time
import os
import sys
from queue import Queue
import logging

import curses
import serial
from evdev import InputDevice, ecodes, list_devices

# Configurer le logging
logging.basicConfig(filename='/tmp/ui_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration Série pour ESP32
SERIAL_PORT = '/dev/ttyACM0'

BAUD_RATE = 115200


# ---------- GESTION DU TOUCH ----------

class TouchReader(threading.Thread):
    def __init__(self, event_queue: Queue):
        super().__init__(daemon=True)
        self.event_queue = event_queue
        self.device = self._find_touch_device()
        if not self.device:
            # En mode dev/test sans écran tactile, on ne plante pas tout de suite,
            # mais l'UI ne réagira pas au touch.
            print("ATTENTION: Aucun périphérique touchscreen trouvé. Mode affichage seul.")
            self.device = None
        else:
            # On récupère les infos d’axes pour calibrer
            abs_x = self.device.absinfo(ecodes.ABS_MT_POSITION_X)
            abs_y = self.device.absinfo(ecodes.ABS_MT_POSITION_Y)

            self.min_x, self.max_x = abs_x.min, abs_x.max
            self.min_y, self.max_y = abs_y.min, abs_y.max

            self.current_x = (self.min_x + self.max_x) // 2
            self.current_y = (self.min_y + self.max_y) // 2

    def _find_touch_device(self):
        """
        Essaie de trouver un device dont le nom contient 'touch' ou 'ft5406'
        (fréquent sur les écrans Raspberry Pi).
        """
        try:
            for path in list_devices():
                dev = InputDevice(path)
                name = dev.name.lower()
                if "touch" in name or "ft5406" in name:
                    # print(f"[TouchReader] Using device: {dev.name} ({path})")
                    return dev
        except ImportError:
            pass # Si list_devices plante
        return None

    def run(self):
        if not self.device:
            return

        for event in self.device.read_loop():
            if event.type == ecodes.EV_ABS:
                if event.code == ecodes.ABS_MT_POSITION_X:
                    self.current_x = event.value
                elif event.code == ecodes.ABS_MT_POSITION_Y:
                    self.current_y = event.value

            elif event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH:
                # 1 = touch down, 0 = touch up
                if event.value == 1:
                    # On push un "tap" dans la queue avec les coordonnées brutes
                    self.event_queue.put(("tap", self.current_x, self.current_y))


# ---------- UI CURSES ----------

class CoolConsoleUI:
    def __init__(self, stdscr, touch_reader, event_queue: Queue):
        self.stdscr = stdscr
        self.touch_reader = touch_reader
        self.event_queue = event_queue
        self.running = True
        self.status_message = "Prêt. Connectez l'ESP32."

        self.buttons = []
        
        # État des LEDs
        self.red_on = False
        self.green_on = False
        self.last_tap_time = 0 # Pour le debounce
        
        # Connexion Série
        self.ser = None
        self._connect_serial()

    def _connect_serial(self):
        try:
            logging.info(f"Tentative de connexion à {SERIAL_PORT}...")
            # DTR = False pour éviter le reset de l'ESP32
            self.ser = serial.Serial()
            self.ser.port = SERIAL_PORT
            self.ser.baudrate = BAUD_RATE
            self.ser.timeout = 0.1
            
            # Configuration explicite des lignes de contrôle pour ESP32
            self.ser.dtr = False 
            self.ser.rts = False
            
            self.ser.open()
            self.status_message = f"Connecté à {SERIAL_PORT}"
            logging.info("Connexion série RÉUSSIE")
        except Exception as e:
            self.status_message = f"Erreur Série: {e}"
            logging.error(f"Erreur connexion série: {e}")

    def _send_cmd(self, cmd):
        if self.ser and self.ser.is_open:
            try:
                logging.info(f"Envoi commande: {cmd}")
                self.ser.write((cmd + '\n').encode())
                self.ser.flush() # Forcer l'envoi
                # Lire la réponse potentielle (non bloquant grâce au timeout court)
                # reponse = self.ser.readline().decode().strip()
                # if reponse:
                #     self.status_message = f"Rép: {reponse}"
            except Exception as e:
                self.status_message = f"Erreur envoi: {e}"
                logging.error(f"Erreur envoi commande: {e}")
        else:
            self.status_message = "Série non connecté!"
            logging.warning("Tentative envoi sans connexion. Reconnexion...")
            # Tenter reconnexion ?
            self._connect_serial()

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        # Pair 1: Status
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   
        # Pair 2: Active / Highlight
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)  
        # Pair 3: Status text
        curses.init_pair(3, curses.COLOR_CYAN, -1)                   
        # Pair 4: Title
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)   
        
        # Pair 5: ROUGE OFF (Sombre)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        # Pair 6: ROUGE ON (Vif/Fond rouge)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)

        # Pair 7: VERT OFF (Sombre)
        curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # Pair 8: VERT ON (Vif/Fond vert)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_GREEN)

        # Pair 9: QUIT
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        # Pair 10: Border
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK) 

    def _build_buttons(self, h, w):
        """
        Construit l'interface : 2 gros boutons LED + Bouton Quit
        """
        self.buttons = []
        
        # --- Configuration Layout ---
        # On veut deux gros boutons côte à côte pour les LEDs
        
        margin_x = 4
        margin_y = 4
        available_w = w - (2 * margin_x)
        # Hauteur dispo : on garde de la place pour titre (2) et status (2) et Quit (3)
        available_h = h - margin_y - 2 - 2 - 4 
        
        btn_w = (available_w // 2) - 2 # Espace entre les deux
        btn_h = max(3, available_h)    # Hauteur max

        # Centrage vertical
        start_row = 3
        
        # --- Bouton ROUGE ---
        self.buttons.append({
            "id": "RED",
            "label": "LED ROUGE\n" + ("ON" if self.red_on else "OFF"),
            "row": start_row,
            "col": margin_x,
            "height": btn_h,
            "width": btn_w,
            "color_idx": 6 if self.red_on else 5, # 6=On, 5=Off
            "active": False
        })

        # --- Bouton VERT ---
        self.buttons.append({
            "id": "GREEN",
            "label": "LED VERTE\n" + ("ON" if self.green_on else "OFF"),
            "row": start_row,
            "col": margin_x + btn_w + 2, # Décalé à droite
            "height": btn_h,
            "width": btn_w,
            "color_idx": 8 if self.green_on else 7, # 8=On, 7=Off
            "active": False
        })

        # --- Bouton QUIT (tout en bas, centré) ---
        quit_w = 20
        quit_col = (w - quit_w) // 2
        quit_row = h - 4
        
        self.buttons.append({
            "id": "QUIT",
            "label": "QUITTER",
            "row": quit_row,
            "col": quit_col,
            "height": 3,
            "width": quit_w,
            "color_idx": 9,
            "active": False
        })

    def _draw(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        
        # Bordure
        try:
            self.stdscr.attron(curses.color_pair(10) | curses.A_BOLD)
            self.stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
            self.stdscr.attroff(curses.color_pair(10) | curses.A_BOLD)
        except: pass

        # Titre
        title = " LilyGO Control Panel "
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        self.stdscr.addstr(0, max(2, (w - len(title)) // 2), title)
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

        # Status bar
        self.stdscr.attron(curses.color_pair(3))
        status_text = f" Status: {self.status_message}"
        if len(status_text) > w - 4: status_text = status_text[:w-4]
        self.stdscr.addstr(h - 2, 2, status_text)
        self.stdscr.attroff(curses.color_pair(3))

        # Reconstruire boutons (pour responsive)
        self._build_buttons(h, w)

        # Dessin des boutons
        for btn in self.buttons:
            attr = curses.color_pair(btn.get("color_idx", 1))
            if btn["active"]: # Effet click
                attr = attr | curses.A_REVERSE

            # Remplissage du bouton
            for r in range(btn["row"], btn["row"] + btn["height"]):
                if 0 <= r < h:
                    self.stdscr.attron(attr)
                    self.stdscr.addstr(r, btn["col"], " " * btn["width"])
                    self.stdscr.attroff(attr)

            # Label (multi-lignes supporté)
            lines = btn["label"].split('\n')
            total_lines = len(lines)
            start_y = btn["row"] + (btn["height"] - total_lines) // 2
            
            for i, line in enumerate(lines):
                lbl_y = start_y + i
                if 0 <= lbl_y < h:
                    lbl_x = btn["col"] + max(0, (btn["width"] - len(line)) // 2)
                    self.stdscr.attron(attr | curses.A_BOLD)
                    self.stdscr.addstr(lbl_y, lbl_x, line)
                    self.stdscr.attroff(attr | curses.A_BOLD)

        self.stdscr.refresh()

    def _touch_to_rowcol(self, x_raw, y_raw):
        if not self.touch_reader or not self.touch_reader.device:
            return 0, 0
            
        h, w = self.stdscr.getmaxyx()
        dx = max(1, self.touch_reader.max_x - self.touch_reader.min_x)
        dy = max(1, self.touch_reader.max_y - self.touch_reader.min_y)

        x_norm = (x_raw - self.touch_reader.min_x) / dx
        y_norm = (y_raw - self.touch_reader.min_y) / dy

        col = int(x_norm * (w - 1))
        row = int(y_norm * (h - 1))
        return row, col

    def _handle_touch_tap(self, x_raw, y_raw):
        # Anti-rebond (Debounce)
        now = time.time()
        if now - self.last_tap_time < 0.3: # Ignorer si moins de 300ms depuis le dernier tap validé
            return
        
        row, col = self._touch_to_rowcol(x_raw, y_raw)

        # Trouver le bouton cliqué
        clicked_btn = None
        for btn in self.buttons:
            if (btn["row"] <= row < btn["row"] + btn["height"] and
                    btn["col"] <= col < btn["col"] + btn["width"]):
                clicked_btn = btn
                break

        if not clicked_btn:
            # self.status_message = f"Click vide: {row},{col}"
            return
            
        # Mise à jour du temps du dernier tap valide seulement si on a cliqué sur un bouton
        self.last_tap_time = now

        # Action
        bid = clicked_btn["id"]
        
        if bid == "RED":
            self.red_on = not self.red_on
            cmd = "RED ON" if self.red_on else "RED OFF"
            self._send_cmd(cmd)
            self.status_message = f"Commande: {cmd}"
            
        elif bid == "GREEN":
            self.green_on = not self.green_on
            cmd = "GREEN ON" if self.green_on else "GREEN OFF"
            self._send_cmd(cmd)
            self.status_message = f"Commande: {cmd}"
            
        elif bid == "QUIT":
            self.running = False

    def run(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        self._init_colors()

        last_redraw = 0

        while self.running:
            now = time.time()
            if now - last_redraw > 0.1:  # 10 FPS suffisent
                self._draw()
                last_redraw = now

            # Clavier (Fallback pour test sans touch : r, v, q)
            try:
                ch = self.stdscr.getch()
            except curses.error:
                ch = -1

            if ch == ord('q'):
                self.running = False
            elif ch == ord('r'): # Touche 'r' pour simuler clic rouge
                self.red_on = not self.red_on
                self._send_cmd("RED ON" if self.red_on else "RED OFF")
            elif ch == ord('v') or ch == ord('g'): # Touche 'v' ou 'g' pour vert
                self.green_on = not self.green_on
                self._send_cmd("GREEN ON" if self.green_on else "GREEN OFF")

            # Touch events - Vider toute la file d'attente
            while not self.event_queue.empty():
                try:
                    event = self.event_queue.get_nowait()
                    kind, x_raw, y_raw = event
                    if kind == "tap":
                        self._handle_touch_tap(x_raw, y_raw)
                except Exception:
                    break

            time.sleep(0.01)

# ---------- ENTRY POINT ----------

def main(stdscr):
    event_queue = Queue()
    
    # Démarrer le thread touch (s'il trouve un device)
    try:
        touch_reader = TouchReader(event_queue)
        if touch_reader.device:
            touch_reader.start()
    except Exception as e:
        touch_reader = None # Pas de touch

    ui = CoolConsoleUI(stdscr, touch_reader, event_queue)
    ui.run()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"Erreur fatale: {e}")
