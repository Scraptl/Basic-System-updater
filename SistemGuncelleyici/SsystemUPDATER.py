#!/usr/bin/env python3
"""
🚀 Evrensel Çapraz Platform Sistem Güncelleyici
Windows, macOS ve Linux için tam destek
"""

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
