

import os
import platform
import shutil
import subprocess
import threading
import time
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
import sys

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
        
        # Dağıtım bilgisi (Linux için)
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

# ---------- Çapraz Platform Paket Yöneticileri ----------
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
        
        # Winget (Modern Windows)
        if shutil.which('winget'):
            managers['winget'] = {
                'name': 'Windows Package Manager',
                'description': 'Microsoft resmi paket yöneticisi',
                'commands': [
                    ['winget', 'upgrade', '--all', '--accept-source-agreements', '--accept-package-agreements']
                ]
            }
        
        # Chocolatey
        if shutil.which('choco'):
            managers['choco'] = {
                'name': 'Chocolatey',
                'description': 'Windows için paket yöneticisi',
                'commands': [
                    ['choco', 'upgrade', 'all', '-y']
                ]
            }
            
        # Scoop
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
        
        # Homebrew
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
        
        # Mac App Store (mas)
        if shutil.which('mas'):
            managers['mas'] = {
                'name': 'Mac App Store',
                'description': 'Mac App Store uygulamaları',
                'commands': [
                    ['mas', 'upgrade']
                ]
            }
            
        # port (MacPorts)
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
        
        # APT (Debian/Ubuntu/Mint)
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
        
        # DNF (Fedora/RHEL)
        if shutil.which('dnf'):
            managers['dnf'] = {
                'name': 'DNF Package Manager',
                'description': 'Fedora/RHEL tabanlı sistemler',
                'commands': [
                    ['sudo', 'dnf', 'upgrade', '--refresh', '-y']
                ]
            }
        
        # Pacman (Arch/Manjaro)
        if shutil.which('pacman'):
            managers['pacman'] = {
                'name': 'Pacman Package Manager',
                'description': 'Arch Linux tabanlı sistemler',
                'commands': [
                    ['sudo', 'pacman', '-Syu', '--noconfirm']
                ]
            }
        
        # Zypper (openSUSE)
        if shutil.which('zypper'):
            managers['zypper'] = {
                'name': 'Zypper Package Manager',
                'description': 'openSUSE tabanlı sistemler',
                'commands': [
                    ['sudo', 'zypper', 'refresh'],
                    ['sudo', 'zypper', 'update', '-y']
                ]
            }
        
        # Snap
        if shutil.which('snap'):
            managers['snap'] = {
                'name': 'Snap Packages',
                'description': 'Universal Linux paketleri',
                'commands': [
                    ['sudo', 'snap', 'refresh']
                ]
            }
        
        # Flatpak
        if shutil.which('flatpak'):
            managers['flatpak'] = {
                'name': 'Flatpak Applications',
                'description': 'Flatpak uygulamaları',
                'commands': [
                    ['flatpak', 'update', '-y']
                ]
            }
            
        return managers

# ---------- Platforma Özel GUI Ayarları ----------
class PlatformSpecificUI:
    @staticmethod
    def get_platform_theme():
        """Platforma göre tema seç"""
        system = platform.system().lower()
        
        if system == 'windows':
            return "blue"
        elif system == 'darwin':
            return "green" 
        elif system == 'linux':
            return "dark-blue"
        else:
            return "blue"
    
    @staticmethod
    def get_window_size():
        """Platforma göre pencere boyutu"""
        system = platform.system().lower()
        
        if system == 'windows':
            return "500x400"
        elif system == 'darwin':
            return "550x450"  # macOS'ta biraz daha büyük
        elif system == 'linux':
            return "500x400"
        else:
            return "500x400"
    
    @staticmethod
    def get_platform_icon():
        """Platforma göre ikon"""
        system = platform.system().lower()
        
        icons = {
            'windows': '🪟',
            'darwin': '🍎', 
            'linux': '🐧'
        }
        return icons.get(system, '💻')

# ---------- Çapraz Platform Güncelleme Yöneticisi ----------
class UniversalUpdateManager:
    def __init__(self):
        self.package_manager = CrossPlatformPackageManager()
        self.managers = self.package_manager.get_available_managers()
        
    def run_updates(self, callback_progress, callback_done):
        """Tüm güncellemeleri çalıştır"""
        if not self.managers:
            callback_done("❌ Sisteminizde paket yöneticisi bulunamadı", [])
            return
        
        total_commands = sum(len(mgr['commands']) for mgr in self.managers.values())
        completed = 0
        success_count = 0
        details = []
        
        for manager_id, manager_info in self.managers.items():
            for command in manager_info['commands']:
                completed += 1
                progress = (completed / total_commands) * 100
                
                callback_progress(progress, f"{manager_info['name']} - {command[0]}")
                
                try:
                    # Linux/macOS için sudo gerekiyorsa
                    if platform.system().lower() != 'windows' and command[0] == 'sudo':
                        # GUI şifre isteme (basit versiyon)
                        result = self._run_command_with_privileges(command)
                    else:
                        result = subprocess.run(
                            command, 
                            capture_output=True, 
                            text=True, 
                            timeout=300,
                            shell=False
                        )
                    
                    if result.returncode == 0:
                        success_count += 1
                        details.append(f"✅ {manager_info['name']} - Başarılı")
                    else:
                        error_msg = result.stderr[:100] if result.stderr else "Bilinmeyen hata"
                        details.append(f"❌ {manager_info['name']} - Hata: {error_msg}")
                        
                except subprocess.TimeoutExpired:
                    details.append(f"⏰ {manager_info['name']} - Zaman aşımı")
                except Exception as e:
                    details.append(f"⚠️ {manager_info['name']} - Hata: {str(e)}")
                
                time.sleep(1)  # Sistem yükünü azaltmak için
        
        summary = f"🎉 Güncelleme tamamlandı! {success_count}/{total_commands} başarılı"
        callback_done(summary, details)
    
    def _run_command_with_privileges(self, command):
        """Ayrıcalıklı komut çalıştırma (basit implementasyon)"""
        # Not: Gerçek uygulamada GUI şifre istemesi eklenmeli
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,
                shell=False
            )
            return result
        except:
            # Şifre gerekirse burada GUI dialog gösterilebilir
            return type('obj', (object,), {'returncode': 1, 'stderr': 'İzin reddedildi'})()

# ---------- Gelişmiş Detaylar Penceresi ----------
class AdvancedDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🔍 Detaylı Sistem Bilgileri")
        self.geometry("700x600")
        self.transient(parent)
        self.grab_set()
        
        self.platform_info = PlatformDetector.get_platform_info()
        self.package_manager = CrossPlatformPackageManager()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Sekmeler
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sistem Bilgileri
        self.tabview.add("🖥️ Sistem Bilgileri")
        self.setup_system_tab()
        
        # Paket Yöneticileri
        self.tabview.add("📦 Paket Yöneticileri")
        self.setup_packages_tab()
        
        # Güncelleme Geçmişi
        self.tabview.add("📊 Güncelleme Durumu")
        self.setup_status_tab()
    
    def setup_system_tab(self):
        text_widget = ctk.CTkTextbox(self.tabview.tab("🖥️ Sistem Bilgileri"))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.insert("end", "🔧 DETAYLI SİSTEM BİLGİLERİ\n\n")
        for key, value in self.platform_info.items():
            text_widget.insert("end", f"• {key.replace('_', ' ').title()}: {value}\n")
        
        text_widget.configure(state="disabled")
    
    def setup_packages_tab(self):
        text_widget = ctk.CTkTextbox(self.tabview.tab("📦 Paket Yöneticileri"))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        managers = self.package_manager.get_available_managers()
        
        text_widget.insert("end", "📦 TESPİT EDİLEN PAKET YÖNETİCİLERİ\n\n")
        
        if managers:
            for manager_id, manager_info in managers.items():
                text_widget.insert("end", f"✅ {manager_info['name']}\n")
                text_widget.insert("end", f"   📝 {manager_info['description']}\n")
                text_widget.insert("end", f"   ⚙️  Komutlar: {' | '.join([' '.join(cmd) for cmd in manager_info['commands']])}\n\n")
        else:
            text_widget.insert("end", "❌ Paket yöneticisi bulunamadı\n")
        
        text_widget.configure(state="disabled")
    
    def setup_status_tab(self):
        text_widget = ctk.CTkTextbox(self.tabview.tab("📊 Güncelleme Durumu"))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.insert("end", "🔄 GÜNCELLEME DURUMU\n\n")
        text_widget.insert("end", f"• Platform: {self.platform_info['system'].title()}\n")
        text_widget.insert("end", f"• Mimari: {self.platform_info['architecture']}\n")
        text_widget.insert("end", f"• Python: {self.platform_info['python_version']}\n\n")
        
        managers = self.package_manager.get_available_managers()
        text_widget.insert("end", f"• Tespit Edilen Yöneticiler: {len(managers)}\n")
        
        text_widget.configure(state="disabled")

# ---------- Ana Uygulama ----------
class UniversalUpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Platforma özel ayarlar
        self.platform_ui = PlatformSpecificUI()
        self.theme = self.platform_ui.get_platform_theme()
        self.window_size = self.platform_ui.get_window_size()
        self.platform_icon = self.platform_ui.get_platform_icon()
        
        # GUI ayarları
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(self.theme)
        
        self.title(f"{self.platform_icon} Evrensel Sistem Güncelleyici")
        self.geometry(self.window_size)
        
        # Güncelleme yöneticisi
        self.update_manager = UniversalUpdateManager()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Platform bilgisi
        platform_info = PlatformDetector.get_platform_info()
        platform_name = platform_info.get('distribution') or f"{platform_info['system'].title()} {platform_info['release']}"
        
        # Başlık
        title_label = ctk.CTkLabel(self, text="🚀 Evrensel Sistem Güncelleyici", 
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=15)
        
        # Platform bilgisi
        platform_label = ctk.CTkLabel(self, text=f"Platform: {platform_name}", 
                                     font=("Arial", 12))
        platform_label.pack(pady=5)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=450, height=20)
        self.progress.set(0)
        self.progress.pack(pady=15)
        
        # Durum label
        self.status_label = ctk.CTkLabel(self, text="Sistem hazır", 
                                        font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        # Butonlar frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=15)
        
        # Güncelle butonu
        self.update_btn = ctk.CTkButton(button_frame, text="🔄 Tümünü Güncelle",
                                       command=self.start_update,
                                       font=("Arial", 14),
                                       width=140)
        self.update_btn.pack(side="left", padx=10)
        
        # Detaylar butonu
        self.details_btn = ctk.CTkButton(button_frame, text="🔍 Sistem Detayları",
                                        command=self.show_details,
                                        font=("Arial", 14),
                                        width=140)
        self.details_btn.pack(side="left", padx=10)
        
        # Detaylı çıktı alanı
        self.output_text = ctk.CTkTextbox(self, width=460, height=150)
        self.output_text.pack(pady=10, fill="x", padx=20)
        self.output_text.insert("1.0", "Güncelleme detayları burada görünecek...\n")
        self.output_text.configure(state="disabled")
        
        # Çıkış butonu
        self.quit_btn = ctk.CTkButton(self, text="❌ Çıkış",
                                     command=self.destroy,
                                     fg_color="red",
                                     font=("Arial", 12))
        self.quit_btn.pack(pady=10)
    
    def show_details(self):
        """Detaylı bilgi penceresini aç"""
        AdvancedDetailsWindow(self)
    
    def start_update(self):
        """Güncellemeyi başlat"""
        self.progress.set(0)
        self.status_label.configure(text="Güncelleme başlatılıyor...")
        self.update_btn.configure(state="disabled")
        
        # Çıktı alanını temizle
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "🔧 Güncelleme başlatıldı...\n")
        self.output_text.configure(state="disabled")
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self.run_update_thread)
        thread.daemon = True
        thread.start()
    
    def run_update_thread(self):
        self.update_manager.run_updates(self.update_progress, self.update_done)
    
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

# ---------- Uygulamayı Başlat ----------
if __name__ == "__main__":
    # Çapraz platform uyumluluk
    if platform.system().lower() not in ['windows', 'darwin', 'linux']:
        print("⚠️ Desteklenmeyen işletim sistemi")
        sys.exit(1)
    
    app = UniversalUpdaterApp()
    app.mainloop()



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
import schedule
from typing import Dict, List, Optional

# ---------- Zamanlama Sistemi ----------
class ScheduledUpdateManager:
    def __init__(self, config_file="schedule_config.json"):
        self.config_file = config_file
        self.schedule_config = self.load_config()
        self.scheduler_running = False
        
    def load_config(self) -> Dict:
        """Zamanlama ayarlarını yükle"""
        default_config = {
            "enabled": False,
            "schedule_type": "weekly",  # weekly, daily, monthly
            "day_of_week": "monday",    # monday, tuesday, etc.
            "time": "14:00",            # HH:MM format
            "last_run": None,
            "next_run": None
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Config yükleme hatası: {e}")
            
        return default_config
    
    def save_config(self):
        """Zamanlama ayarlarını kaydet"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedule_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Config kaydetme hatası: {e}")
    
    def set_schedule(self, schedule_type: str, day_of_week: str, time_str: str):
        """Yeni zamanlama ayarla"""
        self.schedule_config.update({
            "enabled": True,
            "schedule_type": schedule_type.lower(),
            "day_of_week": day_of_week.lower(),
            "time": time_str,
            "last_run": None,
            "next_run": self.calculate_next_run(schedule_type, day_of_week, time_str)
        })
        self.save_config()
        
    def calculate_next_run(self, schedule_type: str, day_of_week: str, time_str: str) -> str:
        """Bir sonraki çalışma zamanını hesapla"""
        now = datetime.now()
        target_time = datetime.strptime(time_str, "%H:%M").time()
        
        if schedule_type == "daily":
            next_run = datetime.combine(now.date(), target_time)
            if next_run <= now:
                next_run += timedelta(days=1)
                
        elif schedule_type == "weekly":
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            target_day = days.index(day_of_week.lower())
            current_day = now.weekday()
            
            days_ahead = target_day - current_day
            if days_ahead <= 0:
                days_ahead += 7
                
            next_run = datetime.combine(now.date() + timedelta(days=days_ahead), target_time)
            
        else:  # monthly
            next_run = datetime.combine(now.date().replace(day=1), target_time)
            if next_run <= now:
                next_run = next_run.replace(month=next_run.month + 1)
        
        return next_run.isoformat()
    
    def get_next_run_info(self) -> str:
        """Bir sonraki çalışma bilgisini formatla"""
        if not self.schedule_config["enabled"]:
            return "Zamanlama kapalı"
            
        next_run_str = self.schedule_config.get("next_run")
        if not next_run_str:
            return "Zamanlama ayarlanmamış"
            
        try:
            next_run = datetime.fromisoformat(next_run_str)
            now = datetime.now()
            
            if next_run <= now:
                return "Şimdi çalışacak!"
            else:
                delta = next_run - now
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                
                if days > 0:
                    return f"{days} gün {hours} saat sonra"
                elif hours > 0:
                    return f"{hours} saat {minutes} dakika sonra"
                else:
                    return f"{minutes} dakika sonra"
                    
        except Exception as e:
            return f"Hesaplama hatası: {e}"
    
    def start_scheduler(self, update_callback):
        """Zamanlayıcıyı başlat"""
        if not self.schedule_config["enabled"]:
            return
            
        self.scheduler_running = True
        self.update_callback = update_callback
        
        # Schedule kütüphanesi ile zamanlama
        schedule.clear()
        
        if self.schedule_config["schedule_type"] == "daily":
            schedule.every().day.at(self.schedule_config["time"]).do(
                self._run_scheduled_update
            )
        elif self.schedule_config["schedule_type"] == "weekly":
            day_method = getattr(schedule.every(), self.schedule_config["day_of_week"])
            day_method.at(self.schedule_config["time"]).do(
                self._run_scheduled_update
            )
        
        # Zamanlayıcı thread'ini başlat
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        print("⏰ Zamanlayıcı başlatıldı")
    
    def _scheduler_loop(self):
        """Zamanlayıcı döngüsü"""
        while self.scheduler_running:
            schedule.run_pending()
            time.sleep(60)  # Her dakika kontrol et
    
    def _run_scheduled_update(self):
        """Zamanlanmış güncellemeyi çalıştır"""
        print("🔄 Zamanlanmış güncelleme başlatılıyor...")
        
        # Son çalışma zamanını güncelle
        self.schedule_config["last_run"] = datetime.now().isoformat()
        self.schedule_config["next_run"] = self.calculate_next_run(
            self.schedule_config["schedule_type"],
            self.schedule_config["day_of_week"],
            self.schedule_config["time"]
        )
        self.save_config()
        
        # Güncellemeyi başlat
        if self.update_callback:
            self.update_callback(scheduled=True)
    
    def stop_scheduler(self):
        """Zamanlayıcıyı durdur"""
        self.scheduler_running = False
        schedule.clear()
        print("⏹️ Zamanlayıcı durduruldu")

# ---------- Platform Tespiti (Önceki koddan) ----------
class PlatformDetector:
    @staticmethod
    def get_platform_info():
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
        try:
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True)
            return f"macOS {result.stdout.strip()}"
        except:
            return "macOS"

# ---------- Çapraz Platform Paket Yöneticileri (Önceki koddan) ----------
class CrossPlatformPackageManager:
    def __init__(self):
        self.platform_info = PlatformDetector.get_platform_info()
        self.system = self.platform_info['system']
        
    def get_available_managers(self):
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
            
        return managers
    
    def _get_macos_managers(self):
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
            
        return managers
    
    def _get_linux_managers(self):
        managers = {}
        
        if shutil.which('apt') or shutil.which('apt-get'):
            apt_cmd = 'apt' if shutil.which('apt') else 'apt-get'
            managers['apt'] = {
                'name': 'APT Package Manager',
                'description': 'Debian tabanlı sistemler',
                'commands': [
                    ['sudo', apt_cmd, 'update'],
                    ['sudo', apt_cmd, 'upgrade', '-y'],
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
        
        return managers

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
        # Ana frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = ctk.CTkLabel(main_frame, text="Zamanlanmış Güncelleme", 
                                  font=("Arial", 16, "bold"))
        title_label.pack(pady=15)
        
        # Aktiflik durumu
        self.enable_var = ctk.BooleanVar()
        self.enable_check = ctk.CTkCheckBox(main_frame, text="Zamanlanmış güncellemeyi aktif et",
                                           variable=self.enable_var,
                                           command=self.toggle_settings)
        self.enable_check.pack(pady=10)
        
        # Zamanlama türü
        type_frame = ctk.CTkFrame(main_frame)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(type_frame, text="Zamanlama Türü:").pack(side="left", padx=5)
        self.schedule_type = ctk.CTkOptionMenu(type_frame, 
                                              values=["Günlük", "Haftalık", "Aylık"])
        self.schedule_type.pack(side="left", padx=5)
        self.schedule_type.set("Haftalık")
        
        # Gün seçimi (haftalık için)
        self.day_frame = ctk.CTkFrame(main_frame)
        self.day_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.day_frame, text="Gün:").pack(side="left", padx=5)
        self.day_of_week = ctk.CTkOptionMenu(self.day_frame,
                                           values=["Pazartesi", "Salı", "Çarşamba", "Perşembe", 
                                                  "Cuma", "Cumartesi", "Pazar"])
        self.day_of_week.pack(side="left", padx=5)
        self.day_of_week.set("Pazartesi")
        
        # Saat seçimi
        time_frame = ctk.CTkFrame(main_frame)
        time_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(time_frame, text="Saat:").pack(side="left", padx=5)
        self.hour_var = ctk.StringVar(value="14")
        self.hour_entry = ctk.CTkEntry(time_frame, textvariable=self.hour_var, width=50)
        self.hour_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(time_frame, text=":").pack(side="left", padx=2)
        self.minute_var = ctk.StringVar(value="00")
        self.minute_entry = ctk.CTkEntry(time_frame, textvariable=self.minute_var, width=50)
        self.minute_entry.pack(side="left", padx=5)
        
        # Durum bilgisi
        self.status_label = ctk.CTkLabel(main_frame, text="", 
                                        text_color="gray", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        # Butonlar
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="✅ Kaydet", 
                     command=self.save_settings).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="❌ İptal", 
                     command=self.destroy).pack(side="left", padx=10)
    
    def load_current_settings(self):
        """Mevcut ayarları yükle"""
        config = self.schedule_manager.schedule_config
        
        self.enable_var.set(config["enabled"])
        
        if config["schedule_type"] == "daily":
            self.schedule_type.set("Günlük")
        elif config["schedule_type"] == "weekly":
            self.schedule_type.set("Haftalık")
        else:
            self.schedule_type.set("Aylık")
        
        # Gün mapping
        day_map = {"monday": "Pazartesi", "tuesday": "Salı", "wednesday": "Çarşamba",
                  "thursday": "Perşembe", "friday": "Cuma", "saturday": "Cumartesi",
                  "sunday": "Pazar"}
        self.day_of_week.set(day_map.get(config["day_of_week"], "Pazartesi"))
        
        if config["time"]:
            hour, minute = config["time"].split(":")
            self.hour_var.set(hour)
            self.minute_var.set(minute)
        
        self.update_status_display()
        self.toggle_settings()
    
    def toggle_settings(self):
        """Ayarları aktif/pasif yap"""
        enabled = self.enable_var.get()
        widgets = [self.schedule_type, self.day_of_week, self.hour_entry, self.minute_entry]
        
        for widget in widgets:
            if enabled:
                widget.configure(state="normal")
            else:
                widget.configure(state="disabled")
    
    def update_status_display(self):
        """Durum bilgisini güncelle"""
        next_run_info = self.schedule_manager.get_next_run_info()
        config = self.schedule_manager.schedule_config
        
        status_text = f"Sonraki çalışma: {next_run_info}\n"
        
        if config.get("last_run"):
            last_run = datetime.fromisoformat(config["last_run"])
            status_text += f"Son çalışma: {last_run.strftime('%d.%m.%Y %H:%M')}"
        
        self.status_label.configure(text=status_text)
    
    def save_settings(self):
        """Ayarları kaydet"""
        try:
            if not self.enable_var.get():
                # Zamanlamayı kapat
                self.schedule_manager.schedule_config["enabled"] = False
                self.schedule_manager.save_config()
                self.on_schedule_updated()
                self.destroy()
                return
            
            # Zamanlama türü mapping
            type_map = {"Günlük": "daily", "Haftalık": "weekly", "Aylık": "monthly"}
            schedule_type = type_map[self.schedule_type.get()]
            
            # Gün mapping
            day_map = {"Pazartesi": "monday", "Salı": "tuesday", "Çarşamba": "wednesday",
                      "Perşembe": "thursday", "Cuma": "friday", "Cumartesi": "saturday",
                      "Pazar": "sunday"}
            day_of_week = day_map[self.day_of_week.get()]
            
            # Saat kontrolü
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            
            if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                messagebox.showerror("Hata", "Saat 0-23, dakika 0-59 arası olmalı!")
                return
            
            time_str = f"{hour:02d}:{minute:02d}"
            
            # Ayarları kaydet
            self.schedule_manager.set_schedule(schedule_type, day_of_week, time_str)
            self.on_schedule_updated()
            
            messagebox.showinfo("Başarılı", "Zamanlama ayarları kaydedildi!")
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz saat formatı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi: {e}")

# ---------- Güncellenmiş Ana Uygulama ----------
class UniversalUpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Platform ayarları
        self.platform_info = PlatformDetector.get_platform_info()
        system = self.platform_info['system']
        
        # GUI ayarları
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        self.title("🚀 Evrensel Sistem Güncelleyici")
        self.geometry("500x450")
        
        # Yöneticiler
        self.package_manager = CrossPlatformPackageManager()
        self.schedule_manager = ScheduledUpdateManager()
        
        self.setup_ui()
        
        # Zamanlayıcıyı başlat
        self.schedule_manager.start_scheduler(self.start_scheduled_update)
    
    def setup_ui(self):
        # Başlık
        title_label = ctk.CTkLabel(self, text="🚀 Sistem Güncelleyici", 
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=15)
        
        # Platform bilgisi
        platform_name = self.platform_info.get('distribution') or f"{self.platform_info['system'].title()} {self.platform_info['release']}"
        platform_label = ctk.CTkLabel(self, text=f"Platform: {platform_name}", 
                                     font=("Arial", 12))
        platform_label.pack(pady=5)
        
        # Zamanlama durumu
        self.schedule_status = ctk.CTkLabel(self, text="", font=("Arial", 10))
        self.schedule_status.pack(pady=5)
        self.update_schedule_status()
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=450, height=20)
        self.progress.set(0)
        self.progress.pack(pady=15)
        
        # Durum label
        self.status_label = ctk.CTkLabel(self, text="Sistem hazır", 
                                        font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        # Butonlar frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        # Güncelle butonu
        self.update_btn = ctk.CTkButton(button_frame, text="🔄 Güncelle",
                                       command=lambda: self.start_update(),
                                       font=("Arial", 12),
                                       width=100)
        self.update_btn.pack(side="left", padx=5)
        
        # Zamanlama butonu
        self.schedule_btn = ctk.CTkButton(button_frame, text="⏰ Zamanlama",
                                         command=self.show_schedule_settings,
                                         font=("Arial", 12),
                                         width=100)
        self.schedule_btn.pack(side="left", padx=5)
        
        # Detaylar butonu
        self.details_btn = ctk.CTkButton(button_frame, text="🔍 Detaylar",
                                        command=self.show_details,
                                        font=("Arial", 12),
                                        width=100)
        self.details_btn.pack(side="left", padx=5)
        
        # Çıktı alanı
        self.output_text = ctk.CTkTextbox(self, width=460, height=150)
        self.output_text.pack(pady=10, fill="x", padx=20)
        self.output_text.insert("1.0", "Güncelleme detayları burada görünecek...\n")
        self.output_text.configure(state="disabled")
        
        # Çıkış butonu
        self.quit_btn = ctk.CTkButton(self, text="❌ Çıkış",
                                     command=self.cleanup_and_exit,
                                     fg_color="red",
                                     font=("Arial", 12))
        self.quit_btn.pack(pady=10)
    
    def update_schedule_status(self):
        """Zamanlama durumunu güncelle"""
        status = self.schedule_manager.get_next_run_info()
        color = "green" if "sonra" in status else "orange"
        self.schedule_status.configure(text=f"⏰ {status}", text_color=color)
    
    def show_schedule_settings(self):
        """Zamanlama ayarları penceresini aç"""
        ScheduleSettingsWindow(self, self.schedule_manager, self.on_schedule_updated)
    
    def on_schedule_updated(self):
        """Zamanlama güncellendiğinde çağrılır"""
        self.schedule_manager.stop_scheduler()
        self.schedule_manager.start_scheduler(self.start_scheduled_update)
        self.update_schedule_status()
    
    def start_scheduled_update(self, scheduled=False):
        """Zamanlanmış güncellemeyi başlat"""
        if scheduled:
            # Bildirim göster (basit versiyon)
            try:
                if platform.system() == "Windows":
                    subprocess.run(["msg", "*", "Zamanlanmış güncelleme başlatılıyor..."])
            except:
                pass
        
        self.start_update()
    
    def start_update(self, scheduled=False):
        """Güncellemeyi başlat"""
        self.progress.set(0)
        self.status_label.configure(text="Güncelleme başlatılıyor...")
        self.update_btn.configure(state="disabled")
        
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        
        if scheduled:
            self.output_text.insert("end", "⏰ ZAMANLANMIŞ GÜNCELLEME BAŞLATILDI\n")
        else:
            self.output_text.insert("end", "🔧 Manuel güncelleme başlatıldı...\n")
            
        self.output_text.configure(state="disabled")
        
        thread = threading.Thread(target=self.run_update_thread)
        thread.daemon = True
        thread.start()
    
    def run_update_thread(self):
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
        self.update_done(summary, details)
    
    def update_progress(self, percent, detail):
        self.progress.set(percent / 100)
        self.status_label.configure(text=f"Güncelleniyor... %{int(percent)}")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"⏳ {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def update_done(self, message, details):
        self.progress.set(1.0)
        self.status_label.configure(text="Tamamlandı!")
        self.update_btn.configure(state="normal")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"\n🎉 {message}\n")
        for detail in details:
            self.output_text.insert("end", f"• {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
        
        # Zamanlama durumunu güncelle
        self.schedule_manager.schedule_config["last_run"] = datetime.now().isoformat()
        self.schedule_manager.save_config()
        self.update_schedule_status()
        
        messagebox.showinfo("Güncelleme Tamamlandı", message)
    
    def show_details(self):
        """Basit detaylar penceresi"""
        managers = self.package_manager.get_available_managers()
        
        details_text = f"🖥️ SİSTEM BİLGİLERİ\n"
        details_text += f"• Platform: {self.platform_info['system'].title()}\n"
        details_text += f"• Sürüm: {self.platform_info['release']}\n"
        details_text += f"• Mimari: {self.platform_info['architecture']}\n\n"
        
        details_text += f"📦 PAKET YÖNETİCİLERİ ({len(managers)} adet)\n"
        for manager_id, manager_info in managers.items():
            details_text += f"• {manager_info['name']}\n"
        
        messagebox.showinfo("Sistem Detayları", details_text)
    
    def cleanup_and_exit(self):
        """Temizlik yap ve çık"""
        self.schedule_manager.stop_scheduler()
        self.destroy()

# ---------- Uygulamayı Başlat ----------
if __name__ == "__main__":
    # Schedule kütüphanesi kontrolü
    try:
        import schedule
    except ImportError:
        print("❌ 'schedule' kütüphanesi gerekli. Yüklemek için:")
        print("pip install schedule")
        sys.exit(1)
    
    app = UniversalUpdaterApp()
    app.mainloop()


#!/usr/bin/env python3
"""
🚀 Evrensel Çapraz Platform Sistem Güncelleyici
Gelişmiş Loglama ve Geçmiş Kaydı ile
"""

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
import schedule
import logging
from logging.handlers import RotatingFileHandler
import csv
import sqlite3
from typing import Dict, List, Optional, Any
import gzip
import hashlib

# ---------- Gelişmiş Loglama Sistemi ----------
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
        # Logger'ı oluştur
        self.logger = logging.getLogger('SystemUpdater')
        self.logger.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Dosya handler (dönen loglar)
        log_file = os.path.join(self.log_dir, 'updater.log')
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024,  # 5MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # Konsol handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Handler'ları ekle
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log_update_start(self, update_type="manual"):
        """Güncelleme başlangıcını logla"""
        self.logger.info(f"🔧 GÜNCELLEME BAŞLATILDI - Tip: {update_type}")
        self.logger.info(f"🖥️  Sistem: {platform.system()} {platform.release()}")
        self.logger.info(f"🐍 Python: {platform.python_version()}")
        
    def log_update_result(self, success_count, total_commands, details):
        """Güncelleme sonucunu logla"""
        success_rate = (success_count / total_commands) * 100 if total_commands > 0 else 0
        self.logger.info(f"📊 GÜNCELLEME SONUCU - Başarı: {success_count}/{total_commands} (%{success_rate:.1f})")
        
        for detail in details:
            if "✅" in detail:
                self.logger.info(f"  {detail}")
            elif "❌" in detail or "⚠️" in detail:
                self.logger.warning(f"  {detail}")
            else:
                self.logger.info(f"  {detail}")
                
    def log_error(self, error_message, context=""):
        """Hata logla"""
        if context:
            self.logger.error(f"❌ {context} - {error_message}")
        else:
            self.logger.error(f"❌ {error_message}")
            
    def log_warning(self, warning_message, context=""):
        """Uyarı logla"""
        if context:
            self.logger.warning(f"⚠️ {context} - {warning_message}")
        else:
            self.logger.warning(f"⚠️ {warning_message}")
            
    def log_info(self, info_message, context=""):
        """Bilgi logla"""
        if context:
            self.logger.info(f"ℹ️  {context} - {info_message}")
        else:
            self.logger.info(f"ℹ️  {info_message}")

# ---------- Geçmiş Kaydı Sistemi ----------
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
        
        # Ana güncelleme geçmişi tablosu
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
        
        # Detaylı komut geçmişi tablosu
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
        
        # Sistem istatistikleri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_updates INTEGER DEFAULT 0,
                successful_updates INTEGER DEFAULT 0,
                total_commands INTEGER DEFAULT 0,
                successful_commands INTEGER DEFAULT 0,
                total_duration REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def start_update_session(self, update_type="manual") -> int:
        """Yeni güncelleme oturumu başlat ve ID döndür"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        system_info = json.dumps({
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'python_version': platform.python_version()
        })
        
        cursor.execute('''
            INSERT INTO update_sessions 
            (timestamp, update_type, success_count, total_commands, duration_seconds, system_info, status)
            VALUES (?, ?, 0, 0, 0, ?, 'running')
        ''', (datetime.now().isoformat(), update_type, system_info))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
        
    def log_command_result(self, session_id: int, command_name: str, command_text: str, 
                          status: str, return_code: int, output: str, error: str, 
                          duration: float):
        """Komut sonucunu kaydet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO command_history 
            (session_id, command_name, command_text, status, return_code, output, error, duration_seconds, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, command_name, command_text, status, return_code, 
              output[:1000] if output else '', error[:1000] if error else '', 
              duration, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
    def complete_update_session(self, session_id: int, success_count: int, 
                               total_commands: int, duration: float, status: str = "completed"):
        """Güncelleme oturumunu tamamla"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE update_sessions 
            SET success_count = ?, total_commands = ?, duration_seconds = ?, status = ?
            WHERE id = ?
        ''', (success_count, total_commands, duration, status, session_id))
        
        # İstatistikleri güncelle
        self.update_statistics(success_count, total_commands, duration)
        
        conn.commit()
        conn.close()
        
    def update_statistics(self, success_count: int, total_commands: int, duration: float):
        """Sistem istatistiklerini güncelle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT * FROM system_stats WHERE date = ?
        ''', (today,))
        
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE system_stats 
                SET total_updates = total_updates + 1,
                    successful_updates = successful_updates + ?,
                    total_commands = total_commands + ?,
                    successful_commands = successful_commands + ?,
                    total_duration = total_duration + ?
                WHERE date = ?
            ''', (1 if success_count == total_commands else 0, total_commands, success_count, duration, today))
        else:
            cursor.execute('''
                INSERT INTO system_stats 
                (date, total_updates, successful_updates, total_commands, successful_commands, total_duration)
                VALUES (?, 1, ?, ?, ?, ?)
            ''', (today, 1 if success_count == total_commands else 0, total_commands, success_count, duration))
        
        conn.commit()
        conn.close()
        
    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Son güncelleme oturumlarını getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM update_sessions 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': row[0],
                'timestamp': row[1],
                'update_type': row[2],
                'success_count': row[3],
                'total_commands': row[4],
                'duration_seconds': row[5],
                'system_info': json.loads(row[6]),
                'status': row[7]
            })
        
        conn.close()
        return sessions
        
    def get_session_details(self, session_id: int) -> Dict:
        """Oturum detaylarını getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Oturum bilgisi
        cursor.execute('SELECT * FROM update_sessions WHERE id = ?', (session_id,))
        session_row = cursor.fetchone()
        
        if not session_row:
            return None
            
        session_info = {
            'id': session_row[0],
            'timestamp': session_row[1],
            'update_type': session_row[2],
            'success_count': session_row[3],
            'total_commands': session_row[4],
            'duration_seconds': session_row[5],
            'system_info': json.loads(session_row[6]),
            'status': session_row[7]
        }
        
        # Komut geçmişi
        cursor.execute('''
            SELECT * FROM command_history 
            WHERE session_id = ? 
            ORDER BY timestamp
        ''', (session_id,))
        
        commands = []
        for row in cursor.fetchall():
            commands.append({
                'id': row[0],
                'command_name': row[2],
                'command_text': row[3],
                'status': row[4],
                'return_code': row[5],
                'output': row[6],
                'error': row[7],
                'duration_seconds': row[8],
                'timestamp': row[9]
            })
        
        session_info['commands'] = commands
        conn.close()
        return session_info
        
    def get_statistics(self, days: int = 30) -> Dict:
        """İstatistikleri getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT 
                SUM(total_updates) as total_updates,
                SUM(successful_updates) as successful_updates,
                SUM(total_commands) as total_commands,
                SUM(successful_commands) as successful_commands,
                SUM(total_duration) as total_duration
            FROM system_stats 
            WHERE date >= ?
        ''', (start_date,))
        
        result = cursor.fetchone()
        
        stats = {
            'total_updates': result[0] or 0,
            'successful_updates': result[1] or 0,
            'total_commands': result[2] or 0,
            'successful_commands': result[3] or 0,
            'total_duration': result[4] or 0,
            'success_rate_updates': (result[1] / result[0] * 100) if result[0] else 0,
            'success_rate_commands': (result[3] / result[2] * 100) if result[2] else 0
        }
        
        conn.close()
        return stats

# ---------- Geçmiş Görüntüleme Penceresi ----------
class HistoryViewerWindow(ctk.CTkToplevel):
    def __init__(self, parent, history_manager: UpdateHistoryManager):
        super().__init__(parent)
        self.history_manager = history_manager
        
        self.title("📊 Güncelleme Geçmişi")
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        self.load_history()
        
    def setup_ui(self):
        # Sekmeler
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tabview.add("📋 Son Güncellemeler")
        self.tabview.add("📈 İstatistikler")
        self.tabview.add("🔍 Detaylı Görünüm")
        
        self.setup_recent_tab()
        self.setup_stats_tab()
        self.setup_details_tab()
        
    def setup_recent_tab(self):
        # Son güncellemeler listesi
        frame = self.tabview.tab("📋 Son Güncellemeler")
        
        # Başlık
        title_label = ctk.CTkLabel(frame, text="Son 10 Güncelleme", 
                                  font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Liste kutusu
        self.session_listbox = ctk.CTkTextbox(frame, width=700, height=400)
        self.session_listbox.pack(pady=10, fill="both", expand=True)
        self.session_listbox.configure(state="disabled")
        
    def setup_stats_tab(self):
        # İstatistikler
        frame = self.tabview.tab("📈 İstatistikler")
        
        self.stats_text = ctk.CTkTextbox(frame, width=700, height=400)
        self.stats_text.pack(pady=10, fill="both", expand=True)
        self.stats_text.configure(state="disabled")
        
    def setup_details_tab(self):
        # Detaylı görünüm
        frame = self.tabview.tab("🔍 Detaylı Görünüm")
        
        # Seçim
        selection_frame = ctk.CTkFrame(frame)
        selection_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(selection_frame, text="Oturum ID:").pack(side="left", padx=5)
        self.session_id_entry = ctk.CTkEntry(selection_frame, width=100)
        self.session_id_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(selection_frame, text="Yükle", 
                     command=self.load_session_details).pack(side="left", padx=10)
        
        # Detaylar
        self.details_text = ctk.CTkTextbox(frame, width=700, height=350)
        self.details_text.pack(pady=10, fill="both", expand=True)
        self.details_text.configure(state="disabled")
        
    def load_history(self):
        """Geçmişi yükle"""
        self.load_recent_sessions()
        self.load_statistics()
        
    def load_recent_sessions(self):
        """Son oturumları yükle"""
        sessions = self.history_manager.get_recent_sessions(10)
        
        self.session_listbox.configure(state="normal")
        self.session_listbox.delete("1.0", "end")
        
        if not sessions:
            self.session_listbox.insert("end", "Henüz güncelleme geçmişi yok.\n")
        else:
            for session in sessions:
                timestamp = datetime.fromisoformat(session['timestamp'])
                success_rate = (session['success_count'] / session['total_commands'] * 100) if session['total_commands'] > 0 else 0
                
                self.session_listbox.insert("end", 
                    f"📅 {timestamp.strftime('%d.%m.%Y %H:%M')}\n")
                self.session_listbox.insert("end",
                    f"   Type: {session['update_type']} | "
                    f"Success: {session['success_count']}/{session['total_commands']} "
                    f"(%{success_rate:.1f}) | "
                    f"Duration: {session['duration_seconds']:.1f}s\n")
                self.session_listbox.insert("end", f"   Status: {session['status']}\n\n")
        
        self.session_listbox.configure(state="disabled")
        
    def load_statistics(self):
        """İstatistikleri yükle"""
        stats = self.history_manager.get_statistics(30)
        
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", "end")
        
        self.stats_text.insert("end", "📊 SON 30 GÜN İSTATİSTİKLERİ\n\n")
        self.stats_text.insert("end", f"• Toplam Güncelleme: {stats['total_updates']}\n")
        self.stats_text.insert("end", f"• Başarılı Güncelleme: {stats['successful_updates']}\n")
        self.stats_text.insert("end", f"• Başarı Oranı: %{stats['success_rate_updates']:.1f}\n\n")
        
        self.stats_text.insert("end", f"• Toplam Komut: {stats['total_commands']}\n")
        self.stats_text.insert("end", f"• Başarılı Komut: {stats['successful_commands']}\n")
        self.stats_text.insert("end", f"• Başarı Oranı: %{stats['success_rate_commands']:.1f}\n\n")
        
        total_hours = stats['total_duration'] / 3600
        self.stats_text.insert("end", f"• Toplam Süre: {total_hours:.2f} saat\n")
        
        self.stats_text.configure(state="disabled")
        
    def load_session_details(self):
        """Oturum detaylarını yükle"""
        try:
            session_id = int(self.session_id_entry.get())
            session_details = self.history_manager.get_session_details(session_id)
            
            if not session_details:
                messagebox.showerror("Hata", "Oturum bulunamadı!")
                return
                
            self.details_text.configure(state="normal")
            self.details_text.delete("1.0", "end")
            
            timestamp = datetime.fromisoformat(session_details['timestamp'])
            self.details_text.insert("end", f"📋 OTOURUM DETAYLARI - ID: {session_id}\n\n")
            self.details_text.insert("end", f"Zaman: {timestamp.strftime('%d.%m.%Y %H:%M:%S')}\n")
            self.details_text.insert("end", f"Tip: {session_details['update_type']}\n")
            self.details_text.insert("end", f"Durum: {session_details['status']}\n\n")
            
            self.details_text.insert("end", "🔧 ÇALIŞTIRILAN KOMUTLAR:\n\n")
            for cmd in session_details['commands']:
                status_icon = "✅" if cmd['status'] == 'success' else "❌"
                self.details_text.insert("end", 
                    f"{status_icon} {cmd['command_name']} ({cmd['duration_seconds']:.1f}s)\n")
                if cmd['error']:
                    self.details_text.insert("end", f"   Hata: {cmd['error']}\n")
                self.details_text.insert("end", "\n")
            
            self.details_text.configure(state="disabled")
            
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir oturum ID'si girin!")
        except Exception as e:
            messagebox.showerror("Hata", f"Detaylar yüklenemedi: {e}")

# ---------- Güncellenmiş Ana Uygulama ----------
class UniversalUpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Loglama ve geçmiş sistemleri
        self.logger = AdvancedLogger()
        self.history_manager = UpdateHistoryManager()
        
        # Platform ayarları
        self.platform_info = self.get_platform_info()
        
        # GUI ayarları
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        self.title("🚀 Evrensel Sistem Güncelleyici")
        self.geometry("500x500")
        
        # Paket yöneticisi
        self.package_manager = CrossPlatformPackageManager()
        
        # Zamanlama yöneticisi (önceki koddan)
        self.schedule_manager = ScheduledUpdateManager()
        
        self.setup_ui()
        self.logger.log_info("Uygulama başlatıldı", "SystemUpdater")
        
    def get_platform_info(self):
        """Platform bilgilerini getir"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'python_version': platform.python_version()
        }
        
    def setup_ui(self):
        # Başlık
        title_label = ctk.CTkLabel(self, text="🚀 Sistem Güncelleyici", 
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=15)
        
        # Platform bilgisi
        platform_label = ctk.CTkLabel(self, 
                                     text=f"Platform: {self.platform_info['system']} {self.platform_info['release']}", 
                                     font=("Arial", 12))
        platform_label.pack(pady=5)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=450, height=20)
        self.progress.set(0)
        self.progress.pack(pady=15)
        
        # Durum label
        self.status_label = ctk.CTkLabel(self, text="Sistem hazır", 
                                        font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        # Butonlar frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        # Güncelle butonu
        self.update_btn = ctk.CTkButton(button_frame, text="🔄 Güncelle",
                                       command=lambda: self.start_update(),
                                       font=("Arial", 12),
                                       width=100)
        self.update_btn.pack(side="left", padx=5)
        
        # Geçmiş butonu
        self.history_btn = ctk.CTkButton(button_frame, text="📊 Geçmiş",
                                        command=self.show_history,
                                        font=("Arial", 12),
                                        width=100)
        self.history_btn.pack(side="left", padx=5)
        
        # Zamanlama butonu
        self.schedule_btn = ctk.CTkButton(button_frame, text="⏰ Zamanlama",
                                         command=self.show_schedule_settings,
                                         font=("Arial", 12),
                                         width=100)
        self.schedule_btn.pack(side="left", padx=5)
        
        # Çıktı alanı
        self.output_text = ctk.CTkTextbox(self, width=460, height=180)
        self.output_text.pack(pady=10, fill="x", padx=20)
        self.output_text.insert("1.0", "Güncelleme detayları burada görünecek...\n")
        self.output_text.configure(state="disabled")
        
        # Çıkış butonu
        self.quit_btn = ctk.CTkButton(self, text="❌ Çıkış",
                                     command=self.cleanup_and_exit,
                                     fg_color="red",
                                     font=("Arial", 12))
        self.quit_btn.pack(pady=10)
        
    def show_history(self):
        """Geçmiş penceresini aç"""
        HistoryViewerWindow(self, self.history_manager)
        
    def start_update(self, update_type="manual"):
        """Güncellemeyi başlat"""
        start_time = time.time()
        
        # Loglama başlat
        self.logger.log_update_start(update_type)
        session_id = self.history_manager.start_update_session(update_type)
        
        self.progress.set(0)
        self.status_label.configure(text="Güncelleme başlatılıyor...")
        self.update_btn.configure(state="disabled")
        
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", f"🔧 Güncelleme başlatıldı... (ID: {session_id})\n")
        self.output_text.configure(state="disabled")
        
        # Thread'de çalıştır
        thread = threading.Thread(target=lambda: self.run_update_thread(session_id, start_time, update_type))
        thread.daemon = True
        thread.start()
        
    def run_update_thread(self, session_id: int, start_time: float, update_type: str):
        """Güncelleme thread'i"""
        managers = self.package_manager.get_available_managers()
        
        if not managers:
            error_msg = "Paket yöneticisi bulunamadı"
            self.logger.log_error(error_msg)
            self.history_manager.complete_update_session(session_id, 0, 0, 0, "failed")
            self.update_done(error_msg, [], session_id, start_time, update_type)
            return
        
        total_commands = sum(len(mgr['commands']) for mgr in managers.values())
        completed = 0
        success_count = 0
        details = []
        
        for manager_id, manager_info in managers.items():
            for command in manager_info['commands']:
                completed += 1
                progress = (completed / total_commands) * 100
                command_start_time = time.time()
                
                self.update_progress(progress, f"{manager_info['name']} - {command[0]}")
                
                try:
                    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
                    command_duration = time.time() - command_start_time
                    
                    if result.returncode == 0:
                        success_count += 1
                        status = "success"
                        details.append(f"✅ {manager_info['name']} - Başarılı")
                    else:
                        status = "failed"
                        error_msg = result.stderr[:100] if result.stderr else "Bilinmeyen hata"
                        details.append(f"❌ {manager_info['name']} - Hata: {error_msg}")
                    
                    # Komut sonucunu geçmişe kaydet
                    self.history_manager.log_command_result(
                        session_id, manager_info['name'], ' '.join(command),
                        status, result.returncode, result.stdout, result.stderr,
                        command_duration
                    )
                        
                except Exception as e:
                    command_duration = time.time() - command_start_time
                    error_msg = str(e)
                    details.append(f"⚠️ {manager_info['name']} - Hata: {error_msg}")
                    
                    self.history_manager.log_command_result(
                        session_id, manager_info['name'], ' '.join(command),
                        "error", -1, "", error_msg, command_duration
                    )
                
                time.sleep(1)
        
        total_duration = time.time() - start_time
        self.history_manager.complete_update_session(
            session_id, success_count, total_commands, total_duration, "completed"
        )
        
        summary = f"🎉 Güncelleme tamamlandı! {success_count}/{total_commands} başarılı"
        self.logger.log_update_result(success_count, total_commands, details)
        self.update_done(summary, details, session_id, start_time, update_type)
    
    def update_progress(self, percent, detail):
        self.progress.set(percent / 100)
        self.status_label.configure(text=f"Güncelleniyor... %{int(percent)}")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"⏳ {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def update_done(self, message, details, session_id, start_time, update_type):
        total_duration = time.time() - start_time
        
        self.progress.set(1.0)
        self.status_label.configure(text="Tamamlandı!")
        self.update_btn.configure(state="normal")
        
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"\n🎉 {message}\n")
        self.output_text.insert("end", f"⏱️  Toplam süre: {total_duration:.1f}s\n")
        for detail in details:
            self.output_text.insert("end", f"• {detail}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
        
        messagebox.showinfo("Güncelleme Tamamlandı", f"{message}\nSüre: {total_duration:.1f}s")
    
    def show_schedule_settings(self):
        """Zamanlama ayarları (önceki koddan)"""
        # Bu fonksiyon önceki zamanlama kodundan gelecek
        pass
        
    def cleanup_and_exit(self):
        """Temizlik yap ve çık"""
        self.logger.log_info("Uygulama kapatılıyor", "SystemUpdater")
        self.destroy()

# ---------- Platform Tespiti (Önceki koddan) ----------
class PlatformDetector:
    @staticmethod
    def get_platform_info():
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

# ---------- Paket Yöneticisi (Önceki koddan) ----------
class CrossPlatformPackageManager:
    def get_available_managers(self):
        # Önceki kodun aynısı
        return {}

# ---------- Zamanlama Yöneticisi (Önceki koddan) ----------
class ScheduledUpdateManager:
    def start_scheduler(self, callback):
        # Önceki kodun aynısı
        pass

# ---------- Uygulamayı Başlat ----------
if __name__ == "__main__":
    app = UniversalUpdaterApp()
    app.mainloop()
