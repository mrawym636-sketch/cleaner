"""
🛡️ CyberClean Pro v4.6 – Version Simplifiée
Nettoyeur de fichiers vides + Antivirus léger
Design: Dracula/Cyberpunk | Interface: Tkinter
Fonctionnalités: Scan, Suppression, Rapport, Copie, Son, Raccourcis
"""

import os
import sys
import json
import threading
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# ============================================================
# Gestion du son (multi-plateforme)
# ============================================================
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# ============================================================
# Gestion du chemin du script
# ============================================================
def get_script_dir():
    try:
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            if '__file__' in globals():
                return os.path.dirname(os.path.abspath(__file__))
            else:
                return os.path.dirname(os.path.abspath(sys.argv[0]))
    except:
        return os.getcwd()

# ============================================================
# CLASSE PRINCIPALE
# ============================================================
class CyberCleanPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ CyberClean Pro v4.6")
        self.root.geometry("920x760")
        self.root.minsize(820, 680)
        
        # ============ THEME ============
        self.theme = {
            "bg": "#0A0A14",
            "card": "#141428",
            "card_border": "#2A2A4A",
            "surface": "#0E0E1E",
            "text": "#E8E8F0",
            "text_gray": "#8888AA",
            "text_dark": "#111122",
            "blue": "#6C8CFF",
            "blue_hover": "#8AA8FF",
            "green": "#6CCF8C",
            "green_hover": "#8ADFAA",
            "red": "#FF6B8A",
            "red_hover": "#FF8AA6",
            "orange": "#FFB86C",
            "purple": "#CBA6F7",
            "btn_bg": "#2A2A4A",
            "hover": "#3A3A5E",
            "logo_bg": "#0A0A14",
            "logo_text": "#6C8CFF",
            "logo_accent": "#FFB86C"
        }
        self.root.configure(bg=self.theme["bg"])
        self.root.bind("<Escape>", lambda e: self.cancel_scan())
        self.root.bind("<Control-c>", lambda e: self.copy_report())
        self.root.bind("<Control-d>", lambda e: self.clear())
        self.root.bind("<F1>", lambda e: self.show_help())

        # ============ VARIABLES ============
        settings = self.load_settings()
        self.scan_path = tk.StringVar(value=settings.get("last_path", os.path.expanduser("~/Desktop")))
        self.sound_enabled = settings.get("sound_enabled", True)
        self.scanning = False
        self.cancel_scan_flag = False
        self.total = 0
        self.empty = []
        self.suspects = []
        self.deleted = []
        self.failed = []
        self.report_path = ""
        self.script_dir = get_script_dir()

        # Extensions suspectes
        self.suspect_exts = {
            '.exe', '.bat', '.cmd', '.vbs', '.js', '.ps1', '.scr',
            '.com', '.pif', '.jar', '.msi', '.dll', '.sys', '.reg',
            '.sh', '.py', '.rb', '.pl', '.php', '.jsp', '.asp',
            '.app', '.deb', '.rpm', '.apk', '.xapk'
        }

        # ============ STYLE ============
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar",
                            troughcolor=self.theme["card"],
                            background=self.theme["blue"],
                            thickness=16,
                            borderwidth=0)
        self.style.configure("TFrame", background=self.theme["bg"])

        # ============ UI ============
        self.create_ui()
        self.play_sound("startup")

    # ============================================================
    # SONS
    # ============================================================
    def play_sound(self, sound_type):
        if not self.sound_enabled or not SOUND_AVAILABLE:
            return
        try:
            sounds = {
                "click": (800, 50),
                "success": (1200, 100),
                "error": (400, 200),
                "scan_done": (1000, 150),
                "startup": (600, 80),
                "delete": (500, 100)
            }
            if sound_type in sounds:
                freq, dur = sounds[sound_type]
                winsound.Beep(freq, dur)
                if sound_type == "success":
                    winsound.Beep(1500, 100)
                elif sound_type == "error":
                    winsound.Beep(300, 200)
                elif sound_type == "scan_done":
                    winsound.Beep(1200, 150)
                    winsound.Beep(1500, 150)
                elif sound_type == "startup":
                    winsound.Beep(800, 80)
                    winsound.Beep(1000, 80)
                elif sound_type == "delete":
                    winsound.Beep(300, 100)
        except:
            pass

    # ============================================================
    # PARAMÈTRES
    # ============================================================
    def load_settings(self):
        try:
            path = os.path.join(self.script_dir, "cyberclean_settings.json")
            with open(path, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_settings(self):
        try:
            settings = {
                "last_path": self.scan_path.get(),
                "sound_enabled": self.sound_enabled
            }
            path = os.path.join(self.script_dir, "cyberclean_settings.json")
            with open(path, "w") as f:
                json.dump(settings, f, indent=4)
        except:
            pass

    # ============================================================
    # INTERFACE
    # ============================================================
    def create_ui(self):
        main = tk.Frame(self.root, bg=self.theme["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # ========== LOGO ==========
        logo_frame = tk.Frame(main, bg=self.theme["logo_bg"])
        logo_frame.pack(fill=tk.X, pady=(0, 12))
        
        logo_text = """
   ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗██╗     ███████╗ █████╗ ███╗   ██╗
  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║
  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║     █████╗  ███████║██╔██╗ ██║
  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║
  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╗███████╗███████╗██║  ██║██║ ╚████║
   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
        """
        
        logo_display = tk.Label(logo_frame, text=logo_text, 
                               font=("Consolas", 9, "bold"),
                               bg=self.theme["logo_bg"],
                               fg=self.theme["logo_text"],
                               justify=tk.CENTER)
        logo_display.pack(pady=(5, 0))
        
        tagline = tk.Label(logo_frame, text="⚡ Nettoyeur · Antivirus · Optimiseur ⚡",
                          font=("Segoe UI", 11, "italic"),
                          bg=self.theme["logo_bg"],
                          fg=self.theme["logo_accent"])
        tagline.pack(pady=(2, 8))

        # ========== DOSSIER ==========
        card = tk.Frame(main, bg=self.theme["card"], 
                       highlightthickness=1, 
                       highlightbackground=self.theme["card_border"])
        card.pack(fill=tk.X, pady=(0, 14), ipady=12, ipadx=14)
        
        path_frame = tk.Frame(card, bg=self.theme["card"])
        path_frame.pack(fill=tk.X, pady=(4,0))
        
        tk.Label(path_frame, text="📂 Dossier cible", 
                font=("Segoe UI", 11, "bold"), 
                bg=self.theme["card"], 
                fg=self.theme["text"]).pack(side=tk.LEFT, padx=(10,8))
        
        entry = tk.Entry(path_frame, textvariable=self.scan_path, 
                        font=("Consolas", 10), 
                        bg=self.theme["bg"], 
                        fg=self.theme["text"],
                        insertbackground=self.theme["text"], 
                        relief=tk.FLAT, 
                        bd=8)
        entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)
        
        tk.Button(path_frame, text="📂 Parcourir", 
                 font=("Segoe UI", 10, "bold"),
                 bg=self.theme["btn_bg"], 
                 fg=self.theme["text"], 
                 relief=tk.FLAT, 
                 padx=18, pady=5,
                 activebackground=self.theme["hover"],
                 command=self.browse,
                 cursor="hand2").pack(side=tk.RIGHT, padx=(0,8))

        # ========== BOUTONS ==========
        actions = tk.Frame(main, bg=self.theme["bg"])
        actions.pack(fill=tk.X, pady=(0, 12))
        
        left = tk.Frame(actions, bg=self.theme["bg"])
        left.pack(side=tk.LEFT)
        
        self.scan_btn = tk.Button(left, text="🔍 Scanner", 
                                 font=("Segoe UI", 13, "bold"),
                                 bg=self.theme["blue"], 
                                 fg=self.theme["text_dark"], 
                                 relief=tk.FLAT, 
                                 padx=35, pady=11,
                                 activebackground=self.theme["blue_hover"],
                                 command=self.start_scan,
                                 cursor="hand2")
        self.scan_btn.pack(side=tk.LEFT, padx=(0,10))
        
        self.cancel_btn = tk.Button(left, text="⏹️ Annuler", 
                                   font=("Segoe UI", 12, "bold"),
                                   bg=self.theme["orange"], 
                                   fg=self.theme["text_dark"], 
                                   relief=tk.FLAT, 
                                   padx=25, pady=11,
                                   activebackground="#FFD08C",
                                   state=tk.DISABLED,
                                   command=self.cancel_scan,
                                   cursor="hand2")
        self.cancel_btn.pack(side=tk.LEFT, padx=(0,10))
        
        self.del_btn = tk.Button(left, text="🗑️ Supprimer les vides", 
                                font=("Segoe UI", 13, "bold"),
                                bg=self.theme["red"], 
                                fg=self.theme["text_dark"], 
                                relief=tk.FLAT, 
                                padx=35, pady=11,
                                activebackground=self.theme["red_hover"],
                                state=tk.DISABLED, 
                                command=self.delete_empty,
                                cursor="hand2")
        self.del_btn.pack(side=tk.LEFT)
        
        right = tk.Frame(actions, bg=self.theme["bg"])
        right.pack(side=tk.RIGHT)
        
        for text, color, cmd in [
            ("📋 Copier", self.theme["btn_bg"], self.copy_report),
            ("📂 Rapport", self.theme["purple"], self.open_report),
            ("🔊 Son", self.theme["btn_bg"], self.toggle_sound),
            ("🧹 Effacer", self.theme["btn_bg"], self.clear)
        ]:
            btn = tk.Button(right, text=text, font=("Segoe UI", 10),
                           bg=color, fg=self.theme["text_dark"] if color == self.theme["purple"] else self.theme["text"],
                           relief=tk.FLAT, padx=14, pady=8,
                           command=cmd, cursor="hand2")
            btn.pack(side=tk.RIGHT, padx=4)
            if text == "🔊 Son":
                self.sound_btn = btn

        # ========== PROGRESSION ==========
        prog_frame = tk.Frame(main, bg=self.theme["bg"])
        prog_frame.pack(fill=tk.X, pady=(0, 6))
        
        self.progress = ttk.Progressbar(prog_frame, style="TProgressbar", mode='determinate')
        self.progress.pack(fill=tk.X)
        
        status_frame = tk.Frame(prog_frame, bg=self.theme["bg"])
        status_frame.pack(fill=tk.X, pady=(6,0))
        
        self.status = tk.Label(status_frame, text="● Prêt à analyser", 
                              font=("Segoe UI", 10),
                              bg=self.theme["bg"], 
                              fg=self.theme["text_gray"], 
                              anchor="w")
        self.status.pack(side=tk.LEFT)
        
        self.report_indicator = tk.Label(status_frame, text="", 
                                         font=("Segoe UI", 9, "italic"),
                                         bg=self.theme["bg"],
                                         fg=self.theme["green"])
        self.report_indicator.pack(side=tk.RIGHT)

        # ========== RAPPORT ==========
        report_header = tk.Frame(main, bg=self.theme["bg"])
        report_header.pack(fill=tk.X, pady=(12, 6))
        
        tk.Label(report_header, text="📊 RAPPORT D'ANALYSE", 
                font=("Segoe UI", 13, "bold"),
                bg=self.theme["bg"], 
                fg=self.theme["text"]).pack(side=tk.LEFT)
        
        self.counter = tk.Label(report_header, text="", 
                               font=("Segoe UI", 10),
                               bg=self.theme["bg"], 
                               fg=self.theme["text_gray"])
        self.counter.pack(side=tk.RIGHT)
        
        self.log_area = scrolledtext.ScrolledText(main, 
                                                 font=("Consolas", 10),
                                                 bg=self.theme["surface"], 
                                                 fg=self.theme["text"],
                                                 insertbackground=self.theme["text"], 
                                                 wrap=tk.WORD,
                                                 state=tk.DISABLED, 
                                                 relief=tk.FLAT, 
                                                 bd=10)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Tags de couleur
        self.log_area.tag_config("info", foreground=self.theme["blue"])
        self.log_area.tag_config("danger", foreground=self.theme["red"])
        self.log_area.tag_config("success", foreground=self.theme["green"])
        self.log_area.tag_config("warning", foreground=self.theme["orange"])
        self.log_area.tag_config("gray", foreground=self.theme["text_gray"])

        # ========== STATS ==========
        bottom = tk.Frame(main, bg=self.theme["bg"])
        bottom.pack(fill=tk.X, pady=(4,0))
        
        self.stats = tk.Label(bottom, 
            text="📁 0 analysés  │  🗑️ 0 vides  │  ⚠️ 0 suspects  │  ✅ 0 supprimés",
            font=("Segoe UI", 10, "bold"), 
            bg=self.theme["bg"], 
            fg=self.theme["text_gray"])
        self.stats.pack(side=tk.LEFT)
        
        shortcuts = tk.Label(bottom, 
            text="[Esc] Annuler  [Ctrl+C] Copier  [Ctrl+D] Effacer  [F1] Aide",
            font=("Segoe UI", 8, "italic"),
            bg=self.theme["bg"],
            fg=self.theme["text_gray"])
        shortcuts.pack(side=tk.RIGHT)

        self.update_sound_button()

    def update_sound_button(self):
        if hasattr(self, 'sound_btn'):
            self.sound_btn.config(text="🔊 Son" if self.sound_enabled else "🔇 Son")

    # ============================================================
    # FONCTIONS
    # ============================================================
    def browse(self):
        folder = filedialog.askdirectory(title="Choisir un dossier à analyser")
        if folder:
            self.scan_path.set(folder)
            self.play_sound("click")
            self.save_settings()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.save_settings()
        self.update_sound_button()
        if self.sound_enabled:
            self.play_sound("click")
            self.status.config(text="● Son activé", fg=self.theme["green"])
        else:
            self.status.config(text="● Son désactivé", fg=self.theme["text_gray"])

    def show_help(self):
        help_text = """
🛡️ CYBERCLEAN PRO v4.6 - AIDE

📌 RACCOURCIS CLAVIER :
   [Esc]     → Annuler le scan
   [Ctrl+C]  → Copier le rapport
   [Ctrl+D]  → Effacer les résultats
   [F1]      → Afficher cette aide

📌 FONCTIONS :
   🔍 Scanner      → Analyse tous les fichiers du dossier
   ⏹️ Annuler      → Arrête le scan en cours
   🗑️ Supprimer   → Supprime les fichiers vides
   📋 Copier      → Copie le rapport dans le presse-papiers
   📂 Rapport     → Ouvre le fichier rapport (.txt)
   🔊 Son         → Active/Désactive les sons
   🧹 Effacer     → Vide les résultats

📌 EXTENSIONS SUSPECTES :
   .exe, .bat, .cmd, .vbs, .js, .ps1, .scr,
   .com, .pif, .jar, .msi, .dll, .sys, .reg,
   .sh, .py, .rb, .pl, .php, .jsp, .asp,
   .app, .deb, .rpm, .apk, .xapk

📌 RAPPORT :
   Généré automatiquement dans le dossier du script.
   Nom: CyberClean_Report_JJ-MM-AAAA_HH-MM-SS.txt
"""
        messagebox.showinfo("🛡️ Aide - CyberClean Pro", help_text)

    def log(self, text, tag=None):
        self.log_area.config(state=tk.NORMAL)
        if tag:
            self.log_area.insert(tk.END, text, tag)
        else:
            self.log_area.insert(tk.END, text)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def update_stats(self):
        self.stats.config(
            text=f"📁 {self.total} analysés  │  🗑️ {len(self.empty)} vides  │  "
                 f"⚠️ {len(self.suspects)} suspects  │  ✅ {len(self.deleted)} supprimés"
        )
        self.counter.config(text=f"🗑️ Vides: {len(self.empty)}  │  ⚠️ Suspects: {len(self.suspects)}")

    def clear(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)
        self.total = 0
        self.empty = []
        self.suspects = []
        self.deleted = []
        self.failed = []
        self.report_path = ""
        self.report_indicator.config(text="")
        self.update_stats()
        self.del_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status.config(text="● Prêt à analyser", fg=self.theme["text_gray"])
        self.play_sound("click")

    def copy_report(self):
        content = self.log_area.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()
            self.play_sound("click")
            messagebox.showinfo("✅ Copié", "Le rapport a été copié dans le presse-papiers !")
        else:
            messagebox.showwarning("⚠️ Attention", "Aucun rapport à copier.")

    def open_report(self):
        if self.report_path and os.path.exists(self.report_path):
            os.startfile(self.report_path)
            self.play_sound("click")
        else:
            messagebox.showwarning("⚠️ Attention", "Aucun rapport disponible. Lancez d'abord un scan.")

    def format_size(self, size):
        for unit in ['o', 'Ko', 'Mo', 'Go']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} To"

    def cancel_scan(self):
        if self.scanning:
            self.cancel_scan_flag = True
            self.status.config(text="⏹️ Annulation en cours...", fg=self.theme["orange"])
            self.play_sound("error")

    # ============================================================
    # SAUVEGARDE RAPPORT
    # ============================================================
    def save_report(self):
        try:
            now = datetime.now()
            filename = f"CyberClean_Report_{now.strftime('%d-%m-%Y_%H-%M-%S')}.txt"
            self.report_path = os.path.join(self.script_dir, filename)
            
            content = self.log_area.get(1.0, tk.END).strip()
            if not content:
                return
            
            header = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                       🛡️ CYBERCLEAN PRO                             ║
║                    RAPPORT D'ANALYSE AUTOMATIQUE                     ║
╚═══════════════════════════════════════════════════════════════════════╝

📅 Date: {now.strftime('%d/%m/%Y à %H:%M:%S')}
📁 Dossier analysé: {self.scan_path.get()}
📊 Total fichiers: {self.total}
🗑️ Fichiers vides: {len(self.empty)}
⚠️ Fichiers suspects: {len(self.suspects)}
✅ Fichiers supprimés: {len(self.deleted)}

{"═"*75}

{content}

{"═"*75}

🔒 Rapport généré automatiquement par CyberClean Pro v4.6
"""
            
            with open(self.report_path, 'w', encoding='utf-8') as f:
                f.write(header)
            
            self.report_indicator.config(text=f"✅ Rapport: {filename}", fg=self.theme["green"])
            self.play_sound("success")
            
        except Exception as e:
            self.report_indicator.config(text=f"❌ Erreur: {e}", fg=self.theme["red"])
            self.play_sound("error")

    # ============================================================
    # SCAN
    # ============================================================
    def start_scan(self):
        if self.scanning:
            return
        path = self.scan_path.get()
        if not os.path.exists(path):
            messagebox.showerror("❌ Erreur", "Le dossier sélectionné n'existe pas !")
            return

        self.clear()
        self.scanning = True
        self.cancel_scan_flag = False
        self.scan_btn.config(state=tk.DISABLED, text="⏳ Scan en cours...")
        self.cancel_btn.config(state=tk.NORMAL)
        self.status.config(text="🔍 Analyse en cours...", fg=self.theme["blue"])
        self.report_indicator.config(text="⏳ Scan en cours...", fg=self.theme["orange"])

        thread = threading.Thread(target=self.scan, args=(path,), daemon=True)
        thread.start()

    def scan(self, path):
        files = []
        for root, dirs, names in os.walk(path, followlinks=False):
            # Ignorer les dossiers cachés
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for name in names:
                files.append(os.path.join(root, name))

        self.total = len(files)

        for i, fp in enumerate(files):
            if self.cancel_scan_flag:
                break
            try:
                size = os.path.getsize(fp)
                prog = int(((i + 1) / self.total) * 100) if self.total > 0 else 0
                self.root.after(0, self.update_prog, prog)
                self.root.after(0, self.update_status, f"Scan: {i+1}/{self.total}")

                if size == 0:
                    self.empty.append(fp)
                    self.root.after(0, self.add_result, "🗑️", fp, "0 o")

                _, ext = os.path.splitext(fp)
                if ext.lower() in self.suspect_exts and size > 0:
                    self.suspects.append(fp)
                    self.root.after(0, self.add_result, "⚠️", fp, self.format_size(size))

            except:
                pass

        self.root.after(0, self.scan_done)

    def update_prog(self, val):
        self.progress['value'] = val

    def update_status(self, text):
        self.status.config(text=f"● {text}")

    def add_result(self, icon, path, size):
        self.log_area.config(state=tk.NORMAL)
        if icon == "🗑️":
            self.log_area.insert(tk.END, f"{icon} {path} ({size})\n", "danger")
        elif icon == "⚠️":
            self.log_area.insert(tk.END, f"{icon} {path} ({size})\n", "warning")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        self.update_stats()

    def scan_done(self):
        self.scanning = False
        self.cancel_btn.config(state=tk.DISABLED)
        
        if self.cancel_scan_flag:
            self.scan_btn.config(state=tk.NORMAL, text="🔍 Scanner")
            self.progress['value'] = 0
            self.status.config(text="⏹️ Scan annulé", fg=self.theme["orange"])
            self.report_indicator.config(text="⏹️ Annulé", fg=self.theme["orange"])
            self.cancel_scan_flag = False
            self.play_sound("error")
            return

        self.scan_btn.config(state=tk.NORMAL, text="🔍 Scanner")
        self.progress['value'] = 100
        self.status.config(text="✅ Scan terminé avec succès !", fg=self.theme["green"])
        self.play_sound("scan_done")

        self.log("\n" + "═"*75 + "\n", "gray")
        self.log("🛡️ RAPPORT D'ANALYSE COMPLET\n", "info")
        self.log(f"📁 Dossier : {self.scan_path.get()}\n", "gray")
        self.log(f"📅 Date : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n", "gray")
        self.log("═"*75 + "\n\n", "gray")

        if self.empty:
            self.log(f"🗑️ FICHIERS VIDES ({len(self.empty)}) :\n", "danger")
            for f in self.empty[:25]:
                self.log(f"  • {f}\n", "gray")
            if len(self.empty) > 25:
                self.log(f"  ... et {len(self.empty)-25} autre(s)\n", "gray")
            self.log("\n")
            self.del_btn.config(state=tk.NORMAL)
        else:
            self.log("✅ Aucun fichier vide détecté.\n\n", "success")

        if self.suspects:
            self.log(f"⚠️ FICHIERS SUSPECTS ({len(self.suspects)}) :\n", "warning")
            for f in self.suspects[:25]:
                try:
                    sz = self.format_size(os.path.getsize(f))
                except:
                    sz = "?"
                self.log(f"  • {f} ({sz})\n", "gray")
            if len(self.suspects) > 25:
                self.log(f"  ... et {len(self.suspects)-25} autre(s)\n", "gray")
            self.log("\n")
        else:
            self.log("✅ Aucun fichier suspect détecté.\n\n", "success")

        self.log("═"*75 + "\n", "gray")
        self.log(f"📊 RÉSUMÉ : {self.total} fichiers analysés\n", "info")
        self.log(f"   🗑️ Vides : {len(self.empty)}\n", "danger")
        self.log(f"   ⚠️ Suspects : {len(self.suspects)}\n", "warning")
        self.log("═"*75 + "\n", "gray")

        self.update_stats()
        self.save_settings()
        self.save_report()

    # ============================================================
    # SUPPRESSION
    # ============================================================
    def delete_empty(self):
        if not self.empty:
            messagebox.showinfo("ℹ️ Information", "Aucun fichier vide à supprimer.")
            return

        confirm = messagebox.askyesno(
            "⚠️ Confirmation de suppression",
            f"🗑️ Supprimer définitivement {len(self.empty)} fichier(s) vide(s) ?\n\n"
            "⚠️ Cette action est IRREVERSIBLE !",
            icon='warning'
        )
        if not confirm:
            return

        self.deleted = []
        self.failed = []

        for f in self.empty:
            try:
                if not os.path.exists(f):
                    self.failed.append((f, "Fichier introuvable"))
                    continue
                if not os.access(f, os.W_OK):
                    self.failed.append((f, "Permission refusée"))
                    continue
                os.remove(f)
                self.deleted.append(f)
                self.play_sound("delete")
            except PermissionError:
                self.failed.append((f, "Permission refusée (admin requis)"))
            except OSError as e:
                self.failed.append((f, f"OS: {e}"))
            except Exception as e:
                self.failed.append((f, f"Erreur: {e}"))

        self.empty = [f for f in self.empty if f not in self.deleted]

        self.log("\n" + "─"*75 + "\n", "gray")
        self.log("🗑️ RÉSULTAT DE LA SUPPRESSION :\n", "info")
        self.log(f"✅ Supprimés : {len(self.deleted)}\n", "success")
        if self.failed:
            self.log(f"❌ Échecs : {len(self.failed)}\n", "danger")
            for f, err in self.failed[:10]:
                self.log(f"  • {f} → {err}\n", "gray")

        self.update_stats()

        if not self.empty:
            self.del_btn.config(state=tk.DISABLED)
            self.status.config(text="✅ Nettoyage terminé !", fg=self.theme["green"])
            self.play_sound("success")
            messagebox.showinfo("✅ Succès", f"{len(self.deleted)} fichier(s) supprimé(s) !")
        else:
            self.status.config(text=f"⚠️ {len(self.empty)} restant(s)", fg=self.theme["red"])
            if self.failed:
                self.play_sound("error")
                messagebox.showwarning(
                    "⚠️ Suppression partielle",
                    f"✅ {len(self.deleted)} supprimés\n"
                    f"❌ {len(self.failed)} échecs\n\n"
                    "▶️ Exécutez en Administrateur\n"
                    "▶️ Fermez les fichiers ouverts"
                )
        
        self.save_report()

# ============================================================
# LANCEMENT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CyberCleanPro(root)
    root.mainloop()