import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from pynput.mouse import Controller, Button
from pynput import keyboard, mouse as pynput_mouse
import threading
import time
import random
import logging
import os
import sys
import ctypes
from PIL import ImageGrab, Image, ImageDraw
import math
import statistics

def get_active_window_title():
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value
    except Exception:
        return ""

class PhotonPulseAutoClicker18D2:
    def __init__(self, root):
        self.root = root
        self.root.title("Photon Pulse Auto Clicer18D2")
        self.root.geometry("1000x800")
        self.mouse = Controller()
        self.clicking = False
        self.stop_event = threading.Event()
        self.cps_var = tk.StringVar(value="10")
        self.duration_var = tk.StringVar(value="0")
        self.start_key_var = tk.StringVar(value="f6")
        self.stop_key_var = tk.StringVar(value="f7")
        self.mode_var = tk.StringVar(value="Constant")
        self.human_like_var = tk.BooleanVar(value=True)
        self.heatup_var = tk.BooleanVar(value=True)
        self.theme_var = tk.StringVar(value="Light")
        self.stealth_key_var = tk.StringVar(value="esc")
        self.overlay_var = tk.BooleanVar(value=False)
        self.overlay_x = tk.IntVar(value=100)
        self.overlay_y = tk.IntVar(value=100)
        self.macros = []
        self.macro_stop_key_var = tk.StringVar(value="f8")
        self.macro_stop_event = threading.Event()
        self.mods = []
        self.mod_vars = {}
        self.active_mods = {}
        self.game_autodetect_var = tk.BooleanVar(value=False)
        self.target_x_var = tk.IntVar(value=0)
        self.target_y_var = tk.IntVar(value=0)
        self.position_picker_active = False
        self.target_finder_var = tk.BooleanVar(value=False)
        self.target_color = None
        self.tolerance_var = tk.IntVar(value=30)
        self.pattern_intervals = []
        self.recording_pattern = False
        self.pattern_last_time = None
        self.ghost_mode_var = tk.BooleanVar(value=False)
        self.log_file = os.path.join(os.path.dirname(__file__), "photon_pulse_autoclicker18d2_log.txt")
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format="%(Y-%m-%d %H:%M:%S - %(message)s)", datefmt="%Y-%m-%d %H:%M:%S")
        self.run_stats = []
        # Language selection
        self.languages = {
            "Türkçe": "tr",
            "English": "en",
            "Deutsch": "de",
            "日本語": "ja",
            "Русский": "ru",
            "中文": "zh"
        }
        self.language_var = tk.StringVar(value="English")
        # Translations for UI text keys
        self.translations = {
            "en": {
                "Clicker": "Clicker",
                "CPS Test": "CPS Test",
                "Pattern": "Pattern",
                "Logs/Stats": "Logs/Stats",
                "Download Mods": "Download Mods",
                "Macro": "Macro",
                "Overlay": "Overlay",
                "Admin Panel": "Admin Panel",
                "Settings": "Settings",
                "Language": "Language",
                "Apply": "Apply",
                # Labels
                "Target CPS:": "Target CPS:",
                "Duration (sec, 0=infinite):": "Duration (sec, 0=infinite):",
                "Start Key:": "Start Key:",
                "Stop Key:": "Stop Key:",
                "Mode:": "Mode:",
                "Human-like Behavior": "Human-like Behavior",
                "Enable Heat-up Ramp": "Enable Heat-up Ramp",
                "Game Auto Detect": "Game Auto Detect",
                "Ghost Mode (Anti-Detect)": "Ghost Mode (Anti-Detect)",
                "Target Finder": "Target Finder",
                "Pick Target Color": "Pick Target Color",
                "Tolerance:": "Tolerance:",
                "Pick Click Position": "Pick Click Position",
                "X:": "X:",
                "Y:": "Y:",
                "Theme:": "Theme:",
                "Stealth Key:": "Stealth Key:",
                "Macro Stop Key:": "Macro Stop Key:",
                "Status: Idle": "Status: Idle",
                "Status: Clicking...": "Status: Clicking...",
                "Status: Stopped": "Status: Stopped",
                "Status: Done": "Status: Done",
                "Click inside to test your CPS": "Click inside to test your CPS",
                "Test Duration (sec):": "Test Duration (sec):",
                "Start CPS Test": "Start CPS Test",
                "CPS: N/A": "CPS: N/A",
                "Start Recording Pattern": "Start Recording Pattern",
                "Stop Recording Pattern": "Stop Recording Pattern",
                "Clear Pattern": "Clear Pattern",
                "Pattern: None": "Pattern: None",
                "Log:": "Log:",
                "Run CPS Stats:": "Run CPS Stats:",
                "Live CPS Overlay": "Live CPS Overlay",
                "Overlay Position X,Y:": "Overlay Position X,Y:",
                "Admin Panel": "Admin Panel",
                "New Macro": "New Macro",
                "Delete": "Delete",
                "Edit": "Edit",
                "Apply Mods": "Apply Mods",
                # etc.
            },
            "tr": {
                "Clicker": "Tıklayıcı",
                "CPS Test": "CPS Testi",
                "Pattern": "Desen",
                "Logs/Stats": "Kayıtlar/İstatistik",
                "Download Mods": "Mod İndir",
                "Macro": "Makro",
                "Overlay": "Kaplama",
                "Admin Panel": "Yönetici Paneli",
                "Settings": "Ayarlar",
                "Language": "Dil",
                "Apply": "Uygula",
                "Target CPS:": "Hedef CPS:",
                "Duration (sec, 0=infinite):": "Süre (sn, 0=sonsuz):",
                "Start Key:": "Başlat Tuşu:",
                "Stop Key:": "Durdur Tuşu:",
                "Mode:": "Mod:",
                "Human-like Behavior": "İnsan Gibi Davran",
                "Enable Heat-up Ramp": "Isınma Artışı Etkin",
                "Game Auto Detect": "Oyunu Otomatik Algıla",
                "Ghost Mode (Anti-Detect)": "Hayalet Modu (Anti-Algıla)",
                "Target Finder": "Hedef Bulucu",
                "Pick Target Color": "Hedef Renk Seç",
                "Tolerance:": "Tolerans:",
                "Pick Click Position": "Tıklama Pozisyonu Seç",
                "X:": "X:",
                "Y:": "Y:",
                "Theme:": "Tema:",
                "Stealth Key:": "Gizli Tuş:",
                "Macro Stop Key:": "Makro Durdurma Tuşu:",
                "Status: Idle": "Durum: Boşta",
                "Status: Clicking...": "Durum: Tıklanıyor...",
                "Status: Stopped": "Durum: Durduruldu",
                "Status: Done": "Durum: Tamamlandı",
                "Click inside to test your CPS": "CPS testi için tıklayın",
                "Test Duration (sec):": "Test Süresi (sn):",
                "Start CPS Test": "CPS Testini Başlat",
                "CPS: N/A": "CPS: YOK",
                "Start Recording Pattern": "Desen Kaydını Başlat",
                "Stop Recording Pattern": "Desen Kaydını Durdur",
                "Clear Pattern": "Deseni Temizle",
                "Pattern: None": "Desen: Yok",
                "Log:": "Kayıt:",
                "Run CPS Stats:": "CPS İstatistikleri:",
                "Live CPS Overlay": "Canlı CPS Kaplaması",
                "Overlay Position X,Y:": "Kaplama Pozisyonu X,Y:",
                "Admin Panel": "Yönetici Paneli",
                "New Macro": "Yeni Makro",
                "Delete": "Sil",
                "Edit": "Düzenle",
                "Apply Mods": "Modları Uygula",
            },
            "de": {
                "Clicker": "Klicker",
                "CPS Test": "CPS-Test",
                "Pattern": "Muster",
                "Logs/Stats": "Protokolle/Statistiken",
                "Download Mods": "Mods Herunterladen",
                "Macro": "Makro",
                "Overlay": "Overlay",
                "Admin Panel": "Admin Bereich",
                "Settings": "Einstellungen",
                "Language": "Sprache",
                "Apply": "Anwenden",
                "Target CPS:": "Ziel-CPS:",
                "Duration (sec, 0=infinite):": "Dauer (Sek, 0=unbegrenzt):",
                "Start Key:": "Starttaste:",
                "Stop Key:": "Stopptaste:",
                "Mode:": "Modus:",
                "Human-like Behavior": "Menschliches Verhalten",
                "Enable Heat-up Ramp": "Aufwärmrampe aktivieren",
                "Game Auto Detect": "Spiel automatisch erkennen",
                "Ghost Mode (Anti-Detect)": "Geistermodus (Anti-Erkennung)",
                "Target Finder": "Zielfinder",
                "Pick Target Color": "Ziel-Farbe wählen",
                "Tolerance:": "Toleranz:",
                "Pick Click Position": "Klick-Position wählen",
                "X:": "X:",
                "Y:": "Y:",
                "Theme:": "Thema:",
                "Stealth Key:": "Verstecktaste:",
                "Macro Stop Key:": "Makro-Stopp-Taste:",
                "Status: Idle": "Status: Leerlauf",
                "Status: Clicking...": "Status: Klickt...",
                "Status: Stopped": "Status: Gestoppt",
                "Status: Done": "Status: Fertig",
                "Click inside to test your CPS": "Klicken zum CPS-Test",
                "Test Duration (sec):": "Testdauer (Sek):",
                "Start CPS Test": "CPS-Test Starten",
                "CPS: N/A": "CPS: N/V",
                "Start Recording Pattern": "Musteraufnahme starten",
                "Stop Recording Pattern": "Musteraufnahme stoppen",
                "Clear Pattern": "Muster löschen",
                "Pattern: None": "Muster: Keines",
                "Log:": "Protokoll:",
                "Run CPS Stats:": "CPS-Statistiken:",
                "Live CPS Overlay": "Live CPS Overlay",
                "Overlay Position X,Y:": "Overlay-Position X,Y:",
                "Admin Panel": "Admin Bereich",
                "New Macro": "Neues Makro",
                "Delete": "Löschen",
                "Edit": "Bearbeiten",
                "Apply Mods": "Mods Anwenden",
            },
            "ja": {
                "Clicker": "クリッカー",
                "CPS Test": "CPSテスト",
                "Pattern": "パターン",
                "Logs/Stats": "ログ/統計",
                "Download Mods": "モッド ダウンロード",
                "Macro": "マクロ",
                "Overlay": "オーバーレイ",
                "Admin Panel": "管理パネル",
                "Settings": "設定",
                "Language": "言語",
                "Apply": "適用",
                "Target CPS:": "ターゲットCPS:",
                "Duration (sec, 0=infinite):": "持続時間(秒,0=無限):",
                "Start Key:": "開始キー:",
                "Stop Key:": "停止キー:",
                "Mode:": "モード:",
                "Human-like Behavior": "人間らしい動作",
                "Enable Heat-up Ramp": "ウォームアップ有効",
                "Game Auto Detect": "ゲーム自動検出",
                "Ghost Mode (Anti-Detect)": "ゴーストモード(アンチ検出)",
                "Target Finder": "ターゲットファインダー",
                "Pick Target Color": "ターゲット色選択",
                "Tolerance:": "許容値:",
                "Pick Click Position": "クリック位置選択",
                "X:": "X:",
                "Y:": "Y:",
                "Theme:": "テーマ:",
                "Stealth Key:": "ステルスキー:",
                "Macro Stop Key:": "マクロ停止キー:",
                "Status: Idle": "状態: 待機中",
                "Status: Clicking...": "状態: クリック中...",
                "Status: Stopped": "状態: 停止",
                "Status: Done": "状態: 完了",
                "Click inside to test your CPS": "CPSテスト用にクリック",
                "Test Duration (sec):": "テスト時間(秒):",
                "Start CPS Test": "CPSテスト開始",
                "CPS: N/A": "CPS: なし",
                "Start Recording Pattern": "パターン記録開始",
                "Stop Recording Pattern": "パターン記録停止",
                "Clear Pattern": "パターンクリア",
                "Pattern: None": "パターン: なし",
                "Log:": "ログ:",
                "Run CPS Stats:": "CPS統計:",
                "Live CPS Overlay": "ライブCPSオーバーレイ",
                "Overlay Position X,Y:": "オーバーレイ位置 X,Y:",
                "Admin Panel": "管理パネル",
                "New Macro": "新しいマクロ",
                "Delete": "削除",
                "Edit": "編集",
                "Apply Mods": "モッド適用",
            },
            "ru": {
                "Clicker": "Кликер",
                "CPS Test": "Тест CPS",
                "Pattern": "Шаблон",
                "Logs/Stats": "Логи/Статистика",
                "Download Mods": "Скачать Моды",
                "Macro": "Макрос",
                "Overlay": "Оверлей",
                "Admin Panel": "Панель Админа",
                "Settings": "Настройки",
                "Language": "Язык",
                "Apply": "Применить",
                "Target CPS:": "Целевой CPS:",
                "Duration (sec, 0=infinite):": "Длительность (сек, 0=бесконечно):",
                "Start Key:": "Клавиша Старт:",
                "Stop Key:": "Клавиша Стоп:",
                "Mode:": "Режим:",
                "Human-like Behavior": "Поведение как у человека",
                "Enable Heat-up Ramp": "Включить разогрев",
                "Game Auto Detect": "Автообнаружение игры",
                "Ghost Mode (Anti-Detect)": "Режим Призрака (Анти-обнаружение)",
                "Target Finder": "Поиск Цели",
                "Pick Target Color": "Выбор Цвета Цели",
                "Tolerance:": "Допуск:",
                "Pick Click Position": "Выбор Позиции Клика",
                "X:": "X:",
                "Y:": "Y:",
                "Theme:": "Тема:",
                "Stealth Key:": "Клавиша Скрытия:",
                "Macro Stop Key:": "Клавиша Остановки Макроса:",
                "Status: Idle": "Статус: Ожидание",
                "Status: Clicking...": "Статус: Кликает...",
                "Status: Stopped": "Статус: Остановлено",
                "Status: Done": "Статус: Готово",
                "Click inside to test your CPS": "Клик для теста CPS",
                "Test Duration (sec):": "Время теста (сек):",
                "Start CPS Test": "Начать тест CPS",
                "CPS: N/A": "CPS: Н/Д",
                "Start Recording Pattern": "Начать запись шаблона",
                "Stop Recording Pattern": "Остановить запись шаблона",
                "Clear Pattern": "Очистить шаблон",
                "Pattern: None": "Шаблон: Нет",
                "Log:": "Лог:",
                "Run CPS Stats:": "Статистика CPS:",
                "Live CPS Overlay": "Оверлей CPS",
                "Overlay Position X,Y:": "Позиция Оверлея X,Y:",
                "Admin Panel": "Панель Админа",
                "New Macro": "Новый Макрос",
                "Delete": "Удалить",
                "Edit": "Редактировать",
                "Apply Mods": "Применить Моды",
            },
            "zh": {
                "Clicker": "点击器",
                "CPS Test": "CPS 测试",
                "Pattern": "模式",
                "Logs/Stats": "日志/统计",
                "Download Mods": "下载 模组",
                "Macro": "宏",
                "Overlay": "覆盖",
                "Admin Panel": "管理员 面板",
                "Settings": "设置",
                "Language": "语言",
                "Apply": "应用",
                "Target CPS:": "目标 CPS:",
                "Duration (sec, 0=infinite):": "持续时间 (秒, 0=无限):",
                "Start Key:": "开始 键:",
                "Stop Key:": "停止 键:",
                "Mode:": "模式:",
                "Human-like Behavior": "模拟 人类 行为",
                "Enable Heat-up Ramp": "启用 预热",
                "Game Auto Detect": "自动 游戏 检测",
                "Ghost Mode (Anti-Detect)": "幽灵 模式 (反 检测)",
                "Target Finder": "目标 寻找",
                "Pick Target Color": "选择 目标 颜色",
                "Tolerance:": "容忍度:",
                "Pick Click Position": "选择 点击 位置",
                "X:": "X:",
                "Y:": "Y:",
                "Theme:": "主题:",
                "Stealth Key:": "隐藏 键:",
                "Macro Stop Key:": "宏 停止 键:",
                "Status: Idle": "状态: 空闲",
                "Status: Clicking...": "状态: 点击 中...",
                "Status: Stopped": "状态: 停止",
                "Status: Done": "状态: 完成",
                "Click inside to test your CPS": "点击进行 CPS 测试",
                "Test Duration (sec):": "测试 持续 时间 (秒):",
                "Start CPS Test": "开始 CPS 测试",
                "CPS: N/A": "CPS: 无",
                "Start Recording Pattern": "开始 记录 模式",
                "Stop Recording Pattern": "停止 记录 模式",
                "Clear Pattern": "清除 模式",
                "Pattern: None": "模式: 无",
                "Log:": "日志:",
                "Run CPS Stats:": "CPS 统计:",
                "Live CPS Overlay": "实时 CPS 覆盖",
                "Overlay Position X,Y:": "覆盖 位置 X,Y:",
                "Admin Panel": "管理员 面板",
                "New Macro": "新 宏",
                "Delete": "删除",
                "Edit": "编辑",
                "Apply Mods": "应用 模组",
            }
        }
        self.create_widgets()
        self.apply_theme()
        self.define_mods()
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.daemon = True
        self.listener.start()
        threading.Thread(target=self.game_detection_loop, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.append_log("Application started")

        


    def create_widgets(self):
        self.style = ttk.Style(self.root)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        frame_clicker = ttk.Frame(notebook, padding=10); notebook.add(frame_clicker, text="Clicker")
        frame_test = ttk.Frame(notebook, padding=10); notebook.add(frame_test, text="CPS Test")
        frame_pattern = ttk.Frame(notebook, padding=10); notebook.add(frame_pattern, text="Pattern")
        frame_logs = ttk.Frame(notebook, padding=10); notebook.add(frame_logs, text="Logs/Stats")
        frame_mods = ttk.Frame(notebook, padding=10); notebook.add(frame_mods, text="Download Mods")
        frame_macro = ttk.Frame(notebook, padding=10); notebook.add(frame_macro, text="Macro")
        frame_overlay = ttk.Frame(notebook, padding=10); notebook.add(frame_overlay, text="Overlay")
        frame_admin = ttk.Frame(notebook, padding=10); notebook.add(frame_admin, text="Admin Panel")
        frame_settings = ttk.Frame(notebook, padding=10); notebook.add(frame_settings, text=self.translations[self.languages[self.language_var.get()]][ "Settings" ])
        ttk.Label(frame_settings, text=self.translations[self.languages[self.language_var.get()]][ "Language" ] + ":").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        lang_combo = ttk.Combobox(frame_settings, values=list(self.languages.keys()), textvariable=self.language_var, state="readonly")
        lang_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_settings, text=self.translations[self.languages[self.language_var.get()]][ "Apply" ], command=self.change_language).grid(row=1, column=0, columnspan=2, pady=10)


        # --- Clicker Tab ---
        row = 0
        ttk.Label(frame_clicker, text="Target CPS:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_clicker, textvariable=self.cps_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(frame_clicker, text="Duration (sec, 0=infinite):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_clicker, textvariable=self.duration_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(frame_clicker, text="Start Key:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_clicker, textvariable=self.start_key_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(frame_clicker, text="Stop Key:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_clicker, textvariable=self.stop_key_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(frame_clicker, text="Mode:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        modes = ["Constant", "Heat-up", "Smart", "Burst", "Wave", "Random", "Learned"]
        ttk.Combobox(frame_clicker, values=modes, textvariable=self.mode_var, state="readonly").grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Checkbutton(frame_clicker, text="Human-like Behavior", variable=self.human_like_var).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Checkbutton(frame_clicker, text="Enable Heat-up Ramp", variable=self.heatup_var).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Checkbutton(frame_clicker, text="Game Auto Detect", variable=self.game_autodetect_var).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Checkbutton(frame_clicker, text="Ghost Mode (Anti-Detect)", variable=self.ghost_mode_var).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Checkbutton(frame_clicker, text="Target Finder", variable=self.target_finder_var).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(frame_clicker, text="Pick Target Color", command=self.start_color_picker).grid(row=row, column=0, padx=5, pady=5)
        ttk.Label(frame_clicker, text="Tolerance:").grid(row=row, column=1, sticky=tk.W)
        ttk.Entry(frame_clicker, textvariable=self.tolerance_var, width=5).grid(row=row, column=1, sticky=tk.E, padx=5)
        row += 1
        ttk.Button(frame_clicker, text="Pick Click Position", command=self.start_position_picker).grid(row=row, column=0, padx=5, pady=5)
        coord_frame = ttk.Frame(frame_clicker)
        coord_frame.grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(coord_frame, text="X:").pack(side=tk.LEFT)
        ttk.Entry(coord_frame, textvariable=self.target_x_var, width=5).pack(side=tk.LEFT)
        ttk.Label(coord_frame, text="Y:").pack(side=tk.LEFT)
        ttk.Entry(coord_frame, textvariable=self.target_y_var, width=5).pack(side=tk.LEFT)
        row += 1
        ttk.Label(frame_clicker, text="Tema:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        themes = ["Light", "Dark", "Neon", "Matrix"]
        ttk.Combobox(frame_clicker, values=themes, textvariable=self.theme_var, state="readonly").grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(frame_clicker, text="Stealth Key:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_clicker, textvariable=self.stealth_key_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        ttk.Label(frame_clicker, text="Macro Stop Key:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_clicker, textvariable=self.macro_stop_key_var).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        self.status_label = ttk.Label(frame_clicker, text="Status: Idle")
        self.status_label.grid(row=row, column=0, columnspan=2, pady=10)
        for i in range(2):
            frame_clicker.columnconfigure(i, weight=1)

        # --- CPS Test Tab ---
        ttk.Label(frame_test, text="Click inside to test your CPS").pack(pady=5)
        ttk.Label(frame_test, text="Test Duration (sec):").pack(anchor=tk.W, padx=5)
        self.test_duration_var = tk.StringVar(value="5")
        ttk.Entry(frame_test, textvariable=self.test_duration_var).pack(anchor=tk.W, padx=5)
        ttk.Button(frame_test, text="Start CPS Test", command=self.start_cps_test).pack(pady=10)
        self.cps_test_label = ttk.Label(frame_test, text="CPS: N/A")
        self.cps_test_label.pack(pady=5)
        self.cps_test_canvas = None

        # --- Pattern Tab ---
        ttk.Button(frame_pattern, text="Start Recording Pattern", command=self.start_recording_pattern).pack(pady=5)
        ttk.Button(frame_pattern, text="Stop Recording Pattern", command=self.stop_recording_pattern).pack(pady=5)
        ttk.Button(frame_pattern, text="Clear Pattern", command=self.clear_pattern).pack(pady=5)
        self.pattern_status = ttk.Label(frame_pattern, text="Pattern: None")
        self.pattern_status.pack(pady=5)

        # --- Logs/Stats Tab ---
        ttk.Label(frame_logs, text="Log:").pack(anchor=tk.W)
        self.log_text = ScrolledText(frame_logs, height=8, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)
        self.append_log("Log initialized")
        ttk.Label(frame_logs, text="Run CPS Stats:").pack(anchor=tk.W)
        self.stats_frame = ttk.Frame(frame_logs)
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Download Mods Tab ---
        canvas_mods = tk.Canvas(frame_mods)
        scrollbar_mods = ttk.Scrollbar(frame_mods, orient="vertical", command=canvas_mods.yview)
        self.mods_frame = ttk.Frame(canvas_mods)
        self.mods_frame.bind("<Configure>", lambda e: canvas_mods.configure(scrollregion=canvas_mods.bbox("all")))
        canvas_mods.create_window((0,0), window=self.mods_frame, anchor="nw")
        canvas_mods.configure(yscrollcommand=scrollbar_mods.set)
        canvas_mods.pack(side="left", fill="both", expand=True)
        scrollbar_mods.pack(side="right", fill="y")
        ttk.Button(frame_mods, text="Apply Mods", command=self.apply_mods_with_loading).pack(pady=10)

        # --- Macro Tab ---
        self.macro_listbox = tk.Listbox(frame_macro)
        self.macro_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ctrl_frame = ttk.Frame(frame_macro); ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        ttk.Button(ctrl_frame, text="New Macro", command=self.add_macro).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl_frame, text="Delete", command=self.delete_macro).pack(fill=tk.X, pady=2)
        ttk.Button(ctrl_frame, text="Edit", command=self.edit_macro).pack(fill=tk.X, pady=2)
        ttk.Label(frame_macro, text="(Press assigned key to run macro, use Macro Stop Key to cancel)").pack(anchor=tk.W, pady=5)

        # --- Overlay Tab ---
        ttk.Checkbutton(frame_overlay, text="Live CPS Overlay", variable=self.overlay_var, command=self.toggle_overlay).pack(anchor=tk.W, pady=5)
        ttk.Label(frame_overlay, text="Overlay Position X,Y:").pack(anchor=tk.W)
        pos_frame = ttk.Frame(frame_overlay); pos_frame.pack(anchor=tk.W, pady=5)
        ttk.Entry(pos_frame, textvariable=self.overlay_x, width=5).pack(side=tk.LEFT)
        ttk.Entry(pos_frame, textvariable=self.overlay_y, width=5).pack(side=tk.LEFT, padx=5)

        # --- Admin Panel Tab ---
        ttk.Label(frame_admin, text="Admin Panel").pack(anchor=tk.W, pady=5)
        help_text = ("Admin Panel:\n- Advanced commands here.\n- 25 example actions.\n")
        self.admin_help = ScrolledText(frame_admin, height=6, state='normal')
        self.admin_help.insert(tk.END, help_text); self.admin_help.configure(state='disabled'); self.admin_help.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)
        self.admin_listbox = tk.Listbox(frame_admin)
        for i in range(1,26): self.admin_listbox.insert(tk.END, f"Admin Action {i}")
        self.admin_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        btn_frame = ttk.Frame(frame_admin); btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Run", command=self.run_admin_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Help", command=self.show_admin_help).pack(side=tk.LEFT, padx=5)

    def apply_theme(self):
        choice = self.theme_var.get()
        if choice == "Light":
            bg = self.root.cget("bg"); fg = "black"; entry_bg = "white"
            try: self.style.theme_use('default')
            except: pass
        elif choice == "Dark":
            bg = "#2e2e2e"; fg = "white"; entry_bg = "#3e3e3e"
            try: self.style.theme_use('clam')
            except: pass
        elif choice == "Neon":
            bg = "#0f0f0f"; fg = "#39ff14"; entry_bg = "#1a1a1a"
            try: self.style.theme_use('clam')
            except: pass
        elif choice == "Matrix":
            bg = "#000000"; fg = "#00ff00"; entry_bg = "#002200"
            try: self.style.theme_use('clam')
            except: pass
        else:
            bg = self.root.cget("bg"); fg = "black"; entry_bg = "white"
        try: self.root.configure(bg=bg)
        except: pass
        self.style.configure('TLabel', background=bg, foreground=fg)
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg)
        self.style.configure('TCheckbutton', background=bg, foreground=fg)
        self.style.configure('TButton', background=bg, foreground=fg)
        try: self.log_text.configure(background=entry_bg, foreground=fg, insertbackground=fg)
        except: pass

    def define_mods(self):
        self.mods = [
            {"name": "Mouse Movement Mimic", "description": "Slight mouse movement before click.", "apply": self.apply_mouse_movement, "remove": self.remove_mouse_movement},
            {"name": "AI Pattern Recognition", "description": "Analyze click patterns and add jitter.", "apply": self.apply_ai_pattern, "remove": self.remove_ai_pattern},
            {"name": "FPS Counter", "description": "Show FPS counter window.", "apply": self.apply_fps_counter, "remove": self.remove_fps_counter},
            {"name": "Random CPS Fluctuation", "description": "Change CPS randomly.", "apply": self.apply_random_cps, "remove": self.remove_random_cps},
            {"name": "AFK Protection", "description": "Small mouse moves to prevent AFK.", "apply": self.apply_afk_protection, "remove": self.remove_afk_protection},
            {"name": "Micro Pauses", "description": "Short random pauses.", "apply": self.apply_micro_pauses, "remove": self.remove_micro_pauses},
            {"name": "Click Logger", "description": "Log clicks to file.", "apply": self.apply_click_logger, "remove": self.remove_click_logger},
            {"name": "Sound Effect", "description": "Play sound on click.", "apply": self.apply_sound_effect, "remove": self.remove_sound_effect},
            {"name": "Combo Simulator", "description": "Simulate predefined click combos.", "apply": self.apply_combo_simulator, "remove": self.remove_combo_simulator},
            {"name": "Anti-Detection", "description": "Add extra jitter/delays.", "apply": self.apply_anti_detection, "remove": self.remove_anti_detection},
            {"name": "Theme Switcher", "description": "Switch GUI theme.", "apply": self.apply_theme_switcher, "remove": self.remove_theme_switcher},
            {"name": "Stats Display", "description": "Show click statistics.", "apply": self.apply_stats_display, "remove": self.remove_stats_display},
            {"name": "Super Jitter", "description": "Apply extra random jitter.", "apply": self.apply_super_jitter, "remove": self.remove_super_jitter},
            {"name": "Ultra Random CPS", "description": "Wider random CPS range.", "apply": self.apply_ultra_random_cps, "remove": self.remove_ultra_random_cps},
            {"name": "Adaptive CPS", "description": "Adjust CPS based on game speed.", "apply": self.apply_adaptive_cps, "remove": self.remove_adaptive_cps},
            {"name": "Dynamic Heat-up", "description": "Dynamic heat-up ramp.", "apply": self.apply_dynamic_heatup, "remove": self.remove_dynamic_heatup},
            {"name": "Velocity Click", "description": "High-speed burst clicks.", "apply": self.apply_velocity_click, "remove": self.remove_velocity_click},
            {"name": "Mirror Mode", "description": "Reverse click direction placeholder.", "apply": self.apply_mirror_mode, "remove": self.remove_mirror_mode},
            {"name": "Auto Pause", "description": "Automatic pause at intervals.", "apply": self.apply_auto_pause, "remove": self.remove_auto_pause},
            {"name": "Rapid Fire", "description": "Short high-speed bursts.", "apply": self.apply_rapid_fire, "remove": self.remove_rapid_fire},
            {"name": "Smooth Click", "description": "Make clicks more human.", "apply": self.apply_smooth_click, "remove": self.remove_smooth_click},
            {"name": "Random Delay", "description": "Randomize delay.", "apply": self.apply_random_delay, "remove": self.remove_random_delay},
            {"name": "Stealth Enhancer", "description": "More hidden stealth mode.", "apply": self.apply_stealth_enhancer, "remove": self.remove_stealth_enhancer},
            {"name": "Auto Retry", "description": "Retry on failed click.", "apply": self.apply_auto_retry, "remove": self.remove_auto_retry},
        ]
        # Populate mods_frame
        for mod in self.mods:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(self.mods_frame, text=mod["name"], variable=var)
            chk.pack(anchor=tk.W, pady=2)
            chk.bind("<Enter>", lambda e, d=mod["description"]: self.status_label.config(text=f"Açıklama: {d}"))
            chk.bind("<Leave>", lambda e: self.status_label.config(text="Status: Idle" if not self.clicking else "Status: Clicking..."))
            self.mod_vars[mod["name"]] = var

    # Example apply/remove methods:
    def apply_mouse_movement(self):
        self.active_mods["Mouse Movement Mimic"] = True
    def remove_mouse_movement(self):
        self.active_mods.pop("Mouse Movement Mimic", None)

    def apply_ai_pattern(self):
        self.active_mods["AI Pattern Recognition"] = True
    def remove_ai_pattern(self):
        self.active_mods.pop("AI Pattern Recognition", None)

    def apply_fps_counter(self):
        self.active_mods["FPS Counter"] = True
        try:
            self.fps_win = tk.Toplevel(self.root)
            self.fps_win.title("FPS Counter")
            self.fps_label = ttk.Label(self.fps_win, text="FPS: N/A")
            self.fps_label.pack(padx=10, pady=10)
        except: pass
    def remove_fps_counter(self):
        try:
            if hasattr(self, 'fps_win') and self.fps_win.winfo_exists(): self.fps_win.destroy()
        except: pass
        self.active_mods.pop("FPS Counter", None)

    def apply_random_cps(self):
        self.active_mods["Random CPS Fluctuation"] = True
    def remove_random_cps(self):
        self.active_mods.pop("Random CPS Fluctuation", None)

    def apply_afk_protection(self):
        self.active_mods["AFK Protection"] = True
    def remove_afk_protection(self):
        self.active_mods.pop("AFK Protection", None)

    def apply_micro_pauses(self):
        self.active_mods["Micro Pauses"] = True
    def remove_micro_pauses(self):
        self.active_mods.pop("Micro Pauses", None)

    def apply_click_logger(self):
        try:
            with open(self.log_file, "a"): pass
        except: pass
        self.active_mods["Click Logger"] = True
    def remove_click_logger(self):
        self.active_mods.pop("Click Logger", None)

    def apply_sound_effect(self):
        self.active_mods["Sound Effect"] = True
    def remove_sound_effect(self):
        self.active_mods.pop("Sound Effect", None)

    def apply_combo_simulator(self):
        self.active_mods["Combo Simulator"] = True
    def remove_combo_simulator(self):
        self.active_mods.pop("Combo Simulator", None)

    def apply_anti_detection(self):
        self.active_mods["Anti-Detection"] = True
    def remove_anti_detection(self):
        self.active_mods.pop("Anti-Detection", None)

    def apply_theme_switcher(self):
        current = self.theme_var.get(); new = "Dark" if current=="Light" else "Light"
        self.theme_var.set(new); self.apply_theme()
        self.active_mods["Theme Switcher"] = True
    def remove_theme_switcher(self):
        self.theme_var.set("Light"); self.apply_theme()
        self.active_mods.pop("Theme Switcher", None)

    def apply_stats_display(self):
        self.active_mods["Stats Display"] = True
    def remove_stats_display(self):
        self.active_mods.pop("Stats Display", None)

    def apply_super_jitter(self):
        self.active_mods["Super Jitter"] = True
    def remove_super_jitter(self):
        self.active_mods.pop("Super Jitter", None)

    def apply_ultra_random_cps(self):
        self.active_mods["Ultra Random CPS"] = True
    def remove_ultra_random_cps(self):
        self.active_mods.pop("Ultra Random CPS", None)

    def apply_adaptive_cps(self):
        self.active_mods["Adaptive CPS"] = True
    def remove_adaptive_cps(self):
        self.active_mods.pop("Adaptive CPS", None)

    def apply_dynamic_heatup(self):
        self.active_mods["Dynamic Heat-up"] = True
    def remove_dynamic_heatup(self):
        self.active_mods.pop("Dynamic Heat-up", None)

    def apply_velocity_click(self):
        self.active_mods["Velocity Click"] = True
    def remove_velocity_click(self):
        self.active_mods.pop("Velocity Click", None)

    def apply_mirror_mode(self):
        self.active_mods["Mirror Mode"] = True
    def remove_mirror_mode(self):
        self.active_mods.pop("Mirror Mode", None)

    def apply_auto_pause(self):
        self.active_mods["Auto Pause"] = True
    def remove_auto_pause(self):
        self.active_mods.pop("Auto Pause", None)

    def apply_rapid_fire(self):
        self.active_mods["Rapid Fire"] = True
    def remove_rapid_fire(self):
        self.active_mods.pop("Rapid Fire", None)

    def apply_smooth_click(self):
        self.active_mods["Smooth Click"] = True
    def remove_smooth_click(self):
        self.active_mods.pop("Smooth Click", None)

    def apply_random_delay(self):
        self.active_mods["Random Delay"] = True
    def remove_random_delay(self):
        self.active_mods.pop("Random Delay", None)

    def apply_stealth_enhancer(self):
        self.active_mods["Stealth Enhancer"] = True
    def remove_stealth_enhancer(self):
        self.active_mods.pop("Stealth Enhancer", None)

    def apply_auto_retry(self):
        self.active_mods["Auto Retry"] = True
    def remove_auto_retry(self):
        self.active_mods.pop("Auto Retry", None)

    def apply_mods_with_loading(self):
        selected = [mod for mod in self.mods if self.mod_vars.get(mod["name"], tk.BooleanVar()).get()]
        to_activate = [mod for mod in selected if mod["name"] not in self.active_mods]
        to_deactivate = [mod for mod in self.mods if mod["name"] in self.active_mods and not self.mod_vars.get(mod["name"], tk.BooleanVar()).get()]
        if not to_activate and not to_deactivate:
            messagebox.showinfo("Info", "No changes.")
            return
        load_win = tk.Toplevel(self.root); load_win.title("Applying Mods"); load_win.geometry("300x100")
        ttk.Label(load_win, text="Loading...").pack(pady=10)
        progress = ttk.Progressbar(load_win, orient='horizontal', length=250, mode='determinate'); progress.pack(pady=10)
        load_win.grab_set()
        def load_sequence():
            for i in range(101):
                time.sleep(0.01); progress['value'] = i; load_win.update_idletasks()
            for mod in to_activate:
                try: mod["apply"](); self.active_mods[mod["name"]] = mod
                except Exception as e: logging.error(f"Error applying mod {mod['name']}: {e}")
            for mod in to_deactivate:
                try: mod["remove"](); self.active_mods.pop(mod["name"], None)
                except Exception as e: logging.error(f"Error removing mod {mod['name']}: {e}")
            load_win.destroy(); messagebox.showinfo("Info", "Mods applied.")
        threading.Thread(target=load_sequence, daemon=True).start()

    # --- Macro methods ---
    def add_macro(self):
        name = simpledialog.askstring("Macro Name", "Enter macro name:")
        if not name:
            return
        key = simpledialog.askstring("Macro Key", "Enter key to trigger macro (single char or key name):")
        if not key:
            return
        try:
            count = int(simpledialog.askstring("Click Count", "Number of clicks:"))
        except:
            count = 1
        try:
            delay = float(simpledialog.askstring("Delay", "Delay between clicks (sec):"))
        except:
            delay = 0.1
        macro = {"name": name, "key": key.lower(), "count": count, "delay": delay}
        self.macros.append(macro)
        self.macro_listbox.insert(tk.END, f"{name} ({key.lower()})")

    def delete_macro(self):
        sel = self.macro_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.macros.pop(idx)
        self.macro_listbox.delete(idx)

    def edit_macro(self):
        sel = self.macro_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        macro = self.macros[idx]
        name = simpledialog.askstring("Macro Name", "Enter macro name:", initialvalue=macro["name"])
        if not name:
            return
        key = simpledialog.askstring("Macro Key", "Enter key to trigger macro:", initialvalue=macro["key"])
        if not key:
            return
        try:
            count = int(simpledialog.askstring("Click Count", "Number of clicks:", initialvalue=str(macro["count"])))
        except:
            count = macro["count"]
        try:
            delay = float(simpledialog.askstring("Delay", "Delay between clicks (sec):", initialvalue=str(macro["delay"])))
        except:
            delay = macro["delay"]
        macro.update({"name": name, "key": key.lower(), "count": count, "delay": delay})
        self.macro_listbox.delete(idx)
        self.macro_listbox.insert(idx, f"{name} ({key.lower()})")

    def run_macro(self, macro):
        for _ in range(macro.get("count",1)):
            if self.macro_stop_event.is_set():
                break
            try: self.mouse.click(Button.left)
            except: pass
            if hasattr(self, 'click_count'):
                self.click_count += 1
            time.sleep(macro.get("delay",0.1))

    # --- Overlay methods ---
    def toggle_overlay(self):
        if self.overlay_var.get():
            self.overlay_win = tk.Toplevel(self.root); self.overlay_win.overrideredirect(True)
            self.overlay_win.attributes("-topmost", True)
            self.overlay_win.geometry(f"+{self.overlay_x.get()}+{self.overlay_y.get()}")
            self.overlay_label = ttk.Label(self.overlay_win, text="CPS: 0.00", background="black", foreground="white")
            self.overlay_label.pack()
            self.update_overlay()
        else:
            if hasattr(self, "overlay_win") and self.overlay_win.winfo_exists():
                self.overlay_win.destroy()

    def update_overlay(self):
        curr = 0.0
        if hasattr(self, "click_start_time") and hasattr(self, "click_count"):
            elapsed = time.time() - self.click_start_time
            curr = self.click_count / elapsed if elapsed > 0 else 0.0
        try: self.overlay_label.config(text=f"CPS: {curr:.2f}")
        except: pass
        if getattr(self, "overlay_win", None) and self.overlay_var.get():
            self.root.after(500, self.update_overlay)

    # --- Admin Panel methods ---
    def run_admin_action(self):
        sel = self.admin_listbox.curselection()
        if not sel:
            messagebox.showinfo("Admin Panel", "Please select an action.")
            return
        action = self.admin_listbox.get(sel[0])
        # Placeholder: implement admin actions here
        messagebox.showinfo("Admin Panel", f"Executed {action} (placeholder).")

    def show_admin_help(self):
        messagebox.showinfo("Admin Help", "This panel contains 25 admin actions.\nSelect one and press Run.")

    # --- Other methods (click_loop, start_clicking, etc) same as earlier ---
    def start_clicking(self):
        try:
            target_cps = float(self.cps_var.get()); duration = float(self.duration_var.get())
            if target_cps <= 0 or duration < 0: raise ValueError
        except:
            self.status_label.config(text="Status: Invalid CPS/Duration")
            return
        self.run_count = getattr(self, 'run_count', 0) + 1
        logging.info(f"Run {self.run_count}: Starting CPS={target_cps}, duration={duration}, mode={self.mode_var.get()}")
        self.clicking = True; self.stop_event.clear()
        self.click_start_time = time.time(); self.click_count = 0
        self.status_label.config(text="Status: Clicking...")
        self.append_log(f"Started clicking CPS={self.cps_var.get()}")
        threading.Thread(target=self.click_loop, args=(target_cps, duration), daemon=True).start()

    def stop_clicking(self):
        if self.clicking:
            self.clicking = False; self.stop_event.set()
            self.status_label.config(text="Status: Stopped")
            self.append_log("Stopped clicking by user")
            logging.info(f"Run {self.run_count}: Stopped by user")

    def click_loop(self, target_cps, duration):
        start_time = time.time()
        end_time = None if duration == 0 else start_time + duration
        click_count = 0
        use_position = not (self.target_x_var.get() == 0 and self.target_y_var.get() == 0)
        tx, ty = self.target_x_var.get(), self.target_y_var.get()
        pattern = self.pattern_intervals if self.pattern_intervals else None
        pat_index = 0
        while self.clicking and (end_time is None or time.time() < end_time):
            if self.mode_var.get() == "Learned" and pattern:
                interval = pattern[pat_index % len(pattern)]
                if self.ghost_mode_var.get() and random.random() < 0.02:
                    time.sleep(random.uniform(0.5,1.5))
                time.sleep(interval)
                if self.target_finder_var.get() and self.target_color:
                    loc = self.find_color_on_screen()
                    if loc:
                        try: self.mouse.position = loc
                        except: pass
                elif use_position:
                    try: self.mouse.position = (tx, ty)
                    except: pass
                try:
                    self.mouse.click(Button.left)
                    click_count += 1; self.click_count = click_count
                except: pass
                pat_index += 1
                continue
            elapsed = time.time() - start_time
            mode = self.mode_var.get()
            if mode == "Constant":
                current_cps = target_cps
            elif mode == "Heat-up":
                ramp = 2.0
                if elapsed < ramp and self.heatup_var.get():
                    factor = 0.5 + 0.5 * (elapsed / ramp)
                    current_cps = target_cps * factor
                else:
                    current_cps = target_cps
            elif mode == "Smart":
                current_cps = target_cps * random.uniform(0.5, 1.5)
            elif mode == "Burst":
                period = 1.0; cycle = elapsed % (2 * period)
                current_cps = target_cps * (1.5 if cycle < period else 0.5)
            elif mode == "Wave":
                period = 4.0; sine = math.sin(2 * math.pi * (elapsed / period))
                current_cps = target_cps * (1 + 0.2 * sine)
            elif mode == "Random":
                current_cps = target_cps * random.uniform(0.3, 1.7)
            else:
                current_cps = target_cps
            if self.ghost_mode_var.get():
                if random.random() < 0.02:
                    time.sleep(random.uniform(0.5,1.5))
                current_cps *= random.uniform(0.8,1.2)
            if self.human_like_var.get():
                if random.random() < 0.05:
                    time.sleep(random.uniform(0.1, 0.5))
                interval = 1.0 / current_cps if current_cps > 0 else 0.01
                interval *= random.uniform(0.85, 1.15)
            else:
                interval = 1.0 / current_cps if current_cps > 0 else 0.01
            if self.target_finder_var.get() and self.target_color:
                loc = self.find_color_on_screen()
                if loc:
                    try: self.mouse.position = loc
                    except: pass
            elif use_position:
                try: self.mouse.position = (tx, ty)
                except: pass
            try:
                self.mouse.click(Button.left)
                click_count += 1; self.click_count = click_count
            except Exception as e:
                logging.error(f"Click error: {e}"); break
            sleep_until = time.time() + interval
            while time.time() < sleep_until:
                if not self.clicking or self.stop_event.is_set():
                    break
                time.sleep(0.005)
        actual = time.time() - start_time
        actual_cps = click_count / actual if actual > 0 else 0
        self.run_stats.append(actual_cps)
        if self.clicking:
            self.status_label.config(text="Status: Done")
            self.append_log(f"Finished clicking actual CPS={self.click_count}")
            logging.info(f"Run {self.run_count}: Finished: Clicks={click_count}, Duration={actual:.2f}s, CPS={actual_cps:.2f}")
        else:
            logging.info(f"Run {self.run_count}: Stopped early: Clicks={click_count}, Duration={actual:.2f}s, CPS={actual_cps:.2f}")
        self.clicking = False
        try:
            self.update_stats_plot()
        except:
            pass

    def start_cps_test(self):
        try:
            duration = float(self.test_duration_var.get())
            if duration <= 0:
                raise ValueError
        except:
            messagebox.showerror("Invalid input", "Test duration must be > 0")
            return
        test_win = tk.Toplevel(self.root)
        test_win.title("CPS Test")
        test_win.geometry("900x600")
        btn = ttk.Button(test_win, text="Click Me!")
        btn.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        label = ttk.Label(test_win, text="Time left: {:.1f}s".format(duration))
        label.pack()
        times = []
        start_time = {'t0': None}
        def on_click(event=None):
            now = time.time()
            if start_time['t0'] is None:
                start_time['t0'] = now
            times.append(now)
            elapsed = now - start_time['t0']
            remaining = duration - elapsed
            if remaining <= 0:
                test_win.destroy()
                total = now - start_time['t0']
                avg = len(times) / total if total > 0 else 0
                self.cps_test_label.config(text=f"CPS: {avg:.2f}")
                self.plot_cps_test(times, start_time['t0'], duration)
                self.show_advanced_stats(times, start_time['t0'])
            else:
                label.config(text="Time left: {:.1f}s".format(remaining))
        btn.bind("<Button-1>", on_click)

    def plot_cps_test(self, times, start_t, duration):
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except:
            return
        bins = int(duration) + 1
        counts = []
        for i in range(bins):
            t0 = start_t + i
            t1 = start_t + i + 1
            counts.append(sum(1 for t in times if t0 <= t < t1))
        for w in self.stats_frame.winfo_children():
            w.destroy()
        fig = Figure(figsize=(5,3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(range(1, len(counts)+1), counts)
        ax.set_title("CPS per Second")
        ax.set_xlabel("Second")
        ax.set_ylabel("Clicks")
        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_advanced_stats(self, times, start_t):
        if not times:
            return
        intervals = [times[i] - times[i-1] for i in range(1, len(times))]
        avg_delay = sum(intervals)/len(intervals) if intervals else 0
        max_cps = 0
        for t in range(int(times[-1]-start_t)+1):
            count = sum(1 for tm in times if start_t + t <= tm < start_t + t +1)
            if count > max_cps:
                max_cps = count
        stdev = statistics.pstdev(intervals) if len(intervals)>1 else 0
        jitter_pct = (stdev/avg_delay*100) if avg_delay>0 else 0
        inconsistent = [i for i in intervals if abs(i-avg_delay) > 0.2*avg_delay] if avg_delay>0 else []
        info = (f"Advanced Stats:\n"
                f"- Maximum CPS: {max_cps}\n"
                f"- Average Delay: {avg_delay:.4f}s\n"
                f"- Std Dev of Delay: {stdev:.4f}s\n"
                f"- Jitter %: {jitter_pct:.1f}%\n"
                f"- Inconsistent intervals count: {len(inconsistent)} of {len(intervals)}")
        messagebox.showinfo("Advanced CPS Stats", info)

    def find_color_on_screen(self):
        try:
            img = ImageGrab.grab()
            w, h = img.size
            pixels = img.load()
            target = self.target_color
            tol = self.tolerance_var.get()
            step = 10
            for x in range(0, w, step):
                for y in range(0, h, step):
                    pix = pixels[x, y]
                    if all(abs(pix[i] - target[i]) <= tol for i in range(3)):
                        return (x, y)
        except Exception as e:
            logging.error(f"Color search error: {e}")
        return None

    def start_color_picker(self):
        messagebox.showinfo("Pick Color", "Next left-click anywhere will pick target color.")
        def on_click(x, y, button, pressed):
            if pressed and button == Button.left:
                try:
                    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
                    color = img.getpixel((0,0))
                    self.target_color = color
                    messagebox.showinfo("Color Set", f"Target color set to {color}")
                except Exception as e:
                    logging.error(f"Color pick error: {e}")
                return False
            return True
        listener = pynput_mouse.Listener(on_click=on_click)
        listener.start()

    def start_position_picker(self):
        if self.position_picker_active:
            return
        self.position_picker_active = True
        messagebox.showinfo("Pick Position", "Next left-click anywhere will set click position.")
        def on_click(x, y, button, pressed):
            if pressed and button == Button.left:
                self.target_x_var.set(int(x)); self.target_y_var.set(int(y))
                messagebox.showinfo("Position Set", f"Position set to X={int(x)}, Y={int(y)}")
                self.position_picker_active = False
                return False
            return True
        listener = pynput_mouse.Listener(on_click=on_click)
        listener.start()

    def start_recording_pattern(self):
        if self.recording_pattern:
            return
        self.recording_pattern = True
        self.pattern_intervals = []
        self.pattern_last_time = None
        messagebox.showinfo("Pattern Recording", "Perform left-clicks; intervals recorded. Press Stop when done.")
        def on_click(x, y, button, pressed):
            if pressed and button == Button.left:
                now = time.time()
                if self.pattern_last_time is not None:
                    interval = now - self.pattern_last_time
                    self.pattern_intervals.append(interval)
                self.pattern_last_time = now
        self.pattern_listener = pynput_mouse.Listener(on_click=on_click)
        self.pattern_listener.start()
        self.pattern_status.config(text="Recording...")

    def stop_recording_pattern(self):
        if not self.recording_pattern:
            return
        self.recording_pattern = False
        try: self.pattern_listener.stop()
        except: pass
        if self.pattern_intervals:
            self.pattern_status.config(text=f"Pattern recorded: {len(self.pattern_intervals)} intervals")
        else:
            self.pattern_status.config(text="No pattern recorded")
        self.pattern_last_time = None

    def clear_pattern(self):
        self.pattern_intervals = []
        self.pattern_status.config(text="Pattern: None")

    def append_log(self, message):
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            entry = f"{timestamp} - {message}\n"
            with open(self.log_file, "a") as f:
                f.write(entry)
            if hasattr(self, "log_text"):
                try:
                    self.log_text.configure(state='normal')
                    self.log_text.insert(tk.END, entry)
                    self.log_text.configure(state='disabled')
                    self.log_text.see(tk.END)
                except:
                    pass
        except:
            pass

    def on_key_press(self, key):
        try:
            k = key.char.lower()
        except:
            k = str(key).replace('Key.', '').lower()
        if not self.clicking and k == self.start_key_var.get().strip().lower():
            self.start_clicking()
        elif self.clicking and k == self.stop_key_var.get().strip().lower():
            self.stop_clicking()
        if k == self.stealth_key_var.get().strip().lower():
            if self.root.winfo_viewable():
                self.root.withdraw()
            else:
                self.root.deiconify()
        if k == self.macro_stop_key_var.get().strip().lower():
            self.macro_stop_event.set()
        for macro in list(self.macros):
            if k == macro.get("key"):
                self.macro_stop_event.clear()
                threading.Thread(target=self.run_macro, args=(macro,), daemon=True).start()

    def game_detection_loop(self):
        while True:
            if self.game_autodetect_var.get():
                title = get_active_window_title().lower()
                # Implement detection-based behavior
            time.sleep(1)

    def update_stats_plot(self):
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except:
            return
        for w in self.stats_frame.winfo_children():
            w.destroy()
        fig = Figure(figsize=(5,3), dpi=100)
        ax = fig.add_subplot(111)
        runs = list(range(1, len(self.run_stats)+1))
        ax.plot(runs, self.run_stats, marker='o')
        ax.set_title("Actual CPS per Run"); ax.set_xlabel("Run #"); ax.set_ylabel("CPS"); ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame); canvas.draw(); canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    
    def change_language(self):
        # Show loading dialog
        load_win = tk.Toplevel(self.root); load_win.title("Loading")
        ttk.Label(load_win, text="Loading...").pack(pady=10)
        progress = ttk.Progressbar(load_win, orient='horizontal', length=200, mode='indeterminate')
        progress.pack(pady=10)
        progress.start(10)
        self.root.update_idletasks()
        # Change labels/texts
        lang_key = self.languages[self.language_var.get()]
        # Update tab texts
        for idx, key in enumerate(["Clicker","CPS Test","Pattern","Logs/Stats","Download Mods","Macro","Overlay","Admin Panel","Settings"]):
            try:
                tab_text = self.translations[lang_key][key]
                self.root.nametowidget(self.root.winfo_children()[0]).tab(idx, text=tab_text)
            except:
                pass
        # Update static labels in Clicker tab
        # For simplicity, restart UI: destroy and recreate widgets
        load_win.destroy()
        self.create_widgets()
        self.apply_theme()
        self.append_log(f"Language changed to {self.language_var.get()}")


    def on_close(self):
        self.clicking = False
        self.stop_event.set()
        self.macro_stop_event.set()
        try:
            self.listener.stop()
        except:
            pass
        self.root.quit()

if __name__ == "__main__":
    missing = []
    try:
        import pynput
    except ImportError:
        missing.append("pynput")
    if missing:
        messagebox.showerror("Dependencies Missing", "Missing modules: " + ", ".join(missing))
        sys.exit(1)
    root = tk.Tk()
    app = PhotonPulseAutoClicker18D2(root)
    root.mainloop()
