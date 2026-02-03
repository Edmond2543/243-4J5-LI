import threading
import time
import os
from queue import Queue

import curses
from evdev import InputDevice, ecodes, list_devices


# ---------- GESTION DU TOUCH ----------

class TouchReader(threading.Thread):
    def __init__(self, event_queue: Queue):
        super().__init__(daemon=True)
        self.event_queue = event_queue
        self.device = self._find_touch_device()
        if not self.device:
            raise RuntimeError("Aucun périphérique touchscreen trouvé.")

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
        for path in list_devices():
            dev = InputDevice(path)
            name = dev.name.lower()
            if "touch" in name or "ft5406" in name:
                print(f"[TouchReader] Using device: {dev.name} ({path})")
                return dev
        return None

    def run(self):
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
    def __init__(self, stdscr, touch_reader: TouchReader, event_queue: Queue):
        self.stdscr = stdscr
        self.touch_reader = touch_reader
        self.event_queue = event_queue
        self.running = True
        self.status_message = "Prêt."

        self.buttons = []  # rempli à chaque redraw en fonction de la taille écran

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # STATUS
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Active
        curses.init_pair(3, curses.COLOR_CYAN, -1)                   # Status Text
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)   # Title
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)    # REBOOT
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW) # LOGS
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_MAGENTA)# QUIT
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Border

    def _build_buttons(self, h, w):
        """
        Construit 4 gros boutons centrés verticalement.
        """
        self.buttons = []
        btn_width = max(20, w - 6)
        btn_height = 3

        # positions verticales : 4 boutons * (3 haut + 1 espace) = 16 lignes
        start_row = (h - 16) // 2
        if start_row < 3:
            start_row = 3

        labels = ["STATUS", "LOGS", "REBOOT", "QUIT"]
        for i, label in enumerate(labels):
            row = start_row + i * (btn_height + 1)
            col = (w - btn_width) // 2
            
            # Couleur unique par bouton
            color_idx = 1
            if label == "STATUS":
                color_idx = 1
            elif label == "LOGS":
                color_idx = 6
            elif label == "REBOOT":
                color_idx = 5
            elif label == "QUIT":
                color_idx = 7

            self.buttons.append({
                "label": label,
                "row": row,
                "col": col,
                "height": btn_height,
                "width": btn_width,
                "active": False,
                "color_idx": color_idx
            })

    def _draw(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        
        # Bordure écran stylisée
        try:
            self.stdscr.attron(curses.color_pair(8) | curses.A_BOLD)
            # Utilisation de caractères ASCII pour éviter les glitchs d'encodage (lettres q, x...)
            self.stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
            self.stdscr.attroff(curses.color_pair(8) | curses.A_BOLD)
        except:
            pass

        # Titre
        title = " RPi Touch Interface v2.0 "
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        self.stdscr.addstr(0, max(2, (w - len(title)) // 2), title)
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

        # Status bar
        self.stdscr.attron(curses.color_pair(3))
        status_text = f" Status: {self.status_message}"
        # Tronquer pour éviter crash
        if len(status_text) > w - 4:
            status_text = status_text[:w-4]
        self.stdscr.addstr(h - 2, 2, status_text)
        self.stdscr.attroff(curses.color_pair(3))

        # Construire les boutons selon la taille écran
        self._build_buttons(h, w)

        # Dessin des boutons
        for btn in self.buttons:
            if btn["active"]:
                attr = curses.color_pair(2) | curses.A_BOLD
            else:
                attr = curses.color_pair(btn.get("color_idx", 1))

            for r in range(btn["row"], btn["row"] + btn["height"]):
                if 0 <= r < h:
                    self.stdscr.attron(attr)
                    self.stdscr.addstr(r, btn["col"], " " * btn["width"])
                    self.stdscr.attroff(attr)

            # Label centré
            label = f"[ {btn['label']} ]"
            label_col = btn["col"] + max(0, (btn["width"] - len(label)) // 2)
            label_row = btn["row"] + btn["height"] // 2
            if 0 <= label_row < h:
                self.stdscr.attron(attr | curses.A_BOLD)
                self.stdscr.addstr(label_row, label_col, label)
                self.stdscr.attroff(attr | curses.A_BOLD)

        self.stdscr.refresh()

    def _touch_to_rowcol(self, x_raw, y_raw):
        """
        Map coordonnées brutes evdev -> lignes/colonnes du terminal curses.
        """
        h, w = self.stdscr.getmaxyx()

        # protection division par zéro
        dx = max(1, self.touch_reader.max_x - self.touch_reader.min_x)
        dy = max(1, self.touch_reader.max_y - self.touch_reader.min_y)

        x_norm = (x_raw - self.touch_reader.min_x) / dx
        y_norm = (y_raw - self.touch_reader.min_y) / dy

        col = int(x_norm * (w - 1))
        row = int(y_norm * (h - 1))

        # clamp
        row = max(0, min(h - 1, row))
        col = max(0, min(w - 1, col))
        return row, col

    def _handle_touch_tap(self, x_raw, y_raw):
        row, col = self._touch_to_rowcol(x_raw, y_raw)

        # Vérifier sur quel bouton on a tapé
        clicked_btn = None
        for btn in self.buttons:
            if (btn["row"] <= row < btn["row"] + btn["height"] and
                    btn["col"] <= col < btn["col"] + btn["width"]):
                clicked_btn = btn
                break

        # Réinitialiser les états
        for btn in self.buttons:
            btn["active"] = False

        if not clicked_btn:
            self.status_message = f"Touched at row={row}, col={col} (no button)."
            return

        clicked_btn["active"] = True
        label = clicked_btn["label"]

        if label == "STATUS":
            self.status_message = f"STATUS: Tout roule. Touch={row},{col}"
        elif label == "LOGS":
            self.status_message = "LOGS: (ici tu pourrais afficher des logs système, etc.)"
        elif label == "REBOOT":
            self.status_message = "REBOOT demandé... (simulation)"
            # os.system("sudo reboot")
        elif label == "QUIT":
            self.status_message = "Quit demandé..."
            self.running = False

    def run(self):
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        self._init_colors()

        last_redraw = 0

        while self.running:
            now = time.time()
            if now - last_redraw > 0.05:  # ~20 FPS
                self._draw()
                last_redraw = now

            # Lecture touches clavier (genre pour debug / sortir)
            try:
                ch = self.stdscr.getch()
            except curses.error:
                ch = -1

            if ch == ord('q'):
                self.status_message = "Quit avec 'q'."
                self.running = False

            # Gestion des événements tactiles
            try:
                event = self.event_queue.get_nowait()
            except Exception:
                event = None

            if event:
                kind, x_raw, y_raw = event
                if kind == "tap":
                    self._handle_touch_tap(x_raw, y_raw)

            time.sleep(0.01)


# ---------- ENTRY POINT ----------

def main(stdscr):
    event_queue = Queue()
    touch_reader = TouchReader(event_queue)
    touch_reader.start()

    ui = CoolConsoleUI(stdscr, touch_reader, event_queue)
    ui.run()


if __name__ == "__main__":
    curses.wrapper(main)
