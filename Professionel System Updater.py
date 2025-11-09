#!/usr/bin/env python3
"""
🚀 PROFESYONEL SİSTEM GÜNCELLEYİCİ v5 (Birleştirilmiş Sürüm)
Tüm Gelişmiş Özelliklerle Tam Entegre ve Gerçek Yetki Yönetimi
"""

# ---------- PYTHON STANDART KÜTÜPHANELERİ ----------
import os
import platform
import shutil
import subprocess
import threading
import time
from datetime import datetime, timedelta
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
import zipfile
import tempfile
import webbrowser
import queue
import asyncio
import secrets
import hashlib
from io import BytesIO
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor
from http.server import HTTPServer, BaseHTTPRequestHandler

# ---------- ÜÇÜNCÜ PARTİ KÜTÜPHANELER ----------
try:
    import customtkinter as ctk
    from tkinter import messagebox, Menu
    import schedule
    import requests
    import psutil
    from cryptography.fernet import Fernet
    import docker
    from PIL import Image, ImageDraw
    import pystray
    import aiohttp
except ImportError as e:
    print(f"❌ EKSİK KÜTÜPHANE: {e}")
    print("Lütfen gerekli tüm kütüphaneleri yüklediğinizden emin olun:")
    print("pip install customtkinter schedule requests psutil cryptography docker pystray aiohttp pillow")
    sys.exit(1)


# =============================================================================
# BÖLÜM 1: TEMEL SİSTEM VE PAKET YÖNETİMİ (v1'den)
# =============================================================================

# ---------- Platform Tespiti ----------
class PlatformDetector:
    @staticmethod
    def get_platform_info():
        """Detaylı platform bilgilerini döndür"""
        system = platform.system().lower()
        info = {
            'system': system,
            'release': platform.release(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'python_version': platform.python_version()
        }
        
        if system == 'linux':
            info['distribution'] = PlatformDetector.get_linux_distro()
        elif system == 'darwin':
            info['distribution'] = PlatformDetector.get_macos_version()
            
        return info
    
    @staticmethod
    def get_linux_distro():
        """Linux dağıtımını tespit et"""
        try:
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            return line.split('=')[1].strip().strip('"')
        except:
            pass
        return "Linux"
    
    @staticmethod
    def get_macos_version():
        """macOS versiyonunu tespit et"""
        try:
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True)
            return f"macOS {result.stdout.strip()}"
        except:
            return "macOS"

# ---------- Çapraz Platform Paket Yöneticileri ----------
class CrossPlatformPackageManager:
    def __init__(self):
        self.platform_info = PlatformDetector.get_platform_info()
        self.system = self.platform_info['system']
        
    def get_available_managers(self) -> Dict[str, Dict]:
        """Mevcut paket yöneticilerini tespit et"""
        managers = {}
        
        if self.system == 'windows':
            managers.update(self._get_windows_managers())
        elif self.system == 'darwin':
            managers.update(self._get_macos_managers())
        elif self.system == 'linux':
            managers.update(self._get_linux_managers())
            
        return managers
    
    def _get_windows_managers(self):
        managers = {}
        if shutil.which('winget'):
            managers['winget'] = {
                'name': 'Windows Package Manager',
                'commands': [
                    ['winget', 'upgrade', '--all', '--accept-source-agreements', '--accept-package-agreements']
                ]
            }
        if shutil.which('choco'):
            managers['choco'] = {
                'name': 'Chocolatey',
                'commands': [['choco', 'upgrade', 'all', '-y']]
            }
        if shutil.which('scoop'):
            managers['scoop'] = {
                'name': 'Scoop',
                'commands': [['scoop', 'update'], ['scoop', 'update', '*']]
            }
        return managers
    
    def _get_macos_managers(self):
        managers = {}
        if shutil.which('brew'):
            managers['brew'] = {
                'name': 'Homebrew',
                'commands': [['brew', 'update'], ['brew', 'upgrade'], ['brew', 'cleanup', '-s']]
            }
        if shutil.which('mas'):
            managers['mas'] = {
                'name': 'Mac App Store',
                'commands': [['mas', 'upgrade']]
            }
        if shutil.which('port'):
            managers['port'] = {
                'name': 'MacPorts',
                'commands': [['sudo', 'port', 'selfupdate'], ['sudo', 'port', 'upgrade', 'outdated']]
            }
        return managers
    
    def _get_linux_managers(self):
        managers = {}
        if shutil.which('apt') or shutil.which('apt-get'):
            apt_cmd = 'apt' if shutil.which('apt') else 'apt-get'
            managers['apt'] = {
                'name': 'APT Package Manager',
                'commands': [
                    ['sudo', apt_cmd, 'update'],
                    ['sudo', apt_cmd, 'upgrade', '-y'],
                    ['sudo', apt_cmd, 'autoremove', '-y']
                ]
            }
        if shutil.which('dnf'):
            managers['dnf'] = {
                'name': 'DNF Package Manager',
                'commands': [['sudo', 'dnf', 'upgrade', '--refresh', '-y']]
            }
        if shutil.which('pacman'):
            managers['pacman'] = {
                'name': 'Pacman Package Manager',
                'commands': [['sudo', 'pacman', '-Syu', '--noconfirm']]
            }
        if shutil.which('zypper'):
            managers['zypper'] = {
                'name': 'Zypper Package Manager',
                'commands': [['sudo', 'zypper', 'refresh'], ['sudo', 'zypper', 'update', '-y']]
            }
        if shutil.which('snap'):
            managers['snap'] = {
                'name': 'Snap Packages',
                'commands': [['sudo', 'snap', 'refresh']]
            }
        if shutil.which('flatpak'):
            managers['flatpak'] = {
                'name': 'Flatpak Applications',
                'commands': [['flatpak', 'update', '-y']]
            }
        return managers


# =============================================================================
# BÖLÜM 2: ZAMANLAMA YÖNETİMİ (v2'den)
# =============================================================================

# ---------- Zamanlama Sistemi ----------
class ScheduledUpdateManager:
    def __init__(self, config_file="schedule_config.json"):
        self.config_file = config_file
        self.schedule_config = self.load_config()
        self.scheduler_running = False
        
    def load_config(self) -> Dict:
        default_config = {
            "enabled": False, "schedule_type": "weekly", "day_of_week": "monday",
            "time": "14:00", "last_run": None, "next_run": None
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Config yükleme hatası: {e}")
        return default_config
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedule_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Config kaydetme hatası: {e}")
    
    def set_schedule(self, schedule_type: str, day_of_week: str, time_str: str):
        self.schedule_config.update({
            "enabled": True, "schedule_type": schedule_type.lower(),
            "day_of_week": day_of_week.lower(), "time": time_str,
            "next_run": self.calculate_next_run(schedule_type, day_of_week, time_str)
        })
        self.save_config()
        
    def calculate_next_run(self, schedule_type: str, day_of_week: str, time_str: str) -> str:
        now = datetime.now()
        target_time = datetime.strptime(time_str, "%H:%M").time()
        
        if schedule_type == "daily":
            next_run = datetime.combine(now.date(), target_time)
            if next_run <= now:
                next_run += timedelta(days=1)
        elif schedule_type == "weekly":
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            target_day = days.index(day_of_week.lower())
            days_ahead = (target_day - now.weekday() + 7) % 7
            if days_ahead == 0 and next_run <= now:
                days_ahead = 7
            next_run = datetime.combine(now.date() + timedelta(days=days_ahead), target_time)
        else:  # monthly
            next_run = datetime.combine(now.date().replace(day=1), target_time)
            if next_run <= now:
                next_run = next_run.replace(month=next_run.month + 1)
        return next_run.isoformat()
    
    def get_next_run_info(self) -> str:
        if not self.schedule_config.get("enabled", False):
            return "Zamanlama kapalı"
        next_run_str = self.schedule_config.get("next_run")
        if not next_run_str:
            return "Zamanlama ayarlanmamış"
        try:
            next_run = datetime.fromisoformat(next_run_str)
            now = datetime.now()
            if next_run <= now:
                return "Şimdi çalışacak!"
            delta = next_run - now
            days, hours, minutes = delta.days, delta.seconds // 3600, (delta.seconds % 3600) // 60
            if days > 0: return f"{days} gün {hours} saat sonra"
            if hours > 0: return f"{hours} saat {minutes} dakika sonra"
            return f"{minutes} dakika sonra"
        except Exception as e:
            return f"Hesaplama hatası: {e}"
    
    def start_scheduler(self, update_callback):
        if not self.schedule_config.get("enabled", False):
            return
        self.scheduler_running = True
        self.update_callback = update_callback
        schedule.clear()
        
        schedule_type = self.schedule_config["schedule_type"]
        time_str = self.schedule_config["time"]
        
        if schedule_type == "daily":
            schedule.every().day.at(time_str).do(self._run_scheduled_update)
        elif schedule_type == "weekly":
            day_method = getattr(schedule.every(), self.schedule_config["day_of_week"])
            day_method.at(time_str).do(self._run_scheduled_update)
        
        threading.Thread(target=self._scheduler_loop, daemon=True).start()
        logging.info("⏰ Zamanlayıcı başlatıldı")
    
    def _scheduler_loop(self):
        while self.scheduler_running:
            schedule.run_pending()
            time.sleep(60)
    
    def _run_scheduled_update(self):
        logging.info("🔄 Zamanlanmış güncelleme başlatılıyor...")
        self.schedule_config["last_run"] = datetime.now().isoformat()
        self.schedule_config["next_run"] = self.calculate_next_run(
            self.schedule_config["schedule_type"], self.schedule_config["day_of_week"], self.schedule_config["time"]
        )
        self.save_config()
        if self.update_callback:
            self.update_callback(update_type="scheduled")
    
    def stop_scheduler(self):
        self.scheduler_running = False
        schedule.clear()
        logging.info("⏹️ Zamanlayıcı durduruldu")

# ---------- Zamanlama Ayarları Penceresi ----------
class ScheduleSettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, schedule_manager, on_schedule_updated):
        super().__init__(parent)
        self.schedule_manager = schedule_manager
        self.on_schedule_updated = on_schedule_updated
        
        self.title("⏰ Zamanlanmış Güncelleme Ayarları")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="Zamanlanmış Güncelleme", font=("Arial", 16, "bold")).pack(pady=15)
        
        self.enable_var = ctk.BooleanVar()
        self.enable_check = ctk.CTkCheckBox(main_frame, text="Zamanlanmış güncellemeyi aktif et",
                                           variable=self.enable_var, command=self.toggle_settings)
        self.enable_check.pack(pady=10)
        
        self.settings_frame = ctk.CTkFrame(main_frame)
        self.settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Zamanlama türü
        ctk.CTkLabel(self.settings_frame, text="Zamanlama Türü:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.schedule_type = ctk.CTkOptionMenu(self.settings_frame, values=["Günlük", "Haftalık"], command=self.toggle_day_picker)
        self.schedule_type.grid(row=0, column=1, padx=5, pady=5)
        
        # Gün seçimi
        self.day_label = ctk.CTkLabel(self.settings_frame, text="Gün:")
        self.day_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.day_of_week = ctk.CTkOptionMenu(self.settings_frame, values=["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"])
        self.day_of_week.grid(row=1, column=1, padx=5, pady=5)
        
        # Saat seçimi
        ctk.CTkLabel(self.settings_frame, text="Saat:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        time_frame = ctk.CTkFrame(self.settings_frame)
        time_frame.grid(row=2, column=1, padx=5, pady=5)
        self.hour_var = ctk.StringVar(value="14")
        self.hour_entry = ctk.CTkEntry(time_frame, textvariable=self.hour_var, width=50)
        self.hour_entry.pack(side="left")
        ctk.CTkLabel(time_frame, text=":").pack(side="left", padx=2)
        self.minute_var = ctk.StringVar(value="00")
        self.minute_entry = ctk.CTkEntry(time_frame, textvariable=self.minute_var, width=50)
        self.minute_entry.pack(side="left")

        # Durum
        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="gray", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        # Butonlar
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="✅ Kaydet", command=self.save_settings).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="❌ İptal", command=self.destroy).pack(side="left", padx=10)
    
    def load_current_settings(self):
        config = self.schedule_manager.schedule_config
        self.enable_var.set(config.get("enabled", False))
        
        type_map = {"daily": "Günlük", "weekly": "Haftalık", "monthly": "Aylık"}
        self.schedule_type.set(type_map.get(config.get("schedule_type"), "Haftalık"))
        
        day_map = {"monday": "Pazartesi", "tuesday": "Salı", "wednesday": "Çarşamba",
                   "thursday": "Perşembe", "friday": "Cuma", "saturday": "Cumartesi", "sunday": "Pazar"}
        self.day_of_week.set(day_map.get(config.get("day_of_week"), "Pazartesi"))
        
        hour, minute = config.get("time", "14:00").split(":")
        self.hour_var.set(hour)
        self.minute_var.set(minute)
        
        self.update_status_display()
        self.toggle_settings()

    def toggle_day_picker(self, choice):
        if choice == "Günlük":
            self.day_label.grid_remove()
            self.day_of_week.grid_remove()
        else:
            self.day_label.grid()
            self.day_of_week.grid()

    def toggle_settings(self):
        enabled = self.enable_var.get()
        state = "normal" if enabled else "disabled"
        
        for widget in self.settings_frame.winfo_children():
            widget.configure(state=state)
        
        self.toggle_day_picker(self.schedule_type.get())

    def update_status_display(self):
        next_run_info = self.schedule_manager.get_next_run_info()
        config = self.schedule_manager.schedule_config
        status_text = f"Sonraki çalışma: {next_run_info}\n"
        if config.get("last_run"):
            last_run = datetime.fromisoformat(config["last_run"])
            status_text += f"Son çalışma: {last_run.strftime('%d.%m.%Y %H:%M')}"
        self.status_label.configure(text=status_text)
    
    def save_settings(self):
        try:
            if not self.enable_var.get():
                self.schedule_manager.schedule_config["enabled"] = False
                self.schedule_manager.save_config()
                self.on_schedule_updated()
                self.destroy()
                return

            type_map = {"Günlük": "daily", "Haftalık": "weekly"}
            schedule_type = type_map[self.schedule_type.get()]
            
            day_map = {"Pazartesi": "monday", "Salı": "tuesday", "Çarşamba": "wednesday",
                       "Perşembe": "thursday", "Cuma": "friday", "Cumartesi": "saturday", "Pazar": "sunday"}
            day_of_week = day_map[self.day_of_week.get()]
            
            hour, minute = int(self.hour_var.get()), int(self.minute_var.get())
            if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                raise ValueError("Geçersiz saat/dakika")
            time_str = f"{hour:02d}:{minute:02d}"
            
            self.schedule_manager.set_schedule(schedule_type, day_of_week, time_str)
            self.on_schedule_updated()
            
            messagebox.showinfo("Başarılı", "Zamanlama ayarları kaydedildi!")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi: {e}")


# =============================================================================
# BÖLÜM 3: LOGLAMA VE GEÇMİŞ YÖNETİMİ (v3'ten)
# =============================================================================

# ---------- Gelişmiş Loglama Sistemi ----------
class AdvancedLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.setup_directories()
        self.logger = self.setup_logging()
        
    def setup_directories(self):
        os.makedirs(self.log_dir, exist_ok=True)
        
    def setup_logging(self):
        logger = logging.getLogger('SystemUpdater')
        if logger.hasHandlers():
            logger.handlers.clear()
            
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        log_file = os.path.join(self.log_dir, 'updater.log')
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=10, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger
        
    def log_update_start(self, update_type="manual"):
        self.logger.info(f"🔧 GÜNCELLEME BAŞLATILDI - Tip: {update_type}")
        self.logger.info(f"🖥️  Sistem: {platform.system()} {platform.release()}")
    
    def log_update_result(self, success_count, total_commands, details_list):
        rate = (success_count / total_commands * 100) if total_commands > 0 else 0
        self.logger.info(f"📊 GÜNCELLEME SONUCU - Başarı: {success_count}/{total_commands} (%{rate:.1f})")
        for detail in details_list:
            if "✅" in detail: self.logger.info(f"  {detail}")
            else: self.logger.warning(f"  {detail}")
            
    def log_error(self, msg, ctx=""): self.logger.error(f"❌ {ctx} - {msg}")
    def log_info(self, msg, ctx=""): self.logger.info(f"ℹ️  {ctx} - {msg}")

# ---------- Geçmiş Kaydı Sistemi ----------
class UpdateHistoryManager:
    def __init__(self, history_dir="history"):
        self.db_path = os.path.join(history_dir, 'update_history.db')
        os.makedirs(history_dir, exist_ok=True)
        self.setup_database()
        
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
        
    def setup_database(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS update_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
                    update_type TEXT NOT NULL, success_count INTEGER NOT NULL,
                    total_commands INTEGER NOT NULL, duration_seconds REAL NOT NULL,
                    system_info TEXT NOT NULL, status TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER,
                    command_name TEXT NOT NULL, command_text TEXT NOT NULL,
                    status TEXT NOT NULL, return_code INTEGER, output TEXT, error TEXT,
                    duration_seconds REAL, timestamp TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES update_sessions (id)
                )
            ''')
            conn.commit()
        
    def start_update_session(self, update_type="manual") -> int:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            system_info = json.dumps(PlatformDetector.get_platform_info())
            cursor.execute('''
                INSERT INTO update_sessions 
                (timestamp, update_type, success_count, total_commands, duration_seconds, system_info, status)
                VALUES (?, ?, 0, 0, 0, ?, 'running')
            ''', (datetime.now().isoformat(), update_type, system_info))
            conn.commit()
            return cursor.lastrowid
        
    def log_command_result(self, session_id: int, command_name: str, command_text: str, 
                          status: str, return_code: int, output: str, error: str, 
                          duration: float):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO command_history 
                (session_id, command_name, command_text, status, return_code, output, error, duration_seconds, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, command_name, command_text, status, return_code, 
                  output[:2000], error[:2000], duration, datetime.now().isoformat()))
            conn.commit()
        
    def complete_update_session(self, session_id: int, success_count: int, 
                               total_commands: int, duration: float, status: str = "completed"):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE update_sessions 
                SET success_count = ?, total_commands = ?, duration_seconds = ?, status = ?
                WHERE id = ?
            ''', (success_count, total_commands, duration, status, session_id))
            conn.commit()
        
    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM update_sessions ORDER BY timestamp DESC LIMIT ?', (limit,))
            sessions = [dict(row) for row in cursor.fetchall()]
            for session in sessions:
                session['system_info'] = json.loads(session['system_info'])
            return sessions
        
    def get_session_details(self, session_id: int) -> Optional[Dict]:
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM update_sessions WHERE id = ?', (session_id,))
            session_row = cursor.fetchone()
            if not session_row: return None
            
            session_info = dict(session_row)
            session_info['system_info'] = json.loads(session_info['system_info'])
            
            cursor.execute('SELECT * FROM command_history WHERE session_id = ? ORDER BY timestamp', (session_id,))
            session_info['commands'] = [dict(row) for row in cursor.fetchall()]
            return session_info

# ---------- Geçmiş Görüntüleme Penceresi ----------
class HistoryViewerWindow(ctk.CTkToplevel):
    def __init__(self, parent, history_manager: UpdateHistoryManager):
        super().__init__(parent)
        self.history_manager = history_manager
        
        self.title("📊 Güncelleme Geçmişi")
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("📋 Son Güncellemeler")
        self.tabview.add("🔍 Detaylı Görünüm")
        
        self.setup_recent_tab()
        self.setup_details_tab()
        self.load_recent_sessions()
        
    def setup_recent_tab(self):
        frame = self.tabview.tab("📋 Son Güncellemeler")
        self.session_listbox = ctk.CTkTextbox(frame, width=700, height=500)
        self.session_listbox.pack(pady=10, fill="both", expand=True)
        self.session_listbox.configure(state="disabled")
        
    def setup_details_tab(self):
        frame = self.tabview.tab("🔍 Detaylı Görünüm")
        selection_frame = ctk.CTkFrame(frame)
        selection_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(selection_frame, text="Oturum ID:").pack(side="left", padx=5)
        self.session_id_entry = ctk.CTkEntry(selection_frame, width=100)
        self.session_id_entry.pack(side="left", padx=5)
        ctk.CTkButton(selection_frame, text="Yükle", command=self.load_session_details).pack(side="left", padx=10)
        
        self.details_text = ctk.CTkTextbox(frame, width=700)
        self.details_text.pack(pady=10, fill="both", expand=True)
        self.details_text.configure(state="disabled")
        
    def load_recent_sessions(self):
        sessions = self.history_manager.get_recent_sessions(20)
        self.session_listbox.configure(state="normal")
        self.session_listbox.delete("1.0", "end")
        
        if not sessions:
            self.session_listbox.insert("end", "Henüz güncelleme geçmişi yok.\n")
        else:
            for session in sessions:
                timestamp = datetime.fromisoformat(session['timestamp']).strftime('%d.%m.%Y %H:%M')
                rate = (session['success_count'] / session['total_commands'] * 100) if session['total_commands'] > 0 else 0
                self.session_listbox.insert("end", f"ID: {session['id']} | 📅 {timestamp} | 🚀 Tip: {session['update_type']}\n")
                self.session_listbox.insert("end", f"   Başarı: {session['success_count']}/{session['total_commands']} (%{rate:.1f}) | Süre: {session['duration_seconds']:.1f}s | Durum: {session['status']}\n\n")
        
        self.session_listbox.configure(state="disabled")
        
    def load_session_details(self):
        try:
            session_id = int(self.session_id_entry.get())
            details = self.history_manager.get_session_details(session_id)
            
            if not details:
                messagebox.showerror("Hata", "Oturum bulunamadı!")
                return
                
            self.details_text.configure(state="normal")
            self.details_text.delete("1.0", "end")
            
            timestamp = datetime.fromisoformat(details['timestamp']).strftime('%d.%m.%Y %H:%M:%S')
            self.details_text.insert("end", f"📋 OTURUM DETAYLARI - ID: {session_id}\n")
            self.details_text.insert("end", f"Zaman: {timestamp} | Tip: {details['update_type']} | Durum: {details['status']}\n\n")
            
            self.details_text.insert("end", "🖥️ SİSTEM BİLGİSİ:\n")
            for key, value in details['system_info'].items():
                self.details_text.insert("end", f"   • {key.title()}: {value}\n")
            
            self.details_text.insert("end", "\n🔧 ÇALIŞTIRILAN KOMUTLAR:\n\n")
            for cmd in details['commands']:
                icon = "✅" if cmd['status'] == 'success' else "❌"
                self.details_text.insert("end", f"{icon} {cmd['command_name']} ({cmd['duration_seconds']:.1f}s) - {cmd['command_text']}\n")
                if cmd['status'] != 'success':
                    self.details_text.insert("end", f"   Hata ({cmd['return_code']}): {cmd['error'][:200]}...\n")
            
            self.details_text.configure(state="disabled")
            
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir oturum ID'si girin!")
        except Exception as e:
            messagebox.showerror("Hata", f"Detaylar yüklenemedi: {e}")


# =============================================================================
# BÖLÜM 4: PROFESYONEL ÖZELLİKLER (v4'ten)
# =============================================================================

# ---------- GÜVENLİK SİSTEMİ ----------
class SecurityManager:
    def __init__(self):
        self.key_file = "encryption.key"
        self.fernet = self._setup_encryption()
        
    def _setup_encryption(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f: key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f: f.write(key)
        return Fernet(key)
    
    def encrypt_data(self, data: str) -> str: return self.fernet.encrypt(data.encode()).decode()
    def decrypt_data(self, enc_data: str) -> str: return self.fernet.decrypt(enc_data.encode()).decode()
    
    def validate_command(self, command: list) -> bool:
        dangerous = ['rm -rf', 'format', 'del ', 'erase']
        cmd_str = ' '.join(command).lower()
        return not any(d in cmd_str for d in dangerous)

# ---------- ANİMASYONLU PROGRESS BAR ----------
class AnimatedProgressBar(ctk.CTkProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._animation_thread = None
        self._stop_animation = False
        self.current_value = 0
        self.target_value = 0
        
    def animate_to_value(self, target_value, duration=0.5):
        if self._animation_thread and self._animation_thread.is_alive():
            self._stop_animation = True
            self._animation_thread.join()
            
        self._stop_animation = False
        self.target_value = target_value
        self._animation_thread = threading.Thread(
            target=self._animation_loop, args=(duration,), daemon=True
        )
        self._animation_thread.start()
        
    def _animation_loop(self, duration):
        start_value = self.current_value
        start_time = time.time()
        
        while not self._stop_animation:
            elapsed = time.time() - start_time
            progress = min(elapsed / duration, 1.0)
            
            self.current_value = start_value + (self.target_value - start_value) * progress
            self.set(self.current_value)
            
            if progress >= 1.0: break
            time.sleep(0.016)

# ---------- SYSTEM TRAY ENTEGRASYONU ----------
class SystemTrayManager:
    def __init__(self, app_instance):
        self.app = app_instance
        self.tray_icon = None
        
    def setup_tray_icon(self):
        image = Image.new('RGB', (64, 64), color='#1e88e5')
        draw = ImageDraw.Draw(image)
        draw.text((10,10), "UP", fill="white", font=ImageDraw.load_default())
        
        menu = Menu(
            Menu.Item('Pencereyi Aç', self.show_window, default=True),
            Menu.SEPARATOR,
            Menu.Item('Hızlı Güncelle', self.quick_update),
            Menu.Item('Geçmişi Gör', lambda: self.app.show_history_viewer()),
            Menu.SEPARATOR,
            Menu.Item('Çıkış', self.exit_app)
        )
        
        self.tray_icon = pystray.Icon('system_updater', image, 'Sistem Güncelleyici', menu)
        
    def show_window(self):
        self.app.after(0, self.app.deiconify)
        self.app.after(0, self.app.lift)
            
    def quick_update(self):
        self.app.start_update(update_type="tray_quick_update")
        
    def exit_app(self):
        self.tray_icon.stop()
        self.app.cleanup_and_exit()
        
    def start_tray(self):
        if not self.tray_icon:
            self.setup_tray_icon()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

# ---------- PERFORMANS İZLEME ----------
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {'cpu': [], 'mem': []}
        self.monitoring = False
        
    def start_monitoring(self):
        self.monitoring = True
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        
    def stop_monitoring(self):
        self.monitoring = False
        
    def _monitor_loop(self):
        while self.monitoring:
            self.metrics['cpu'].append(psutil.cpu_percent(interval=None))
            self.metrics['mem'].append(psutil.virtual_memory().percent)
            self.metrics['cpu'] = self.metrics['cpu'][-100:]
            self.metrics['mem'] = self.metrics['mem'][-100:]
            time.sleep(2)
            
    def get_performance_report(self):
        cpu_avg = sum(self.metrics['cpu']) / len(self.metrics['cpu']) if self.metrics['cpu'] else 0
        mem_avg = sum(self.metrics['mem']) / len(self.metrics['mem']) if self.metrics['mem'] else 0
        return {'cpu_avg': cpu_avg, 'mem_avg': mem_avg}

# ---------- BACKUP ve ROLLBACK SİSTEMİ ----------
class BackupManager:
    def __init__(self):
        self.backup_dir = "system_backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def create_system_backup(self):
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Yedeklenecek önemli dosyaları/dizinleri buraya ekleyin
                # Örnek:
                # if os.path.exists('/etc/hosts'): zipf.write('/etc/hosts')
                pass
            logging.info(f"Yedek oluşturuldu: {backup_path}")
            return backup_path
        except Exception as e:
            logging.error(f"Backup creation error: {e}")
            return None

# ---------- CONTAINER ve VM DESTEĞİ ----------
class ContainerManager:
    def __init__(self):
        self.docker_client = None
        try:
            self.docker_client = docker.from_env(timeout=5)
            self.docker_client.ping()
            logging.info("Docker bağlantısı başarılı.")
        except Exception as e:
            logging.warning(f"Docker'a bağlanılamadı: {e}")
            
    def update_all_containers(self):
        if not self.docker_client:
            return "Docker bağlı değil", []
            
        updated_containers = []
        try:
            for container in self.docker_client.containers.list():
                try:
                    image_name = container.image.tags[0]
                    logging.info(f"{container.name} için imaj çekiliyor: {image_name}")
                    
                    old_image = self.docker_client.images.get(image_name)
                    new_image = self.docker_client.images.pull(image_name)
                    
                    if old_image.id != new_image.id:
                        logging.info(f"{container.name} yeniden oluşturuluyor...")
                        container.stop()
                        container.remove()
                        self.docker_client.containers.run(image_name, detach=True, name=container.name)
                        updated_containers.append(container.name)
                        
                except Exception as e:
                    logging.error(f"Container güncelleme hatası ({container.name}): {e}")
            
            return f"Docker güncellemesi tamamlandı. {len(updated_containers)} container güncellendi.", updated_containers
            
        except Exception as e:
            logging.error(f"Container update error: {e}")
            return f"Docker güncelleme hatası: {e}", []

# ---------- PLUGIN SİSTEMİ ----------
class PluginManager:
    def __init__(self):
        self.plugins_dir = "plugins"
        self.active_plugins = {}
        self.load_plugins()
        
    def load_plugins(self):
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
            return
            
        for filename in os.listdir(self.plugins_dir):
            if filename.endswith('.py'):
                plugin_name = filename[:-3]
                try:
                    plugin_path = os.path.join(self.plugins_dir, filename)
                    with open(plugin_path, 'r', encoding='utf-8') as f:
                        plugin_code = f.read()
                    
                    plugin_globals = {"app": app} # Ana uygulamaya erişim
                    exec(plugin_code, plugin_globals)
                    self.active_plugins[plugin_name] = plugin_globals
                    logging.info(f"Plugin yüklendi: {plugin_name}")
                except Exception as e:
                    logging.error(f"Plugin yükleme hatası {filename}: {e}")
                    
    def execute_plugin_hook(self, hook_name: str, *args, **kwargs):
        for plugin_name, plugin in self.active_plugins.items():
            if hook_name in plugin:
                try:
                    plugin[hook_name](*args, **kwargs)
                except Exception as e:
                    logging.error(f"Plugin hook hatası {plugin_name}.{hook_name}: {e}")

# ---------- WEB DASHBOARD ENTEGRASYONU ----------
class WebDashboard:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server = None
        
    def start_dashboard(self):
        class DashboardHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/api/status':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    report = app.performance_monitor.get_performance_report()
                    report['next_run'] = app.schedule_manager.get_next_run_info()
                    self.wfile.write(json.dumps(report).encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    html = "<html><body><h1>🚀 Sistem Güncelleyici Dashboard</h1></body></html>"
                    self.wfile.write(html.encode())

        self.server = HTTPServer((self.host, self.port), DashboardHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        logging.info(f"Web Dashboard http://{self.host}:{self.port} adresinde başlatıldı")
        
    def stop_dashboard(self):
        if self.server:
            self.server.shutdown()

    def open_dashboard(self):
        webbrowser.open(f'http://{self.host}:{self.port}')

# ---------- GELİŞMİŞ HATA YÖNETİMİ ----------
class ErrorHandler:
    def __init__(self, logger):
        self.error_queue = queue.Queue()
        self.logger = logger
        sys.excepthook = self.global_except_hook
        
    def global_except_hook(self, exctype, value, traceback):
        self.handle_error(value, traceback)
        sys.__excepthook__(exctype, value, traceback)
            
    def handle_error(self, error, traceback=None):
        error_msg = f"GLOBAL HATA YAKALANDI: {type(error).__name__}: {error}"
        self.logger.log_error(error_msg, "ErrorHandler")
        if isinstance(error, (MemoryError, SystemError)):
            messagebox.showerror("Kritik Hata", f"Kritik sistem hatası: {error}\nUygulama kapanabilir.")


# =============================================================================
# BÖLÜM 5: BİRLEŞTİRİLMİŞ ANA UYGULAMA
# =============================================================================

class UniversalUpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Loglama ve Hata Yönetimi (ilk başlatılanlar olmalı)
        self.logger = AdvancedLogger()
        self.error_handler = ErrorHandler(self.logger)
        
        # Diğer Tüm Yöneticiler
        self.security_manager = SecurityManager()
        self.performance_monitor = PerformanceMonitor()
        self.backup_manager = BackupManager()
        self.container_manager = ContainerManager()
        self.web_dashboard = WebDashboard()
        self.history_manager = UpdateHistoryManager()
        self.schedule_manager = ScheduledUpdateManager()
        self.package_manager = CrossPlatformPackageManager()
        
        # Pluginler (uygulama referansı için en son)
        self.plugin_manager = PluginManager() 
        
        # Sistem Tepsisi
        self.tray_manager = SystemTrayManager(self)
        
        # GUI ayarları
        self.setup_gui()
        
        # Sistemleri başlat
        self.start_systems()
        
        # Çıkış protokolü
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        
    def setup_gui(self):
        self.title("🚀 PROFESYONEL SİSTEM GÜNCELLEYİCİ v5")
        self.geometry("650x700")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        self.progress = AnimatedProgressBar(self, width=600, height=25)
        self.progress.pack(pady=20, padx=20)
        
        self.setup_status_indicators()
        self.setup_control_buttons()
        self.setup_system_info_panel()
        self.setup_log_display()
        
    def setup_status_indicators(self):
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(pady=10, fill='x', padx=20)
        
        self.cpu_label = ctk.CTkLabel(status_frame, text="CPU: --%", width=180)
        self.cpu_label.pack(side='left', padx=10, pady=5)
        
        self.memory_label = ctk.CTkLabel(status_frame, text="RAM: --%", width=180)
        self.memory_label.pack(side='left', padx=10, pady=5)
        
        self.schedule_label = ctk.CTkLabel(status_frame, text="Zamanlama: --", width=180)
        self.schedule_label.pack(side='left', padx=10, pady=5)
        
    def setup_control_buttons(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, fill='x', padx=20)
        
        buttons = [
            ("🔄 Güncelle", self.start_update),
            ("💾 Yedek Al", self.create_backup),
            ("📊 Dashboard", self.web_dashboard.open_dashboard),
            ("⏰ Zamanlama", self.show_schedule_settings),
            ("📜 Geçmiş", self.show_history_viewer),
            ("🐳 Docker", self.update_docker)
        ]
        
        for i in range(0, len(buttons), 3):
            row_frame = ctk.CTkFrame(button_frame)
            row_frame.pack(pady=5, fill='x', expand=True)
            for text, command in buttons[i:i+3]:
                btn = ctk.CTkButton(row_frame, text=text, command=command, width=180)
                btn.pack(side='left', padx=10, pady=5, expand=True)
                
    def setup_system_info_panel(self):
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(pady=10, fill='x', padx=20)
        
        self.system_info_text = ctk.CTkTextbox(info_frame, height=100)
        self.system_info_text.pack(pady=5, fill='x', padx=10, expand=True)
        self.system_info_text.insert('1.0', self.get_system_info())
        self.system_info_text.configure(state='disabled')
        
    def setup_log_display(self):
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        self.log_text = ctk.CTkTextbox(log_frame)
        self.log_text.pack(pady=5, fill='both', expand=True, padx=10)
        self.log_text.insert('1.0', "Sistem başlatıldı...\n")
        self.log_text.configure(state='disabled')
        
    def get_system_info(self):
        info = PlatformDetector.get_platform_info()
        return f"""🖥️ SİSTEM BİLGİLERİ
Platform: {info.get('distribution') or f"{info.get('system')} {info.get('release')}"}
İşlemci: {info.get('processor')}
Mimari: {info.get('architecture')} | Python: {info.get('python_version')}"""
        
    def start_systems(self):
        self.performance_monitor.start_monitoring()
        self.web_dashboard.start_dashboard()
        self.tray_manager.start_tray()
        self.schedule_manager.start_scheduler(self.start_update)
        
        self.plugin_manager.execute_plugin_hook('on_startup')
        self.start_status_updater()
        
        self.log_to_display("Tüm sistemler başlatıldı.")
        
    def start_status_updater(self):
        """Durum güncelleyiciyi başlat"""
        def update_loop():
            try:
                report = self.performance_monitor.get_performance_report()
                self.cpu_label.configure(text=f"CPU: {report['cpu_avg']:.1f}%")
                self.memory_label.configure(text=f"RAM: {report['mem_avg']:.1f}%")
                self.schedule_label.configure(text=f"Zamanlama: {self.schedule_manager.get_next_run_info()}")
            except Exception as e:
                self.logger.log_error(f"UI Güncelleme Hatası: {e}", "StatusUpdater")
            
            self.after(2000, update_loop) # 2 saniyede bir
                
        self.after(1000, update_loop)
        
    def log_to_display(self, message: str):
        """Thread-safe olarak GUI'deki log alanına yazar"""
        def _log():
            try:
                self.log_text.configure(state="normal")
                self.log_text.insert("end", f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
            except Exception as e:
                print(f"Log GUI Hatası: {e}") # GUI yok edilmişse
        
        if self.winfo_exists():
            self.after(0, _log)

    # ---------- YENİ: Grafiksel Yetki Yükseltme ----------
    def run_privileged_command(self, command: list) -> subprocess.CompletedProcess:
        """
        Platforma özgü olarak grafik arayüzde yetki isteyen bir komut çalıştırır.
        (Sadece sudo gerektiren komutlar için)
        """
        cmd_str = ' '.join(command)
        system = platform.system().lower()
        self.log_to_display(f"Yetki isteniyor: {command[1]}...")
        
        try:
            if system == 'linux':
                pkexec_cmd = ['pkexec', 'sh', '-c', cmd_str]
                return subprocess.run(pkexec_cmd, capture_output=True, text=True, timeout=600, encoding='utf-8')
            
            elif system == 'darwin':
                # AppleScript tırnak işaretlerini düzgün yönetmeli
                escaped_cmd = cmd_str.replace('"', '\\"')
                applescript = f'do shell script "{escaped_cmd}" with administrator privileges'
                osascript_cmd = ['osascript', '-e', applescript]
                return subprocess.run(osascript_cmd, capture_output=True, text=True, timeout=600, encoding='utf-8')
            
            else:
                # Windows veya beklenmeyen bir durum (sudo olmamalı)
                return subprocess.run(command, capture_output=True, text=True, timeout=600, encoding='utf-8')
                
        except FileNotFoundError:
            msg = "HATA: Yetki yükseltme aracı (pkexec/osascript) bulunamadı."
            self.log_to_display(msg)
            self.logger.log_error(msg)
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="Yetki aracı bulunamadı")
        except subprocess.TimeoutExpired:
            msg = f"HATA: Yetki istemi zaman aşımına uğradı: {cmd_str}"
            self.log_to_display(msg)
            self.logger.log_error(msg)
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="Zaman aşımı")
        except Exception as e:
            self.log_to_display(f"Yetki hatası: {e}")
            self.logger.log_error(f"Yetki hatası ({cmd_str}): {e}")
            return subprocess.CompletedProcess(command, 1, stdout="", stderr=str(e))

    # ---------- GÜNCELLENMİŞ: Ana Güncelleme İşlevi ----------
    def start_update(self, update_type="manual"):
        self.log_to_display(f"Güncelleme başlatılıyor (Tip: {update_type})...")
        self.plugin_manager.execute_plugin_hook('before_update')
        
        start_time = time.time()
        session_id = self.history_manager.start_update_session(update_type)
        
        self.progress.animate_to_value(0.05, 0.1)
        self.log_to_display(f"Yeni oturum ID: {session_id}")
        
        # Ana güncelleme işini bir thread'e ver
        threading.Thread(
            target=self._run_update_logic, 
            args=(session_id, start_time, update_type), 
            daemon=True
        ).start()
        
    def _run_update_logic(self, session_id: int, start_time: float, update_type: str):
        """Gerçek güncelleme mantığını çalıştıran thread fonksiyonu"""
        self.logger.log_update_start(update_type)
        managers = self.package_manager.get_available_managers()
        
        if not managers:
            msg = "❌ Sisteminizde desteklenen paket yöneticisi bulunamadı."
            self.log_to_display(msg)
            self.logger.log_error(msg)
            self.history_manager.complete_update_session(session_id, 0, 0, 0, "failed")
            self.progress.animate_to_value(0)
            return

        total_commands = sum(len(mgr['commands']) for mgr in managers.values())
        completed = 0
        success_count = 0
        details_list = []
        
        for manager_id, manager_info in managers.items():
            mgr_name = manager_info['name']
            for command in manager_info['commands']:
                completed += 1
                progress_val = completed / total_commands
                self.progress.animate_to_value(progress_val)
                
                cmd_str = ' '.join(command)
                self.log_to_display(f"Çalıştırılıyor [{completed}/{total_commands}]: {mgr_name} ({command[0]})")
                
                if not self.security_manager.validate_command(command):
                    msg = f"❌ GÜVENLİK: Tehlikeli komut engellendi: {cmd_str}"
                    self.log_to_display(msg)
                    self.logger.log_error(msg)
                    details_list.append(msg)
                    continue

                cmd_start_time = time.time()
                try:
                    if command[0] == 'sudo':
                        result = self.run_privileged_command(command)
                    else:
                        result = subprocess.run(command, capture_output=True, text=True, timeout=600, encoding='utf-8')
                    
                    cmd_duration = time.time() - cmd_start_time
                    
                    if result.returncode == 0:
                        success_count += 1
                        status = "success"
                        msg = f"✅ {mgr_name} - Başarılı ({cmd_duration:.1f}s)"
                        self.log_to_display(msg)
                        details_list.append(msg)
                    else:
                        status = "failed"
                        err_msg = result.stderr[:150].strip() or result.stdout[:150].strip() or "Bilinmeyen hata"
                        msg = f"❌ {mgr_name} - Hata: {err_msg}"
                        self.log_to_display(msg)
                        details_list.append(msg)
                    
                    self.history_manager.log_command_result(
                        session_id, mgr_name, cmd_str, status, result.returncode,
                        result.stdout, result.stderr, cmd_duration
                    )
                        
                except Exception as e:
                    cmd_duration = time.time() - cmd_start_time
                    msg = f"⚠️ {mgr_name} - Kritik Hata: {e}"
                    self.log_to_display(msg)
                    details_list.append(msg)
                    self.history_manager.log_command_result(
                        session_id, mgr_name, cmd_str, "error", -1, "", str(e), cmd_duration
                    )
        
        # Güncelleme tamamlandı
        total_duration = time.time() - start_time
        summary = f"🎉 Güncelleme tamamlandı! {success_count}/{total_commands} başarılı ({total_duration:.1f}s)"
        
        self.log_to_display(summary)
        self.logger.log_update_result(success_count, total_commands, details_list)
        self.history_manager.complete_update_session(
            session_id, success_count, total_commands, total_duration
        )
        self.plugin_manager.execute_plugin_hook('after_update', success=(success_count == total_commands))
        
        self.progress.animate_to_value(1.0)
        self.after(2000, lambda: self.progress.animate_to_value(0)) # 2sn sonra sıfırla
        
        self.after(0, lambda: messagebox.showinfo("Güncelleme Tamamlandı", summary))
            
    def create_backup(self):
        self.log_to_display("Yedek oluşturuluyor...")
        backup_path = self.backup_manager.create_system_backup()
        if backup_path:
            msg = f"Yedek oluşturuldu: {backup_path}"
            self.log_to_display(msg)
            messagebox.showinfo("Başarılı", msg)
        else:
            msg = "Yedek oluşturulamadı!"
            self.log_to_display(msg)
            messagebox.showerror("Hata", msg)
            
    def update_docker(self):
        self.log_to_display("Docker container'ları güncelleniyor...")
        self.progress.animate_to_value(0.5)
        
        def _docker_update():
            summary, updated = self.container_manager.update_all_containers()
            self.log_to_display(summary)
            self.progress.animate_to_value(0)
            self.after(0, lambda: messagebox.showinfo("Docker Güncellemesi", summary))
            
        threading.Thread(target=_docker_update, daemon=True).start()
        
    def show_schedule_settings(self):
        """Zamanlama ayarları penceresini açar (v2'den)"""
        ScheduleSettingsWindow(self, self.schedule_manager, self.on_schedule_updated)
    
    def on_schedule_updated(self):
        """Zamanlama ayarları değiştiğinde tetiklenir (v2'den)"""
        self.schedule_manager.stop_scheduler()
        self.schedule_manager.start_scheduler(self.start_update)
        info = self.schedule_manager.get_next_run_info()
        self.schedule_label.configure(text=f"Zamanlama: {info}")
        self.log_to_display(f"Zamanlama güncellendi. Sonraki çalışma: {info}")
    
    def show_history_viewer(self):
        """Geçmiş penceresini açar (v3'ten)"""
        HistoryViewerWindow(self, self.history_manager)
        
    def hide_to_tray(self):
        """Pencereyi gizle ve sistem tepsisine gönder"""
        self.withdraw()
        self.log_to_display("Uygulama sistem tepsisine küçültüldü.")
        
    def cleanup_and_exit(self):
        """Temizlik yap ve uygulamadan çık"""
        self.log_to_display("Uygulama kapatılıyor...")
        self.performance_monitor.stop_monitoring()
        self.schedule_manager.stop_scheduler()
        self.web_dashboard.stop_dashboard()
        self.plugin_manager.execute_plugin_hook('on_shutdown')
        self_logger = self.logger.logger # logger referansını al
        
        # Handler'ları kaldır (dosya kilidini serbest bırakmak için)
        handlers = self_logger.handlers[:]
        for handler in handlers:
            handler.close()
            self_logger.removeHandler(handler)
            
        self.destroy()
        sys.exit(0)

# =============================================================================
# BÖLÜM 6: UYGULAMAYI BAŞLAT
# =============================================================================

if __name__ == "__main__":
    # Windows'ta konsol penceresini gizle
    if platform.system().lower() == 'windows':
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass # GUI olmayan bir ortamda çalışıyorsa
            
    app = UniversalUpdaterApp()
    
    # PluginManager'a uygulama referansını ekle
    # (Plugin'lerin 'app' global değişkenine erişebilmesi için)
    for plugin in app.plugin_manager.active_plugins.values():
        plugin['app'] = app
        
    app.mainloop()
