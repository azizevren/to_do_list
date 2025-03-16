import os
import json
from datetime import datetime

class TodoApp:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()
    
    def load_tasks(self):
        """Görevleri JSON dosyasından yükler"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.tasks = json.load(file)
                print("Görevler başarıyla yüklendi.")
            except Exception as e:
                print(f"Görevler yüklenirken hata oluştu: {e}")
                self.tasks = []
        else:
            print("Görev dosyası bulunamadı. Yeni bir dosya oluşturulacak.")
            self.tasks = []
    
    def save_tasks(self):
        """Görevleri JSON dosyasına kaydeder"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
            print("Görevler başarıyla kaydedildi.")
        except Exception as e:
            print(f"Görevler kaydedilirken hata oluştu: {e}")
    
    def add_task(self):
        """Yeni görev ekler"""
        title = input("Görev başlığı: ")
        description = input("Görev açıklaması: ")
        
        # Tarih girişi ve doğrulama
        while True:
            due_date_str = input("Son tarih (GG.AA.YYYY): ")
            if due_date_str.strip() == "":
                due_date = ""
                break
            
            try:
                due_date = datetime.strptime(due_date_str, "%d.%m.%Y").strftime("%d.%m.%Y")
                break
            except ValueError:
                print("Geçersiz tarih formatı! Lütfen GG.AA.YYYY formatında girin.")
        
        # Öncelik seviyesi
        priority_options = {"1": "Düşük", "2": "Orta", "3": "Yüksek"}
        print("Öncelik seçin:")
        for key, value in priority_options.items():
            print(f"{key}. {value}")
        
        while True:
            priority_choice = input("Seçiminiz (1-3): ")
            if priority_choice in priority_options:
                priority = priority_options[priority_choice]
                break
            print("Geçersiz seçim! Lütfen 1-3 arasında seçin.")
        
        # Yeni görev oluştur
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "status": "Beklemede",
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        print(f"'{title}' görevi başarıyla eklendi.")
    
    def list_tasks(self):
        """Tüm görevleri listeler"""
        if not self.tasks:
            print("Henüz hiç görev eklenmemiş.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<4}{'Başlık':<20}{'Durum':<12}{'Öncelik':<12}{'Son Tarih':<15}")
        print("-"*80)
        
        for task in self.tasks:
            print(f"{task['id']:<4}{task['title'][:19]:<20}{task['status']:<12}{task['priority']:<12}{task['due_date']:<15}")
        
        print("="*80 + "\n")
    
    def view_task(self):
        """Belirli bir görevi ayrıntılı olarak görüntüler"""
        self.list_tasks()
        if not self.tasks:
            return
            
        task_id = input("Görüntülemek istediğiniz görevin ID'sini girin: ")
        try:
            task_id = int(task_id)
            task = next((t for t in self.tasks if t["id"] == task_id), None)
            
            if task:
                print("\n" + "="*50)
                print(f"ID: {task['id']}")
                print(f"Başlık: {task['title']}")
                print(f"Açıklama: {task['description']}")
                print(f"Durum: {task['status']}")
                print(f"Öncelik: {task['priority']}")
                print(f"Son Tarih: {task['due_date']}")
                print(f"Oluşturulma Tarihi: {task['created_at']}")
                print("="*50 + "\n")
            else:
                print(f"ID {task_id} olan görev bulunamadı.")
        except ValueError:
            print("Geçersiz ID! Lütfen bir sayı girin.")
    
    def update_task_status(self):
        """Görev durumunu günceller"""
        self.list_tasks()
        if not self.tasks:
            return
            
        task_id = input("Durumunu güncellemek istediğiniz görevin ID'sini girin: ")
        try:
            task_id = int(task_id)
            task = next((t for t in self.tasks if t["id"] == task_id), None)
            
            if task:
                status_options = {"1": "Beklemede", "2": "Devam Ediyor", "3": "Tamamlandı"}
                print("Yeni durum seçin:")
                for key, value in status_options.items():
                    print(f"{key}. {value}")
                
                while True:
                    status_choice = input("Seçiminiz (1-3): ")
                    if status_choice in status_options:
                        task["status"] = status_options[status_choice]
                        self.save_tasks()
                        print(f"Görev durumu '{task['status']}' olarak güncellendi.")
                        break
                    print("Geçersiz seçim! Lütfen 1-3 arasında seçin.")
            else:
                print(f"ID {task_id} olan görev bulunamadı.")
        except ValueError:
            print("Geçersiz ID! Lütfen bir sayı girin.")
    
    def delete_task(self):
        """Görevi siler"""
        self.list_tasks()
        if not self.tasks:
            return
            
        task_id = input("Silmek istediğiniz görevin ID'sini girin: ")
        try:
            task_id = int(task_id)
            task = next((t for t in self.tasks if t["id"] == task_id), None)
            
            if task:
                confirm = input(f"'{task['title']}' görevini silmek istediğinizden emin misiniz? (e/h): ")
                if confirm.lower() == 'e':
                    self.tasks.remove(task)
                    # ID'leri yeniden düzenle
                    for i, t in enumerate(self.tasks):
                        t["id"] = i + 1
                    self.save_tasks()
                    print("Görev başarıyla silindi.")
                else:
                    print("Silme işlemi iptal edildi.")
            else:
                print(f"ID {task_id} olan görev bulunamadı.")
        except ValueError:
            print("Geçersiz ID! Lütfen bir sayı girin.")
    
    def search_tasks(self):
        """Görevlerde arama yapar"""
        if not self.tasks:
            print("Henüz hiç görev eklenmemiş.")
            return
            
        search_term = input("Arama terimi: ").lower()
        found_tasks = [t for t in self.tasks if search_term in t["title"].lower() or search_term in t["description"].lower()]
        
        if found_tasks:
            print("\n" + "="*80)
            print(f"{'ID':<4}{'Başlık':<20}{'Durum':<12}{'Öncelik':<12}{'Son Tarih':<15}")
            print("-"*80)
            
            for task in found_tasks:
                print(f"{task['id']:<4}{task['title'][:19]:<20}{task['status']:<12}{task['priority']:<12}{task['due_date']:<15}")
            
            print("="*80 + "\n")
        else:
            print(f"'{search_term}' ile eşleşen görev bulunamadı.")
    
    def display_menu(self):
        """Ana menüyü gösterir"""
        print("\n📋 TO-DO LİSTESİ UYGULAMASI 📋")
        print("1. Görevleri Listele")
        print("2. Görev Ekle")
        print("3. Görev Detaylarını Görüntüle")
        print("4. Görev Durumunu Güncelle")
        print("5. Görev Sil")
        print("6. Görevlerde Ara")
        print("0. Çıkış")
    
    def run(self):
        """Uygulamayı çalıştırır"""
        while True:
            self.display_menu()
            choice = input("\nSeçiminiz: ")
            
            if choice == "1":
                self.list_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.view_task()
            elif choice == "4":
                self.update_task_status()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                self.search_tasks()
            elif choice == "0":
                print("Uygulamadan çıkılıyor...")
                break
            else:
                print("Geçersiz seçim! Lütfen tekrar deneyin.")


if __name__ == "__main__":
    app = TodoApp()
    app.run()