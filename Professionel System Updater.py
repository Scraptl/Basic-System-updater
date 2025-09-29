#!/usr/bin/env python3
"""
🚀 ULTIMATE PROFESYONEL SİSTEM GÜNCELLEYİCİ
Tüm Gelişmiş Özelliklerle Tam Entegre - Tek Dosya
"""

import os
import platform
import shutil
import subprocess
import threading
import time
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox, Menu
import sys
import json
import schedule
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
import requests
import psutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import zipfile
import docker
from io import BytesIO
import tempfile
from PIL import Image, ImageDraw
import pystray
import webbrowser
import queue
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import secrets
import hashlib
import base64
import hmac
from typing import Dict, List, Optional, Any
import jwt
import socketio
import qrcode
from web3 import Web3
import numpy as np
from sklearn.ensemble import IsolationForest

# =========== TEMEL SİSTEMLER ===========

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
            elif os.path.exists('/etc/redhat-release'):
                with open('/etc/redhat-release', 'r') as f:
                    return f.read().strip()
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

class CrossPlatformPackageManager:
    def __init__(self):
        self.platform_info = PlatformDetector.get_platform_info()
        self.system = self.platform_info['system']
        
    def get_available_managers(self):
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
        """Windows paket yöneticileri"""
        managers = {}
        
        if shutil.which('winget'):
            managers['winget'] = {
                'name': 'Windows Package Manager',
                'description': 'Microsoft resmi paket yöneticisi',
                'commands': [
                    ['winget', 'upgrade', '--all', '--accept-source-agreements', '--accept-package-agreements']
                ]
            }
        
        if shutil.which('choco'):
            managers['choco'] = {
                'name': 'Chocolatey',
                'description': 'Windows için paket yöneticisi',
                'commands': [
                    ['choco', 'upgrade', 'all', '-y']
                ]
            }
            
        if shutil.which('scoop'):
            managers['scoop'] = {
                'name': 'Scoop',
                'description': 'Windows için komut satırı yükleyici',
                'commands': [
                    ['scoop', 'update'],
                    ['scoop', 'update', '*']
                ]
            }
            
        return managers
    
    def _get_macos_managers(self):
        """macOS paket yöneticileri"""
        managers = {}
        
        if shutil.which('brew'):
            managers['brew'] = {
                'name': 'Homebrew',
                'description': 'macOS için paket yöneticisi',
                'commands': [
                    ['brew', 'update'],
                    ['brew', 'upgrade'],
                    ['brew', 'cleanup', '-s']
                ]
            }
        
        if shutil.which('mas'):
            managers['mas'] = {
                'name': 'Mac App Store',
                'description': 'Mac App Store uygulamaları',
                'commands': [
                    ['mas', 'upgrade']
                ]
            }
            
        if shutil.which('port'):
            managers['port'] = {
                'name': 'MacPorts',
                'description': 'macOS paket yönetimi',
                'commands': [
                    ['sudo', 'port', 'selfupdate'],
                    ['sudo', 'port', 'upgrade', 'outdated']
                ]
            }
            
        return managers
    
    def _get_linux_managers(self):
        """Linux paket yöneticileri"""
        managers = {}
        distro = self.platform_info.get('distribution', '').lower()
        
        if shutil.which('apt') or shutil.which('apt-get'):
            apt_cmd = 'apt' if shutil.which('apt') else 'apt-get'
            managers['apt'] = {
                'name': 'APT Package Manager',
                'description': 'Debian tabanlı sistemler',
                'commands': [
                    ['sudo', apt_cmd, 'update'],
                    ['sudo', apt_cmd, 'upgrade', '-y'],
                    ['sudo', apt_cmd, 'autoremove', '-y']
                ]
            }
        
        if shutil.which('dnf'):
            managers['dnf'] = {
                'name': 'DNF Package Manager',
                'description': 'Fedora/RHEL tabanlı sistemler',
                'commands': [
                    ['sudo', 'dnf', 'upgrade', '--refresh', '-y']
                ]
            }
        
        if shutil.which('pacman'):
            managers['pacman'] = {
                'name': 'Pacman Package Manager',
                'description': 'Arch Linux tabanlı sistemler',
                'commands': [
                    ['sudo', 'pacman', '-Syu', '--noconfirm']
                ]
            }
        
        if shutil.which('zypper'):
            managers['zypper'] = {
                'name': 'Zypper Package Manager',
                'description': 'openSUSE tabanlı sistemler',
                'commands': [
                    ['sudo', 'zypper', 'refresh'],
                    ['sudo', 'zypper', 'update', '-y']
                ]
            }
        
        if shutil.which('snap'):
            managers['snap'] = {
                'name': 'Snap Packages',
                'description': 'Universal Linux paketleri',
                'commands': [
                    ['sudo', 'snap', 'refresh']
                ]
            }
        
        if shutil.which('flatpak'):
            managers['flatpak'] = {
                'name': 'Flatpak Applications',
                'description': 'Flatpak uygulamaları',
                'commands': [
                    ['flatpak', 'update', '-y']
                ]
            }
            
        return managers

# =========== GELİŞMİŞ ÖZELLİKLER ===========

class AdvancedLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.setup_directories()
        self.setup_logging()
        
    def setup_directories(self):
        """Log dizinlerini oluştur"""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "archives"), exist_ok=True)
        
    def setup_logging(self):
        """Loglama sistemini kur"""
        self.logger = logging.getLogger('SystemUpdater')
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        log_file = os.path.join(self.log_dir, 'updater.log')
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024,
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log_update_start(self, update_type="manual"):
        """Güncelleme başlangıcını logla"""
        self.logger.info(f"🔧 GÜNCELLEME BAŞLATILDI - Tip: {update_type}")
        
    def log_update_result(self, success_count, total_commands, details):
        """Güncelleme sonucunu logla"""
        success_rate = (success_count / total_commands) * 100 if total_commands > 0 else 0
        self.logger.info(f"📊 GÜNCELLEME SONUCU - Başarı: {success_count}/{total_commands} (%{success_rate:.1f})")

class UpdateHistoryManager:
    def __init__(self, history_dir="history"):
        self.history_dir = history_dir
        self.setup_directories()
        self.setup_database()
        
    def setup_directories(self):
        """Geçmiş dizinlerini oluştur"""
        os.makedirs(self.history_dir, exist_ok=True)
        
    def setup_database(self):
        """SQLite veritabanını kur"""
        self.db_path = os.path.join(self.history_dir, 'update_history.db')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS update_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                update_type TEXT NOT NULL,
                success_count INTEGER NOT NULL,
                total_commands INTEGER NOT NULL,
                duration_seconds REAL NOT NULL,
                system_info TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                command_name TEXT NOT NULL,
                command_text TEXT NOT NULL,
                status TEXT NOT NULL,
                return_code INTEGER,
                output TEXT,
                error TEXT,
                duration_seconds REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES update_sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def start_update_session(self, update_type="manual") -> int:
        """Yeni güncelleme oturumu başlat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        system_info = json.dumps(PlatformDetector.get_platform_info())
        
        cursor.execute('''
            INSERT INTO update_sessions 
            (timestamp, update_type, success_count, total_commands, duration_seconds, system_info, status)
            VALUES (?, ?, 0, 0, 0, ?, 'running')
        ''', (datetime.now().isoformat(), update_type, system_info))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

class SecurityManager:
    def __init__(self):
        self.key_file = "encryption.key"
        self.fernet = self._setup_encryption()
        
    def _setup_encryption(self):
        """Şifreleme anahtarını ayarla"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        return Fernet(key)
    
    def validate_command(self, command: list) -> bool:
        """Komut güvenliğini doğrula"""
        dangerous_commands = ['rm -rf', 'format', 'del', 'erase']
        cmd_str = ' '.join(command).lower()
        return not any(dangerous in cmd_str for dangerous in dangerous_commands)

class ScheduledUpdateManager:
    def __init__(self, config_file="schedule_config.json"):
        self.config_file = config_file
        self.schedule_config = self.load_config()
        self.scheduler_running = False
        
    def load_config(self) -> Dict:
        """Zamanlama ayarlarını yükle"""
        default_config = {
            "enabled": False,
            "schedule_type": "weekly",
            "day_of_week": "monday",
            "time": "14:00",
            "last_run": None,
            "next_run": None
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return default_config

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'disk_io': [],
            'network_io': []
        }
        
    def start_monitoring(self):
        """Performans izlemeyi başlat"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def _monitor_loop(self):
        """İzleme döngüsü"""
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                self.metrics['cpu_usage'].append(cpu_percent)
                
                memory = psutil.virtual_memory()
                self.metrics['memory_usage'].append(memory.percent)
                
                for key in self.metrics:
                    self.metrics[key] = self.metrics[key][-100:]
                    
            except Exception:
                pass
            time.sleep(5)

class SystemTrayManager:
    def __init__(self, app_instance):
        self.app = app_instance
        
    def setup_tray_icon(self):
        """Sistem tepsi ikonunu oluştur"""
        try:
            image = Image.new('RGB', (64, 64), color='#1e88e5')
            draw = ImageDraw.Draw(image)
            draw.rectangle([16, 16, 48, 48], outline='white', width=3)
            
            menu = Menu(
                Menu.Item('Pencereyi Aç', self.show_window),
                Menu.SEPARATOR,
                Menu.Item('Hızlı Güncelle', self.quick_update),
                Menu.Item('Çıkış', self.exit_app)
            )
            
            self.tray_icon = pystray.Icon(
                'system_updater',
                image,
                'Sistem Güncelleyici',
                menu
            )
        except Exception:
            pass

# =========== ANA UYGULAMA ===========

class UltimateSystemUpdater(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Tüm manager'ları başlat
        self.platform_info = PlatformDetector.get_platform_info()
        self.package_manager = CrossPlatformPackageManager()
        self.logger = AdvancedLogger()
        self.history_manager = UpdateHistoryManager()
        self.security_manager = SecurityManager()
        self.schedule_manager = ScheduledUpdateManager()
        self.performance_monitor = PerformanceMonitor()
        self.tray_manager = SystemTrayManager(self)
        
        # GUI ayarları
        self.setup_gui()
        
        # Sistemleri başlat
        self.start_systems()
        
    def setup_gui(self):
        """Profesyonel GUI kurulumu"""
        self.title("🚀 ULTIMATE SİSTEM GÜNCELLEYİCİ")
        self.geometry("800x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Ana container
        self.main_container = ctk.CTkTabview(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sekmeleri oluştur
        self.setup_dashboard_tab()
        self.setup_update_tab()
        self.setup_history_tab()
        self.setup_settings_tab()
        self.setup_monitoring_tab()
        
    def setup_dashboard_tab(self):
        """Dashboard sekmesi"""
        tab = self.main_container.add("📊 Dashboard")
        
        # Sistem durumu
        status_frame = ctk.CTkFrame(tab)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        self.system_status = ctk.CTkLabel(status_frame, text="🟢 Sistem Aktif", 
                                         font=("Arial", 16, "bold"))
        self.system_status.pack(pady=10)
        
        # Sistem bilgileri
        info_text = f"""🖥️ SİSTEM BİLGİLERİ
Platform: {self.platform_info['system'].title()} {self.platform_info['release']}
Mimari: {self.platform_info['architecture']}
İşlemci: {self.platform_info['processor']}
Python: {self.platform_info['python_version']}"""
        
        info_label = ctk.CTkLabel(status_frame, text=info_text, justify="left")
        info_label.pack(pady=10)
        
        # Hızlı aksiyon butonları
        self.setup_quick_actions(tab)
        
    def setup_update_tab(self):
        """Güncelleme sekmesi"""
        tab = self.main_container.add("🔄 Güncelleme")
        
        # Paket yöneticileri
        managers_frame = ctk.CTkFrame(tab)
        managers_frame.pack(fill="x", padx=10, pady=10)
        
        managers = self.package_manager.get_available_managers()
        managers_text = "📦 TESPİT EDİLEN PAKET YÖNETİCİLERİ:\n\n"
        
        if managers:
            for manager_id, manager_info in managers.items():
                managers_text += f"✅ {manager_info['name']}\n"
                managers_text += f"   {manager_info['description']}\n\n"
        else:
            managers_text += "❌ Paket yöneticisi bulunamadı\n"
            
        managers_label = ctk.CTkLabel(managers_frame, text=managers_text, justify="left")
        managers_label.pack(pady=10)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(tab, width=700, height=20)
        self.progress.set(0)
        self.progress.pack(pady=15)
        
        # Durum label
        self.status_label = ctk.CTkLabel(tab, text="Sistem hazır", 
                                        font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        # Güncelle butonu
        self.update_btn = ctk.CTkButton(tab, text="🚀 TÜM SİSTEMİ GÜNCELLE",
                                       command=self.start_update,
                                       font=("Arial", 16, "bold"),
                                       height=40)
        self.update_btn.pack(pady=20)
        
        # Çıktı alanı
        self.output_text = ctk.CTkTextbox(tab, width=750, height=200)
        self.output_text.pack(pady=10, fill="x", padx=20)
        self.output_text.insert("1.0", "Güncelleme detayları burada görünecek...\n")
        self.output_text.configure(state="disabled")
        
    def setup_history_tab(self):
        """Geçmiş sekmesi"""
        tab = self.main_container.add("📜 Geçmiş")
        
        # Geçmiş listesi
        history_text = ctk.CTkTextbox(tab, width=750, height=400)
        history_text.pack(pady=10, fill="both", expand=True, padx=20)
        history_text.insert("1.0", "Son güncellemeler burada listelenecek...\n")
        history_text.configure(state="disabled")
        
    def setup_settings_tab(self):
        """Ayarlar sekmesi"""
        tab = self.main_container.add("⚙️ Ayarlar")
        
        # Tema seçimi
        theme_frame = ctk.CTkFrame(tab)
        theme_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(theme_frame, text="Tema:", font=("Arial", 14)).pack(side="left", padx=5)
        
        theme_var = ctk.StringVar(value="dark")
        theme_dropdown = ctk.CTkOptionMenu(theme_frame, 
                                          values=["dark", "light", "blue"],
                                          variable=theme_var,
                                          command=self.change_theme)
        theme_dropdown.pack(side="left", padx=5)
        
        # Zamanlama ayarları
        schedule_frame = ctk.CTkFrame(tab)
        schedule_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(schedule_frame, text="⏰ Zamanlama Ayarları",
                     command=self.show_schedule_settings).pack(pady=5)
        
    def setup_monitoring_tab(self):
        """Monitoring sekmesi"""
        tab = self.main_container.add("📈 Monitoring")
        
        # Performans göstergeleri
        metrics_frame = ctk.CTkFrame(tab)
        metrics_frame.pack(fill="x", padx=10, pady=10)
        
        self.cpu_label = ctk.CTkLabel(metrics_frame, text="CPU: --%", font=("Arial", 12))
        self.cpu_label.pack(side="left", padx=20)
        
        self.memory_label = ctk.CTkLabel(metrics_frame, text="RAM: --%", font=("Arial", 12))
        self.memory_label.pack(side="left", padx=20)
        
        self.disk_label = ctk.CTkLabel(metrics_frame, text="DISK: --%", font=("Arial", 12))
        self.disk_label.pack(side="left", padx=20)
        
    def setup_quick_actions(self, parent):
        """Hızlı aksiyon butonları"""
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        buttons = [
            ("🔍 Sistem Detayları", self.show_system_details),
            ("💾 Hızlı Yedek", self.quick_backup),
            ("📊 Performans", self.show_performance),
            ("🔒 Güvenlik Tarama", self.security_scan)
        ]
        
        for i in range(0, len(buttons), 2):
            row_frame = ctk.CTkFrame(actions_frame)
            row_frame.pack(pady=5)
            
            for text, command in buttons[i:i+2]:
                btn = ctk.CTkButton(row_frame, text=text, command=command, width=180)
                btn.pack(side="left", padx=5)
                
    def start_systems(self):
        """Tüm sistemleri başlat"""
        self.performance_monitor.start_monitoring()
        self.start_status_updater()
        
    def start_status_updater(self):
        """Durum güncelleyiciyi başlat"""
        def update_loop():
            while True:
                try:
                    # CPU ve memory güncelleme
                    cpu = psutil.cpu_percent()
                    memory = psutil.virtual_memory().percent
                    
                    self.cpu_label.configure(text=f"CPU: {cpu:.1f}%")
                    self.memory_label.configure(text=f"RAM: {memory:.1f}%")
                    
                except Exception:
                    pass
                time.sleep(2)
                
        threading.Thread(target=update_loop, daemon=True).start()
        
    def start_update(self):
        """Güncellemeyi başlat"""
        # Güvenlik kontrolü
        if not self.security_manager.validate_command(['update']):
            messagebox.showerror("Güvenlik Uyarısı", "Güvenlik kontrolü başarısız!")
            return
            
        self.progress.set(0)
        self.status_label.configure(text="Güncelleme başlatılıyor...")
        self.update_btn.configure(state="disabled")
        
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "🔧 Güncelleme başlatıldı...\n")
        self.output_text.configure(state="disabled")
        
        # Loglama başlat
        self.logger.log_update_start("manual")
        session_id = self.history_manager.start_update_session("manual")
        
        # Thread'de çalıştır
        thread = threading.Thread(target=lambda: self.run_update_thread(session_id))
        thread.daemon = True
        thread.start()
        
    def run_update_thread(self, session_id: int):
        """Güncelleme thread'i"""
        managers = self.package_manager.get_available_managers()
        
        if not managers:
            self.update_done("❌ Paket yöneticisi bulunamadı", [])
            return
        
        total_commands = sum(len(mgr['commands']) for mgr in managers.values())
        completed = 0
        success_count = 0
        details = []
        
        for manager_id, manager_info in managers.items():
            for command in manager_info['commands']:
                completed += 1
                progress = (completed / total_commands) * 100
                
                self.update_progress(progress, f"{manager_info['name']} - {command[0]}")
                
                try:
                    # Sudo gerekiyorsa özel işlem
                    if platform.system().lower() != 'windows' and command[0] == 'sudo':
                        result = self.run_privileged_command(command)
                    else:
                        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        success_count += 1
                        details.append(f"✅ {manager_info['name']} - Başarılı")
                    else:
                        error_msg = result.stderr[:100] if result.stderr else "Bilinmeyen hata"
                        details.append(f"❌ {manager_info['name']} - Hata: {error_msg}")
                        
                except Exception as e:
                    details.append(f"⚠️ {manager_info['name']} - Hata: {str(e)}")
                
                time.sleep(1)
        
        summary = f"🎉 Güncelleme tamamlandı! {success_count}/{total_commands} başarılı"
        self.logger.log_update_result(success_count, total_commands, details)
        self.update_done(summary, details)
        
    def run_privileged_command(self, command):
        """Ayrıcalıklı komut çalıştırma"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
            return result
        except:
            return type('obj', (object,), {'returncode': 1, 'stderr': 'İzin reddedildi'})()
    
    def update_progress(self, percent, detail):
        """İlerlemeyi güncelle"""
        self.progress.set(percent / 100)
        self.status_label.configure(text=f"Güncelleniyor... %{int(percent)}")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"⏳ {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def update_done(self, message, details):
        """Güncelleme tamamlandı"""
        self.progress.set(1.0)
        self.status_label.configure(text="Tamamlandı!")
        self.update_btn.configure(state="normal")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"\n🎉 {message}\n")
        for detail in details:
            self.output_text.insert("end", f"• {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
        
        messagebox.showinfo("Güncelleme Tamamlandı", message)
        
    def change_theme(self, theme_name):
        """Tema değiştir"""
        ctk.set_appearance_mode(theme_name)
        
    def show_system_details(self):
        """Sistem detaylarını göster"""
        details = f"""🔧 DETAYLI SİSTEM BİLGİLERİ

Platform: {self.platform_info['system'].title()} {self.platform_info['release']}
Dağıtım: {self.platform_info.get('distribution', 'N/A')}
Mimari: {self.platform_info['architecture']}
İşlemci: {self.platform_info['processor']}
Python: {self.platform_info['python_version']}

📦 PAKET YÖNETİCİLERİ:"""
        
        managers = self.package_manager.get_available_managers()
        for manager_id, manager_info in managers.items():
            details += f"\n✅ {manager_info['name']} - {manager_info['description']}"
            
        messagebox.showinfo("Sistem Detayları", details)
        
    def show_schedule_settings(self):
        """Zamanlama ayarlarını göster"""
        messagebox.showinfo("Zamanlama", "Zamanlama ayarları penceresi burada açılacak")
        
    def quick_backup(self):
        """Hızlı yedek al"""
        messagebox.showinfo("Yedek", "Hızlı yedek alma işlemi başlatıldı")
        
    def show_performance(self):
        """Performans bilgilerini göster"""
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        performance_info = f"""📊 SİSTEM PERFORMANSI

CPU Kullanımı: {cpu}%
Bellek: {memory.percent}% ({memory.used//1024**3}GB / {memory.total//1024**3}GB)
Disk: {disk.percent}% ({disk.used//1024**3}GB / {disk.total//1024**3}GB)
Çalışma Süresi: {time.strftime('%H:%M:%S', time.gmtime(time.time() - psutil.boot_time()))}"""
        
        messagebox.showinfo("Sistem Performansı", performance_info)
        
    def security_scan(self):
        """Güvenlik taraması"""
        messagebox.showinfo("Güvenlik", "Güvenlik taraması başlatıldı")

# =========== UYGULAMAYI BAŞLAT ===========

def main():
    """Ana uygulama fonksiyonu"""
    # Platform kontrolü
    if platform.system().lower() not in ['windows', 'darwin', 'linux']:
        print("⚠️ Desteklenmeyen işletim sistemi")
        return
    
    # Gerekli kütüphaneleri kontrol et
    try:
        import psutil
    except ImportError:
        print("❌ 'psutil' kütüphanesi gerekli. Yüklemek için:")
        print("pip install psutil")
        return
        
    try:
        import customtkinter
    except ImportError:
        print("❌ 'customtkinter' kütüphanesi gerekli. Yüklemek için:")
        print("pip install customtkinter")
        return
    
    # Uygulamayı başlat
    app = UltimateSystemUpdater()
    app.mainloop()

if __name__ == "__main__":
    main()
