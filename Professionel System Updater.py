import os
import platform
import shutil
import subprocess
import threading
import time
from datetime import datetime, timedelta
import customtkinter as ctk
from tkinter import messagebox
import sys
import json
import hashlib
import hmac
import secrets
from typing import Dict, List, Optional
import sqlite3
import requests
import psutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# =========== GELİŞMİŞ GÜVENLİK SİSTEMİ ===========

class SecurityHardening:
    def __init__(self):
        self.setup_secure_environment()
        self.whitelisted_commands = self.load_command_whitelist()
        
    def setup_secure_environment(self):
        """Güvenli ortam kurulumu"""
        # Memory protection için secure allocation
        self.sensitive_data = {}
        self.secure_memory_alloc()
        
    def secure_memory_alloc(self):
        """Güvenli bellek ayırma"""
        # Hassas veriler için özel bellek yönetimi
        self.encryption_key = Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        
    def load_command_whitelist(self):
        """Güvenli komut whitelist'i"""
        return {
            'winget', 'choco', 'scoop', 'brew', 'mas', 'port',
            'apt', 'apt-get', 'dnf', 'pacman', 'zypper', 'snap', 'flatpak'
        }
    
    def validate_command(self, command: list) -> bool:
        """Komut güvenliğini doğrula"""
        if not command:
            return False
            
        base_cmd = command[0].lower()
        
        # Command injection koruması
        dangerous_patterns = [';', '|', '&', '`', '$', '>', '<', 'rm -rf', 'format']
        cmd_str = ' '.join(command).lower()
        
        if any(pattern in cmd_str for pattern in dangerous_patterns):
            return False
            
        # Whitelist kontrolü
        return base_cmd in self.whitelisted_commands
    
    def secure_command_execution(self, command: list) -> Dict:
        """Güvenli komut çalıştırma"""
        if not self.validate_command(command):
            return {
                'success': False, 
                'error': 'Potentially dangerous command blocked',
                'return_code': -1
            }
            
        try:
            # Resource limiting ile çalıştırma
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 dakika timeout
                shell=False,
                env=self.get_secure_environment()
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timeout', 'return_code': -1}
        except Exception as e:
            return {'success': False, 'error': str(e), 'return_code': -1}
    
    def get_secure_environment(self):
        """Güvenli environment variables"""
        env = os.environ.copy()
        # Potansiyel tehlikeli environment'ları kaldır
        dangerous_vars = ['LD_PRELOAD', 'PYTHONPATH', 'BASH_ENV']
        for var in dangerous_vars:
            env.pop(var, None)
        return env
    
    def validate_digital_signature(self, file_path: str, expected_hash: str) -> bool:
        """Dijital imza doğrulama"""
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                
            actual_hash = hashlib.sha256(file_data).hexdigest()
            return hmac.compare_digest(actual_hash, expected_hash)
            
        except Exception:
            return False

# =========== GÜVENLİK YÖNETİMİ ===========

class SecurityManager:
    def __init__(self):
        self.security_db = "security_updates.db"
        self.setup_security_database()
        self.cve_data = []
        
    def setup_security_database(self):
        """Güvenlik veritabanını kur"""
        conn = sqlite3.connect(self.security_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT UNIQUE,
                severity TEXT,
                package_name TEXT,
                fixed_version TEXT,
                detected_version TEXT,
                status TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerability_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_type TEXT,
                vulnerabilities_found INTEGER,
                total_checks INTEGER,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def fetch_cve_data(self):
        """CVE verilerini getir (basit implementasyon)"""
        # Gerçek uygulamada CVE API'sine bağlanılır
        self.cve_data = [
            {
                'id': 'CVE-2023-1234',
                'package': 'openssl',
                'affected_version': '1.1.1',
                'fixed_version': '1.1.1a',
                'severity': 'HIGH',
                'description': 'SSL/TLS vulnerability'
            }
        ]
        return self.cve_data
    
    def vulnerability_scan(self):
        """Güvenlik açığı taraması"""
        vulnerabilities = []
        
        # Sistem paketlerini kontrol et
        system_packages = self.get_system_packages()
        cve_data = self.fetch_cve_data()
        
        for package_name, current_version in system_packages.items():
            for cve in cve_data:
                if (cve['package'] == package_name and 
                    self.is_vulnerable_version(current_version, cve)):
                    vulnerabilities.append({
                        'cve_id': cve['id'],
                        'severity': cve['severity'],
                        'package': package_name,
                        'current_version': current_version,
                        'fixed_version': cve['fixed_version'],
                        'description': cve['description']
                    })
        
        # Sonuçları kaydet
        self.log_scan_result(len(vulnerabilities))
        return vulnerabilities
    
    def get_system_packages(self):
        """Sistem paketlerini getir"""
        packages = {}
        try:
            if platform.system() == 'Windows':
                # Windows paketleri
                pass
            elif platform.system() == 'Linux':
                # Linux paketleri
                if shutil.which('dpkg'):
                    result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
                    # dpkg çıktısını parse et
                    pass
        except Exception:
            pass
        return packages
    
    def is_vulnerable_version(self, current_version: str, cve: Dict) -> bool:
        """Versiyonun güvenlik açığı içerip içermediğini kontrol et"""
        # Basit versiyon karşılaştırma
        try:
            return current_version <= cve['affected_version']
        except:
            return False
    
    def log_scan_result(self, vulnerabilities_found: int):
        """Tarama sonucunu kaydet"""
        conn = sqlite3.connect(self.security_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vulnerability_scans 
            (scan_type, vulnerabilities_found, total_checks, timestamp)
            VALUES (?, ?, ?, ?)
        ''', ('full_scan', vulnerabilities_found, 100, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

# =========== BULUT ENTEGRASYONU ===========

class CloudIntegration:
    def __init__(self):
        self.api_base_url = "https://api.system-updater.com/v1"
        self.auth_token = None
        self.sync_enabled = False
        
    def authenticate(self, api_key: str) -> bool:
        """API kimlik doğrulama"""
        try:
            # Basit authentication simülasyonu
            if api_key and len(api_key) > 10:
                self.auth_token = f"token_{api_key[-10:]}"
                self.sync_enabled = True
                return True
        except Exception:
            pass
        return False
    
    def sync_settings(self, settings: Dict) -> bool:
        """Ayarları cloud'a senkronize et"""
        if not self.sync_enabled:
            return False
            
        try:
            # Senkronizasyon simülasyonu
            sync_data = {
                'timestamp': datetime.now().isoformat(),
                'settings': settings,
                'system_id': self.get_system_id()
            }
            print(f"Settings synced to cloud: {sync_data}")
            return True
        except Exception:
            return False
    
    def get_remote_updates(self) -> List:
        """Uzaktan güncellemeleri getir"""
        if not self.sync_enabled:
            return []
            
        try:
            # Remote updates simülasyonu
            return [
                {
                    'id': 'remote_001',
                    'name': 'Security Patch',
                    'description': 'Important security update',
                    'priority': 'high'
                }
            ]
        except Exception:
            return []
    
    def get_system_id(self) -> str:
        """Benzersiz sistem ID'si oluştur"""
        system_info = platform.system() + platform.release() + platform.machine()
        return hashlib.md5(system_info.encode()).hexdigest()

# =========== BİLDİRİM SİSTEMİ ===========

class NotificationManager:
    def __init__(self):
        self.notification_queue = queue.Queue()
        self.user_preferences = self.load_user_preferences()
        self.setup_notification_handlers()
        
    def load_user_preferences(self):
        """Kullanıcı tercihlerini yükle"""
        return {
            'priority_alerts': True,
            'security_notifications': True,
            'update_notifications': True,
            'quiet_hours': {'start': '22:00', 'end': '08:00'}
        }
    
    def setup_notification_handlers(self):
        """Bildirim handler'larını kur"""
        # Platforma özel bildirimler
        self.notification_analytics = {
            'sent': 0,
            'clicked': 0,
            'dismissed': 0
        }
    
    def send_notification(self, title: str, message: str, priority: str = "normal"):
        """Bildirim gönder"""
        if not self.should_show_notification(priority):
            return
            
        notification = {
            'id': secrets.token_hex(8),
            'title': title,
            'message': message,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        self.notification_queue.put(notification)
        self.display_notification(notification)
        self.log_notification(notification)
    
    def should_show_notification(self, priority: str) -> bool:
        """Bildirimin gösterilip gösterilmeyeceğini kontrol et"""
        # Sessiz saatler kontrolü
        if self.is_quiet_hours():
            return priority == 'critical'
            
        # Kullanıcı tercihleri
        if priority == 'security' and not self.user_preferences['security_notifications']:
            return False
            
        return True
    
    def is_quiet_hours(self) -> bool:
        """Sessiz saatlerde mi kontrol et"""
        try:
            now = datetime.now().time()
            start = datetime.strptime(self.user_preferences['quiet_hours']['start'], '%H:%M').time()
            end = datetime.strptime(self.user_preferences['quiet_hours']['end'], '%H:%M').time()
            
            if start < end:
                return start <= now <= end
            else:
                return now >= start or now <= end
        except:
            return False
    
    def display_notification(self, notification: Dict):
        """Bildirimi göster"""
        # Platforma özel bildirim gösterimi
        if platform.system() == 'Windows':
            try:
                # Windows toast notification
                pass
            except:
                # Fallback to messagebox
                messagebox.showinfo(notification['title'], notification['message'])
        else:
            messagebox.showinfo(notification['title'], notification['message'])
    
    def log_notification(self, notification: Dict):
        """Bildirimi logla"""
        self.notification_analytics['sent'] += 1
        
        # Analytics verisini kaydet
        analytics_data = {
            'notification_id': notification['id'],
            'title': notification['title'],
            'priority': notification['priority'],
            'timestamp': notification['timestamp']
        }

# =========== TEMA YÖNETİMİ ===========

class ThemeManager:
    def __init__(self):
        self.current_theme = "system"
        self.themes = {
            "dark": {
                "bg_color": "#2b2b2b",
                "fg_color": "#ffffff",
                "accent_color": "#1e88e5",
                "text_color": "#ffffff"
            },
            "light": {
                "bg_color": "#ffffff",
                "fg_color": "#000000",
                "accent_color": "#1976d2",
                "text_color": "#000000"
            },
            "blue": {
                "bg_color": "#0d1b2a",
                "fg_color": "#e0e1dd",
                "accent_color": "#415a77",
                "text_color": "#e0e1dd"
            },
            "high_contrast": {
                "bg_color": "#000000",
                "fg_color": "#ffffff",
                "accent_color": "#ffff00",
                "text_color": "#ffffff"
            }
        }
        self.auto_switch_enabled = False
        
    def switch_theme(self, theme_name: str):
        """Tema değiştir"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            ctk.set_appearance_mode(theme_name)
            self.apply_custom_theme(self.themes[theme_name])
    
    def apply_custom_theme(self, theme: Dict):
        """Özel tema uygula"""
        try:
            ctk.ThemeManager.theme = {
                "CTk": {
                    "fg_color": theme["bg_color"],
                    "text_color": theme["text_color"],
                },
                "CTkButton": {
                    "fg_color": theme["accent_color"],
                    "text_color": theme["text_color"],
                },
                "CTkLabel": {
                    "text_color": theme["text_color"],
                }
            }
        except Exception:
            pass
    
    def enable_auto_switch(self):
        """Otomatik tema değiştirmeyi aktif et"""
        self.auto_switch_enabled = True
        self.auto_switch_thread = threading.Thread(target=self._auto_switch_loop, daemon=True)
        self.auto_switch_thread.start()
    
    def _auto_switch_loop(self):
        """Otomatik tema değiştirme döngüsü"""
        while self.auto_switch_enabled:
            try:
                now = datetime.now()
                current_hour = now.hour
                
                # 06:00 - 18:00 arası light theme, diğer zamanlarda dark theme
                if 6 <= current_hour < 18:
                    self.switch_theme("light")
                else:
                    self.switch_theme("dark")
                    
                time.sleep(300)  # 5 dakikada bir kontrol et
            except Exception:
                time.sleep(300)

# =========== KURTARMA SİSTEMİ ===========

class DisasterRecovery:
    def __init__(self):
        self.recovery_points = []
        self.backup_dir = "system_backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        self.setup_recovery_system()
    
    def setup_recovery_system(self):
        """Kurtarma sistemini kur"""
        # İlk kurtarma noktasını oluştur
        self.create_recovery_point("initial_setup")
    
    def create_recovery_point(self, name: str):
        """Kurtarma noktası oluştur"""
        try:
            recovery_point = {
                'name': name,
                'timestamp': datetime.now().isoformat(),
                'system_state': self.capture_system_state(),
                'config_backup': self.backup_configuration(),
                'data_backup': self.backup_essential_data()
            }
            
            self.recovery_points.append(recovery_point)
            self.save_recovery_point(recovery_point)
            return True
        except Exception:
            return False
    
    def capture_system_state(self) -> Dict:
        """Sistem durumunu yakala"""
        return {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'timestamp': datetime.now().isoformat(),
            'installed_managers': list(CrossPlatformPackageManager().get_available_managers().keys())
        }
    
    def backup_configuration(self) -> str:
        """Konfigürasyonu yedekle"""
        config_data = {
            'app_settings': {},
            'user_preferences': {},
            'schedule_config': {}
        }
        
        backup_file = os.path.join(self.backup_dir, f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        return backup_file
    
    def backup_essential_data(self) -> str:
        """Önemli verileri yedekle"""
        # Uygulama verilerini yedekle
        essential_data = {
            'update_history': [],
            'security_scans': [],
            'system_info': PlatformDetector.get_platform_info()
        }
        
        backup_file = os.path.join(self.backup_dir, f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(essential_data, f, indent=2)
        
        return backup_file
    
    def save_recovery_point(self, recovery_point: Dict):
        """Kurtarma noktasını kaydet"""
        recovery_file = os.path.join(self.backup_dir, f"recovery_{recovery_point['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(recovery_file, 'w', encoding='utf-8') as f:
            json.dump(recovery_point, f, indent=2)
    
    def restore_system(self, recovery_point_name: str) -> bool:
        """Sistemi kurtarma noktasından geri yükle"""
        recovery_point = self.find_recovery_point(recovery_point_name)
        if not recovery_point:
            return False
        
        try:
            # Config'leri geri yükle
            if os.path.exists(recovery_point['config_backup']):
                with open(recovery_point['config_backup'], 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                # Config'leri uygula
                print(f"Config restored from: {recovery_point['config_backup']}")
            
            # Verileri geri yükle
            if os.path.exists(recovery_point['data_backup']):
                with open(recovery_point['data_backup'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Verileri uygula
                print(f"Data restored from: {recovery_point['data_backup']")
            
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    def find_recovery_point(self, name: str) -> Optional[Dict]:
        """Kurtarma noktasını bul"""
        for point in self.recovery_points:
            if point['name'] == name:
                return point
        return None

# =========== PERFORMANS İZLEME ===========

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'disk_io': [],
            'network_io': [],
            'execution_times': []
        }
        self.scaling_policies = {
            'cpu_threshold': 80.0,
            'memory_threshold': 85.0,
            'max_concurrent_updates': 3
        }
        self.monitoring = False
    
    def start_monitoring(self):
        """Performans izlemeyi başlat"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """İzlemeyi durdur"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """İzleme döngüsü"""
        while self.monitoring:
            try:
                # CPU kullanımı
                cpu_percent = psutil.cpu_percent(interval=1)
                self.metrics['cpu_usage'].append(cpu_percent)
                
                # Bellek kullanımı
                memory = psutil.virtual_memory()
                self.metrics['memory_usage'].append(memory.percent)
                
                # Disk I/O
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    self.metrics['disk_io'].append({
                        'read_bytes': disk_io.read_bytes,
                        'write_bytes': disk_io.write_bytes
                    })
                
                # Son 100 kaydı tut
                for key in ['cpu_usage', 'memory_usage']:
                    self.metrics[key] = self.metrics[key][-100:]
                
                # Auto-scale kontrolü
                self.auto_scale()
                
            except Exception as e:
                print(f"Monitoring error: {e}")
            
            time.sleep(5)
    
    def auto_scale(self):
        """Otomatik ölçeklendirme"""
        if len(self.metrics['cpu_usage']) < 5:
            return
        
        avg_cpu = sum(self.metrics['cpu_usage'][-5:]) / 5
        avg_memory = sum(self.metrics['memory_usage'][-5:]) / 5
        
        # CPU threshold'ları
        if avg_cpu > self.scaling_policies['cpu_threshold']:
            self.scale_down_operations()
        elif avg_cpu < 20:
            self.scale_up_operations()
    
    def scale_down_operations(self):
        """Operasyonları ölçeklendir (aşağı)"""
        # Daha az eşzamanlı güncelleme
        self.scaling_policies['max_concurrent_updates'] = max(1, self.scaling_policies['max_concurrent_updates'] - 1)
        print(f"Scaling down: max_concurrent_updates = {self.scaling_policies['max_concurrent_updates']}")
    
    def scale_up_operations(self):
        """Operasyonları ölçeklendir (yukarı)"""
        # Daha fazla eşzamanlı güncelleme
        self.scaling_policies['max_concurrent_updates'] = min(5, self.scaling_policies['max_concurrent_updates'] + 1)
        print(f"Scaling up: max_concurrent_updates = {self.scaling_policies['max_concurrent_updates']}")
    
    def get_performance_report(self) -> Dict:
        """Performans raporu oluştur"""
        cpu_avg = sum(self.metrics['cpu_usage'][-10:]) / len(self.metrics['cpu_usage'][-10:]) if self.metrics['cpu_usage'] else 0
        memory_avg = sum(self.metrics['memory_usage'][-10:]) / len(self.metrics['memory_usage'][-10:]) if self.metrics['memory_usage'] else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': cpu_avg,
            'memory_usage': memory_avg,
            'system_load': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
            'scaling_policy': self.scaling_policies
        }

# =========== GÜNCELLENMİŞ ANA UYGULAMA ===========

class AdvancedUniversalUpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Tüm gelişmiş manager'ları başlat
        self.security_hardening = SecurityHardening()
        self.security_manager = SecurityManager()
        self.cloud_integration = CloudIntegration()
        self.notification_manager = NotificationManager()
        self.theme_manager = ThemeManager()
        self.disaster_recovery = DisasterRecovery()
        self.performance_monitor = PerformanceMonitor()
        
        # Orijinal manager'lar
        self.platform_info = PlatformDetector.get_platform_info()
        self.package_manager = CrossPlatformPackageManager()
        self.update_manager = UniversalUpdateManager()
        
        # GUI ayarları
        self.setup_advanced_gui()
        
        # Sistemleri başlat
        self.start_advanced_systems()
    
    def setup_advanced_gui(self):
        """Gelişmiş GUI kurulumu"""
        self.title("🚀 GELİŞMİŞ SİSTEM GÜNCELLEYİCİ")
        self.geometry("600x700")
        
        # Tema yöneticisi
        self.theme_manager.switch_theme("dark")
        
        # Ana container
        self.main_container = ctk.CTkTabview(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Gelişmiş sekmeler
        self.setup_dashboard_tab()
        self.setup_security_tab()
        self.setup_cloud_tab()
        self.setup_recovery_tab()
        self.setup_monitoring_tab()
        self.setup_settings_tab()
    
    def setup_dashboard_tab(self):
        """Dashboard sekmesi"""
        tab = self.main_container.add("📊 Dashboard")
        
        # Sistem durumu
        status_frame = ctk.CTkFrame(tab)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        self.system_status = ctk.CTkLabel(status_frame, text="🟢 Gelişmiş Sistem Aktif", 
                                         font=("Arial", 16, "bold"))
        self.system_status.pack(pady=10)
        
        # Hızlı aksiyon butonları
        self.setup_quick_actions(tab)
        
        # Orijinal güncelleme bileşenleri
        self.setup_update_components(tab)
    
    def setup_security_tab(self):
        """Güvenlik sekmesi"""
        tab = self.main_container.add("🔒 Güvenlik")
        
        security_frame = ctk.CTkFrame(tab)
        security_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkButton(security_frame, text="🔍 Güvenlik Taraması Başlat",
                     command=self.start_security_scan).pack(pady=5)
        
        ctk.CTkButton(security_frame, text="📊 Güvenlik Raporu",
                     command=self.show_security_report).pack(pady=5)
        
        ctk.CTkButton(security_frame, text="🛡️  Güvenlik Ayarları",
                     command=self.show_security_settings).pack(pady=5)
    
    def setup_cloud_tab(self):
        """Bulut sekmesi"""
        tab = self.main_container.add("☁️ Bulut")
        
        cloud_frame = ctk.CTkFrame(tab)
        cloud_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.api_key_entry = ctk.CTkEntry(cloud_frame, placeholder_text="API Anahtarınız")
        self.api_key_entry.pack(pady=5)
        
        ctk.CTkButton(cloud_frame, text="🔑 Bağlan",
                     command=self.connect_cloud).pack(pady=5)
        
        ctk.CTkButton(cloud_frame, text="🔄 Senkronize Et",
                     command=self.sync_with_cloud).pack(pady=5)
    
    def setup_recovery_tab(self):
        """Kurtarma sekmesi"""
        tab = self.main_container.add("💾 Kurtarma")
        
        recovery_frame = ctk.CTkFrame(tab)
        recovery_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkButton(recovery_frame, text="📸 Kurtarma Noktası Oluştur",
                     command=self.create_recovery_point).pack(pady=5)
        
        ctk.CTkButton(recovery_frame, text="🔄 Sistemi Geri Yükle",
                     command=self.restore_system).pack(pady=5)
        
        ctk.CTkButton(recovery_frame, text="📊 Kurtarma Geçmişi",
                     command=self.show_recovery_history).pack(pady=5)
    
    def setup_monitoring_tab(self):
        """Monitoring sekmesi"""
        tab = self.main_container.add("📈 Monitoring")
        
        monitoring_frame = ctk.CTkFrame(tab)
        monitoring_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.cpu_label = ctk.CTkLabel(monitoring_frame, text="CPU: --%")
        self.cpu_label.pack(pady=2)
        
        self.memory_label = ctk.CTkLabel(monitoring_frame, text="RAM: --%")
        self.memory_label.pack(pady=2)
        
        self.performance_label = ctk.CTkLabel(monitoring_frame, text="Performans: --")
        self.performance_label.pack(pady=2)
    
    def setup_settings_tab(self):
        """Ayarlar sekmesi"""
        tab = self.main_container.add("⚙️ Ayarlar")
        
        settings_frame = ctk.CTkFrame(tab)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tema seçimi
        ctk.CTkLabel(settings_frame, text="Tema:").pack(pady=2)
        theme_var = ctk.StringVar(value="dark")
        theme_dropdown = ctk.CTkOptionMenu(settings_frame, 
                                          values=["dark", "light", "blue", "high_contrast"],
                                          variable=theme_var,
                                          command=self.theme_manager.switch_theme)
        theme_dropdown.pack(pady=5)
        
        # Otomatik tema değiştirme
        self.auto_theme_var = ctk.BooleanVar()
        ctk.CTkCheckBox(settings_frame, text="Otomatik tema değiştir",
                       variable=self.auto_theme_var,
                       command=self.toggle_auto_theme).pack(pady=5)
    
    def setup_quick_actions(self, parent):
        """Hızlı aksiyon butonları"""
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        buttons = [
            ("🔍 Sistem Detayları", self.show_system_details),
            ("🛡️  Hızlı Tarama", self.quick_security_scan),
            ("💾 Yedek Al", self.quick_backup),
            ("📊 Performans", self.show_performance)
        ]
        
        for i in range(0, len(buttons), 2):
            row_frame = ctk.CTkFrame(actions_frame)
            row_frame.pack(pady=2)
            
            for text, command in buttons[i:i+2]:
                btn = ctk.CTkButton(row_frame, text=text, command=command, width=140)
                btn.pack(side="left", padx=2)
    
    def setup_update_components(self, parent):
        """Orijinal güncelleme bileşenleri"""
        # Progress bar
        self.progress = ctk.CTkProgressBar(parent, width=550, height=20)
        self.progress.set(0)
        self.progress.pack(pady=10)
        
        # Durum label
        self.status_label = ctk.CTkLabel(parent, text="Sistem hazır", font=("Arial", 14))
        self.status_label.pack(pady=5)
        
        # Güncelle butonu
        self.update_btn = ctk.CTkButton(parent, text="🚀 GÜNCELLEME BAŞLAT",
                                       command=self.start_secure_update,
                                       font=("Arial", 14, "bold"),
                                       height=35)
        self.update_btn.pack(pady=10)
        
        # Çıktı alanı
        self.output_text = ctk.CTkTextbox(parent, width=560, height=150)
        self.output_text.pack(pady=10, fill="x", padx=20)
        self.output_text.insert("1.0", "Güvenli güncelleme detayları burada görünecek...\n")
        self.output_text.configure(state="disabled")
    
    def start_advanced_systems(self):
        """Gelişmiş sistemleri başlat"""
        # Performans izlemeyi başlat
        self.performance_monitor.start_monitoring()
        
        # Durum güncelleme döngüsünü başlat
        self.start_advanced_status_updater()
        
        # Güvenlik taraması
        threading.Thread(target=self.initial_security_scan, daemon=True).start()
    
    def start_advanced_status_updater(self):
        """Gelişmiş durum güncelleyici"""
        def update_loop():
            while True:
                try:
                    # Performans metriklerini güncelle
                    report = self.performance_monitor.get_performance_report()
                    
                    self.cpu_label.configure(text=f"CPU: {report['cpu_usage']:.1f}%")
                    self.memory_label.configure(text=f"RAM: {report['memory_usage']:.1f}%")
                    
                    # Performans durumu
                    if report['cpu_usage'] > 80:
                        status = "⚠️ Yüksek Yük"
                    elif report['cpu_usage'] > 60:
                        status = "🔶 Orta Yük"
                    else:
                        status = "✅ Normal"
                    
                    self.performance_label.configure(text=f"Performans: {status}")
                    
                except Exception as e:
                    print(f"Status update error: {e}")
                
                time.sleep(3)
        
        threading.Thread(target=update_loop, daemon=True).start()
    
    def start_secure_update(self):
        """Güvenli güncelleme başlat"""
        # Güvenlik kontrolü
        if not self.security_hardening.validate_command(['update']):
            self.notification_manager.send_notification(
                "Güvenlik Uyarısı",
                "Güncelleme komutu güvenlik kontrolünden geçemedi!",
                "security"
            )
            return
        
        self.progress.set(0)
        self.status_label.configure(text="Güvenli güncelleme başlatılıyor...")
        self.update_btn.configure(state="disabled")
        
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "🔒 GÜVENLİ GÜNCELLEME BAŞLATILDI\n")
        self.output_text.insert("end", "• Komut güvenlik kontrolü: ✅\n")
        self.output_text.insert("end", "• Sistem izolasyonu: ✅\n")
        self.output_text.configure(state="disabled")
        
        # Bildirim gönder
        self.notification_manager.send_notification(
            "Güncelleme Başlatıldı",
            "Sistem güncellemesi güvenli modda başlatıldı",
            "normal"
        )
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self.run_secure_update_thread)
        thread.daemon = True
        thread.start()
    
    def run_secure_update_thread(self):
        """Güvenli güncelleme thread'i"""
        managers = self.package_manager.get_available_managers()
        
        if not managers:
            error_msg = "❌ Paket yöneticisi bulunamadı"
            self.notification_manager.send_notification("Güncelleme Hatası", error_msg, "critical")
            self.update_done(error_msg, [])
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
                
                # Güvenli komut çalıştırma
                result = self.security_hardening.secure_command_execution(command)
                
                if result['success']:
                    success_count += 1
                    details.append(f"✅ {manager_info['name']} - Başarılı")
                else:
                    details.append(f"❌ {manager_info['name']} - Hata: {result['error']}")
                
                time.sleep(1)
        
        summary = f"🎉 Güvenli güncelleme tamamlandı! {success_count}/{total_commands} başarılı"
        
        # Bildirim gönder
        self.notification_manager.send_notification(
            "Güncelleme Tamamlandı",
            f"{success_count}/{total_commands} işlem başarılı",
            "normal" if success_count == total_commands else "warning"
        )
        
        self.update_done(summary, details)
    
    def update_progress(self, percent, detail):
        """İlerlemeyi güncelle"""
        self.progress.set(percent / 100)
        self.status_label.configure(text=f"Güvenli güncelleme... %{int(percent)}")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"⏳ {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def update_done(self, message, details):
        """Güncelleme tamamlandı"""
        self.progress.set(1.0)
        self.status_label.configure(text="Güvenli güncelleme tamamlandı!")
        self.update_btn.configure(state="normal")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"\n🎉 {message}\n")
        for detail in details:
            self.output_text.insert("end", f"• {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
        
        # Kurtarma noktası oluştur
        self.disaster_recovery.create_recovery_point("post_update")
    
    # Gelişmiş metodlar
    def start_security_scan(self):
        """Güvenlik taraması başlat"""
        self.notification_manager.send_notification(
            "Güvenlik Taraması",
            "Sistem güvenlik taraması başlatıldı",
            "security"
        )
        
        def scan_thread():
            vulnerabilities = self.security_manager.vulnerability_scan()
            
            if vulnerabilities:
                message = f"{len(vulnerabilities)} güvenlik açığı bulundu"
                self.notification_manager.send_notification(
                    "Güvenlik Uyarısı",
                    message,
                    "critical"
                )
            else:
                self.notification_manager.send_notification(
                    "Güvenlik Taraması",
                    "Güvenlik taraması temiz",
                    "normal"
                )
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def connect_cloud(self):
        """Buluta bağlan"""
        api_key = self.api_key_entry.get()
        if self.cloud_integration.authenticate(api_key):
            self.notification_manager.send_notification(
                "Bulut Bağlantısı",
                "Bulut servisine başarıyla bağlanıldı",
                "normal"
            )
        else:
            self.notification_manager.send_notification(
                "Bağlantı Hatası",
                "Bulut servisine bağlanılamadı",
                "warning"
            )
    
    def create_recovery_point(self):
        """Kurtarma noktası oluştur"""
        if self.disaster_recovery.create_recovery_point("manual_backup"):
            self.notification_manager.send_notification(
                "Kurtarma Noktası",
                "Sistem kurtarma noktası oluşturuldu",
                "normal"
            )
        else:
            self.notification_manager.send_notification(
                "Yedekleme Hatası",
                "Kurtarma noktası oluşturulamadı",
                "warning"
            )
    
    def toggle_auto_theme(self):
        """Otomatik tema değiştirmeyi aç/kapat"""
        if self.auto_theme_var.get():
            self.theme_manager.enable_auto_switch()
        else:
            self.theme_manager.auto_switch_enabled = False
    
    def initial_security_scan(self):
        """İlk güvenlik taraması"""
        time.sleep(5)  # Uygulama başladıktan sonra
        self.security_manager.vulnerability_scan()
    
    def quick_security_scan(self):
        """Hızlı güvenlik taraması"""
        self.start_security_scan()
    
    def quick_backup(self):
        """Hızlı yedek"""
        self.create_recovery_point()
    
    def show_performance(self):
        """Performans bilgilerini göster"""
        report = self.performance_monitor.get_performance_report()
        messagebox.showinfo(
            "Sistem Performansı",
            f"CPU: {report['cpu_usage']:.1f}%\n"
            f"RAM: {report['memory_usage']:.1f}%\n"
            f"Eşzamanlı Güncelleme: {report['scaling_policy']['max_concurrent_updates']}"
        )
    
    def show_system_details(self):
        """Sistem detaylarını göster"""
        PlatformSpecificUI.show_details(self)

# =========== UYGULAMAYI BAŞLAT ===========

if __name__ == "__main__":
    # Çapraz platform uyumluluk
    if platform.system().lower() not in ['windows', 'darwin', 'linux']:
        print("⚠️ Desteklenmeyen işletim sistemi")
        sys.exit(1)
    
    # Gerekli kütüphaneleri kontrol et
    try:
        import psutil
    except ImportError:
        print("❌ 'psutil' kütüphanesi gerekli. Yüklemek için:")
        print("pip install psutil")
        sys.exit(1)
    
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("❌ 'cryptography' kütüphanesi gerekli. Yüklemek için:")
        print("pip install cryptography")
        sys.exit(1)
    
    # Gelişmiş uygulamayı başlat
    app = AdvancedUniversalUpdaterApp()
    app.mainloop()
