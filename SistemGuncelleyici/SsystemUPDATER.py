import os
import platform
import shutil
import subprocess
import threading
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# ---------- Sistem Bilgileri ----------
def get_system_info():
    """Detaylı sistem bilgilerini topla"""
    info = {
        "İşletim Sistemi": f"{platform.system()} {platform.release()}",
        "Python Versiyonu": platform.python_version(),
        "İşlemci": platform.processor(),
        "Mimari": platform.architecture()[0],
        "Kullanıcı": os.getlogin(),
        "Çalışma Dizini": os.getcwd()
    }
    return info

def get_package_managers():
    """Mevcut paket yöneticilerini kontrol et"""
    managers = {}
    
    if shutil.which("winget"):
        managers["Windows Package Manager (winget)"] = "✅ Mevcut"
    else:
        managers["Windows Package Manager (winget)"] = "❌ Yok"
    
    if shutil.which("choco"):
        managers["Chocolatey"] = "✅ Mevcut"
    else:
        managers["Chocolatey"] = "❌ Yok"
    
    return managers

# ---------- Güncelleme Sistemi ----------
def which(cmd):
    return shutil.which(cmd) is not None

def build_commands():
    system = platform.system().lower()
    cmds = []
    
    if "windows" in system:
        if which("winget"):
            cmds.append({
                "name": "Windows Paket Yöneticisi", 
                "cmd": ["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements"],
                "description": "Microsoft Store ve sistem uygulamalarını günceller"
            })
        if which("choco"):
            cmds.append({
                "name": "Chocolatey",
                "cmd": ["choco", "upgrade", "all", "-y"],
                "description": "Chocolatey ile yüklenen tüm yazılımları günceller"
            })
    
    return cmds

def run_updates(callback_progress, callback_done):
    cmds = build_commands()
    if not cmds:
        callback_done("❌ Sisteminiz için paket yöneticisi bulunamadı", [])
        return
    
    total = len(cmds)
    completed = 0
    success_count = 0
    details = []

    for cmd_info in cmds:
        completed += 1
        progress = (completed / total) * 100
        callback_progress(progress, cmd_info["name"])
        
        try:
            result = subprocess.run(
                cmd_info["cmd"], 
                capture_output=True, 
                text=True, 
                shell=False,
                timeout=300  # 5 dakika timeout
            )
            
            if result.returncode == 0:
                success_count += 1
                details.append(f"✅ {cmd_info['name']} - Başarılı")
            else:
                details.append(f"❌ {cmd_info['name']} - Hata: {result.stderr[:100]}...")
                
        except subprocess.TimeoutExpired:
            details.append(f"⏰ {cmd_info['name']} - Zaman aşımı")
        except Exception as e:
            details.append(f"⚠️ {cmd_info['name']} - Hata: {str(e)}")
    
    callback_done(f"✅ {success_count}/{total} güncelleme başarılı!", details)

# ---------- Detaylı Bilgi Penceresi ----------
class DetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🔍 Sistem Detayları")
        self.geometry("600x500")
        self.transient(parent)
        self.grab_set()
        
        # Sekmeler oluştur
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sistem Bilgileri sekmesi
        self.tabview.add("Sistem Bilgileri")
        self.setup_system_tab()
        
        # Paket Yöneticileri sekmesi
        self.tabview.add("Paket Yöneticileri")
        self.setup_packages_tab()
        
        # Güncelleme Geçmişi sekmesi
        self.tabview.add("Güncelleme Geçmişi")
        self.setup_history_tab()
    
    def setup_system_tab(self):
        # Sistem bilgilerini göster
        system_info = get_system_info()
        
        text_widget = ctk.CTkTextbox(self.tabview.tab("Sistem Bilgileri"))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        for key, value in system_info.items():
            text_widget.insert("end", f"🔹 {key}: {value}\n\n")
        text_widget.configure(state="disabled")
    
    def setup_packages_tab(self):
        # Paket yöneticilerini göster
        managers = get_package_managers()
        
        text_widget = ctk.CTkTextbox(self.tabview.tab("Paket Yöneticileri"))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.insert("end", "📦 SİSTEMDE BULUNAN PAKET YÖNETİCİLERİ\n\n")
        for manager, status in managers.items():
            text_widget.insert("end", f"{status} {manager}\n\n")
        
        text_widget.insert("end", "\n💡 ÖNERİLER:\n")
        text_widget.insert("end", "• Windows: winget (otomatik gelir)\n")
        text_widget.insert("end", "• Chocolatey: https://chocolatey.org/install\n")
        text_widget.configure(state="disabled")
    
    def setup_history_tab(self):
        # Güncelleme geçmişi (basit versiyon)
        text_widget = ctk.CTkTextbox(self.tabview.tab("Güncelleme Geçmişi"))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.insert("end", "📊 SON GÜNCELLEME BİLGİLERİ\n\n")
        text_widget.insert("end", "• Bu özellik geliştirme aşamasındadır\n")
        text_widget.insert("end", "• Gelecek sürümlerde detaylı geçmiş eklenecek\n")
        text_widget.configure(state="disabled")

# ---------- Ana Uygulama ----------
class UpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🚀 Sistem Güncelleyici")
        self.geometry("500x400")
        
        # Başlık
        title_label = ctk.CTkLabel(self, text="Sistem Güncelleyici", 
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        # Sistem bilgisi
        sys_info = f"{platform.system()} {platform.release()}"
        sys_label = ctk.CTkLabel(self, text=sys_info, font=("Arial", 12))
        sys_label.pack(pady=5)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=400, height=20)
        self.progress.set(0)
        self.progress.pack(pady=20)
        
        # Durum label
        self.status_label = ctk.CTkLabel(self, text="Hazır", 
                                        font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        # Butonlar frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        
        # Güncelle butonu
        self.update_btn = ctk.CTkButton(button_frame, text="🔄 Güncelle",
                                       command=self.start_update,
                                       font=("Arial", 14),
                                       width=120)
        self.update_btn.pack(side="left", padx=10)
        
        # Detaylar butonu
        self.details_btn = ctk.CTkButton(button_frame, text="🔍 Detayları Gör",
                                        command=self.show_details,
                                        font=("Arial", 14),
                                        width=120)
        self.details_btn.pack(side="left", padx=10)
        
        # Çıkış butonu
        self.quit_btn = ctk.CTkButton(self, text="❌ Çıkış",
                                     command=self.destroy,
                                     fg_color="red",
                                     font=("Arial", 12))
        self.quit_btn.pack(pady=10)
        
        # Detaylı sonuçlar için text alanı
        self.details_text = ctk.CTkTextbox(self, width=450, height=100)
        self.details_text.pack(pady=10, fill="x", padx=25)
        self.details_text.insert("1.0", "Güncelleme detayları burada görünecek...")
        self.details_text.configure(state="disabled")

    def show_details(self):
        """Detaylı bilgi penceresini aç"""
        DetailsWindow(self)

    def start_update(self):
        self.progress.set(0)
        self.status_label.configure(text="Güncelleme başlatılıyor...")
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", "Güncelleme başlatıldı...\n")
        self.details_text.configure(state="disabled")
        self.update_btn.configure(state="disabled")
        
        thread = threading.Thread(target=self.run_update_thread)
        thread.daemon = True
        thread.start()

    def run_update_thread(self):
        run_updates(self.update_progress, self.update_done)

    def update_progress(self, percent, detail):
        self.progress.set(percent / 100)
        self.status_label.configure(text=f"Güncelleniyor... %{int(percent)}")
        
        # Detayları güncelle
        self.details_text.configure(state="normal")
        self.details_text.insert("end", f"⏳ {detail}...\n")
        self.details_text.see("end")
        self.details_text.configure(state="disabled")

    def update_done(self, message, details):
        self.progress.set(1.0)
        self.status_label.configure(text="Tamamlandı!")
        self.update_btn.configure(state="normal")
        
        # Detaylı sonuçları göster
        self.details_text.configure(state="normal")
        self.details_text.insert("end", f"\n🎉 {message}\n")
        for detail in details:
            self.details_text.insert("end", f"• {detail}\n")
        self.details_text.configure(state="disabled")
        
        messagebox.showinfo("Güncelleme Tamamlandı", message)

# ---------- Uygulamayı Başlat ----------
if __name__ == "__main__":
    # .py dosyası olarak çalıştığında direkt açılsın
    app = UpdaterApp()
    app.mainloop()