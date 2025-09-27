import os
import platform
import shutil
import subprocess
import threading
import time
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# ---------- Ayarlar ----------
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# ---------- Yardımcı Fonksiyonlar ----------
def which(cmd):
    return shutil.which(cmd) is not None

def run_command(cmd, timeout=300):
    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            timeout=timeout,
            shell=False
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# ---------- Komut Listesi ----------
def build_commands():
    system = platform.system().lower()
    cmds = []

    if "windows" in system:
        if which("winget"):
            cmds.append({
                "name": "Windows Package Manager", 
                "cmd": ["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements"],
                "timeout": 600
            })
        if which("choco"):
            cmds.append({
                "name": "Chocolatey",
                "cmd": ["choco", "upgrade", "all", "-y"], 
                "timeout": 600
            })

    elif "darwin" in system:
        if which("brew"):
            cmds.extend([
                {"name": "Homebrew Update", "cmd": ["brew", "update"], "timeout": 300},
                {"name": "Homebrew Upgrade", "cmd": ["brew", "upgrade"], "timeout": 600},
                {"name": "Homebrew Cleanup", "cmd": ["brew", "cleanup"], "timeout": 300}
            ])

    elif "linux" in system:
        if which("apt") or which("apt-get"):
            apt = "apt" if which("apt") else "apt-get"
            cmds.extend([
                {"name": "APT Update", "cmd": ["sudo", apt, "update"], "timeout": 300},
                {"name": "APT Upgrade", "cmd": ["sudo", apt, "upgrade", "-y"], "timeout": 600},
            ])

    return cmds

# ---------- Güncelleme İşlemi ----------
def run_updates(callback_progress, callback_done):
    cmds = build_commands()
    if not cmds:
        callback_done("❌ Sistem için paket yöneticisi bulunamadı")
        return

    total = len(cmds)
    completed = 0
    success_count = 0
    fail_count = 0
    results = []

    for cmd_info in cmds:
        # İlerleme güncelle
        completed += 1
        progress = (completed / total) * 100
        callback_progress(progress, f"{cmd_info['name']} çalıştırılıyor...")

        # Komutu çalıştır
        success, output, error = run_command(cmd_info["cmd"], cmd_info["timeout"])
        
        if success:
            success_count += 1
            results.append(f"✅ {cmd_info['name']} - Başarılı")
        else:
            fail_count += 1
            results.append(f"❌ {cmd_info['name']} - Başarısız")

    # Sonuçları hazırla
    summary = f"""🎉 GÜNCELLEME TAMAMLANDI

📊 SONUÇLAR:
✅ Başarılı: {success_count}
❌ Başarısız: {fail_count}

🔧 DETAYLAR:
"""
    summary += "\n".join(results)
    
    callback_done(summary)

# ---------- GUI Sınıfı ----------
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
        
        # Detay label
        self.detail_label = ctk.CTkLabel(self, text="", 
                                        font=("Arial", 10),
                                        text_color="gray")
        self.detail_label.pack(pady=5)
        
        # Buton
        self.update_btn = ctk.CTkButton(self, text="🔄 Güncellemeleri Çalıştır",
                                       command=self.start_update,
                                       font=("Arial", 14),
                                       height=40)
        self.update_btn.pack(pady=20)
        
        # Çıkış butonu
        self.quit_btn = ctk.CTkButton(self, text="❌ Çıkış",
                                     command=self.destroy,
                                     fg_color="red",
                                     font=("Arial", 12))
        self.quit_btn.pack(pady=10)

    def start_update(self):
        self.progress.set(0)
        self.status_label.configure(text="Güncelleme başlatılıyor...")
        self.detail_label.configure(text="")
        self.update_btn.configure(state="disabled")
        
        thread = threading.Thread(target=self.run_update_thread)
        thread.daemon = True
        thread.start()

    def run_update_thread(self):
        run_updates(self.update_progress, self.update_done)

    def update_progress(self, percent, detail):
        self.progress.set(percent / 100)
        self.status_label.configure(text=f"Güncelleniyor... %{int(percent)}")
        self.detail_label.configure(text=detail)

    def update_done(self, result):
        self.progress.set(1.0)
        self.status_label.configure(text="Güncelleme tamamlandı!")
        self.update_btn.configure(state="normal")
        
        messagebox.showinfo("Güncelleme Tamamlandı", result)

# ---------- Ana Program ----------
if __name__ == "__main__":
    app = UpdaterApp()
    app.mainloop()

    #!/usr/bin/env python3

import os
from PIL import Image, ImageDraw

# ---------- Icon Oluşturucu  ----------
def create_icon():
    try:
        # Basit bir icon oluştur
        img = Image.new('RGB', (64, 64), color='#1f538d')
        draw = ImageDraw.Draw(img)
        draw.rectangle([15, 15, 49, 49], outline='white', width=3)
        draw.polygon([(32, 22), (27, 35), (37, 35)], fill='white')
        img.save('icon.ico', format='ICO')
        print("✅ Icon oluşturuldu")
        return True
    except Exception as e:
        print("⚠️ Icon oluşturulamadı, iconsuz devam edilecek")
        return False

# Icon'u oluştur (eğer yoksa)
if not os.path.exists('icon.ico'):
    create_icon()

import platform
import shutil
import subprocess
import threading
