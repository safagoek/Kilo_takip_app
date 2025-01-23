import subprocess
import sys
import os

def install_dependencies():
    dependencies = ['customtkinter', 'matplotlib']
    missing_packages = []
    
    for package in dependencies:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)

def check_and_create_database():
    if not os.path.exists('diet_tracker.db'):
        print("Veritabanı oluşturuluyor...")

import customtkinter as ctk
import sqlite3
from datetime import datetime, date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from tkinter import messagebox
import tkinter as tk

class DatePicker(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_date = date.today()
        self.selected_date = self.current_date
        
        self.date_str = ctk.StringVar(value=self.current_date.strftime("%d-%m-%Y"))
        self.date_label = ctk.CTkLabel(self, 
                                     textvariable=self.date_str,
                                     font=("Arial", 14, "bold"))
        self.date_label.pack(pady=5)

        self.month_year_frame = ctk.CTkFrame(self)
        self.month_year_frame.pack(pady=5)

        self.prev_month = ctk.CTkButton(self.month_year_frame, 
                                      text="←", 
                                      width=30,
                                      command=self.previous_month)
        self.prev_month.pack(side="left", padx=5)

        months = list(calendar.month_name)[1:]
        self.month_var = ctk.StringVar(value=calendar.month_name[self.current_date.month])
        self.month_menu = ctk.CTkOptionMenu(self.month_year_frame,
                                          values=months,
                                          variable=self.month_var,
                                          command=self.update_calendar)
        self.month_menu.pack(side="left", padx=5)

        years = [str(year) for year in range(2020, 2031)]
        self.year_var = ctk.StringVar(value=str(self.current_date.year))
        self.year_menu = ctk.CTkOptionMenu(self.month_year_frame,
                                         values=years,
                                         variable=self.year_var,
                                         command=self.update_calendar)
        self.year_menu.pack(side="left", padx=5)

        self.next_month = ctk.CTkButton(self.month_year_frame, 
                                      text="→", 
                                      width=30,
                                      command=self.next_month)
        self.next_month.pack(side="left", padx=5)

        self.days_frame = ctk.CTkFrame(self)
        self.days_frame.pack(pady=5)

        self.create_calendar()

    def create_calendar(self):
        days = ['Pt', 'Sa', 'Ça', 'Pe', 'Cu', 'Ct', 'Pa']
        for i, day in enumerate(days):
            lbl = ctk.CTkLabel(self.days_frame, text=day)
            lbl.grid(row=0, column=i, padx=2, pady=2)

        self.update_calendar()

    def update_calendar(self, *args):
        for widget in self.days_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        year = int(self.year_var.get())
        month = list(calendar.month_name).index(self.month_var.get())
        cal = calendar.monthcalendar(year, month)

        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:
                    btn = ctk.CTkButton(self.days_frame, 
                                      text=str(day),
                                      width=30,
                                      height=30,
                                      command=lambda d=day: self.select_date(d))
                    btn.grid(row=i+1, column=j, padx=2, pady=2)

    def select_date(self, day):
        year = int(self.year_var.get())
        month = list(calendar.month_name).index(self.month_var.get())
        self.selected_date = date(year, month, day)
        self.date_str.set(self.selected_date.strftime("%d-%m-%Y"))

    def previous_month(self):
        current_month_idx = list(calendar.month_name).index(self.month_var.get())
        if current_month_idx > 1:
            self.month_var.set(calendar.month_name[current_month_idx - 1])
        else:
            current_year = int(self.year_var.get())
            self.year_var.set(str(current_year - 1))
            self.month_var.set(calendar.month_name[12])
        self.update_calendar()

    def next_month(self):
        current_month_idx = list(calendar.month_name).index(self.month_var.get())
        if current_month_idx < 12:
            self.month_var.set(calendar.month_name[current_month_idx + 1])
        else:
            current_year = int(self.year_var.get())
            self.year_var.set(str(current_year + 1))
            self.month_var.set(calendar.month_name[1])
        self.update_calendar()

    def get_date(self):
        return self.selected_date

class ClientNotes(ctk.CTkToplevel):
    _instance = None

    def __new__(cls, parent, client_id, client_name):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent, client_id, client_name):
        if not hasattr(self, 'initialized'):
            super().__init__(parent)
            self.title(f"Danışan Notları - {client_name}")
            self.geometry("800x600")
            
            self.transient(parent)
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            self.client_id = client_id
            self.client_name = client_name
            
            self.main_frame = ctk.CTkFrame(self)
            self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            self.top_frame = ctk.CTkFrame(self.main_frame)
            self.top_frame.pack(fill="x", pady=(0, 10))
            
            self.note_title = ctk.CTkEntry(self.top_frame, 
                                         placeholder_text="Not Başlığı",
                                         height=35,
                                         font=("Arial", 12))
            self.note_title.pack(fill="x", padx=5, pady=5)
            
            self.note_entry = ctk.CTkTextbox(self.top_frame, height=150,
                                           font=("Arial", 12))
            self.note_entry.pack(fill="x", padx=5, pady=5)
            
            self.button_frame = ctk.CTkFrame(self.top_frame)
            self.button_frame.pack(fill="x", padx=5, pady=5)
            
            self.add_button = ctk.CTkButton(self.button_frame, 
                                          text="Not Ekle",
                                          command=self.add_note,
                                          font=("Arial", 12, "bold"))
            self.add_button.pack(side="left", padx=5)
            
            self.clear_button = ctk.CTkButton(self.button_frame,
                                            text="Temizle",
                                            command=self.clear_entry,
                                            font=("Arial", 12, "bold"))
            self.clear_button.pack(side="left", padx=5)
            
            self.bottom_frame = ctk.CTkFrame(self.main_frame)
            self.bottom_frame.pack(fill="both", expand=True)
            
            self.notes_label = ctk.CTkLabel(self.bottom_frame,
                                          text="Kayıtlı Notlar",
                                          font=("Arial", 14, "bold"))
            self.notes_label.pack(pady=5)
            
            self.notes_text = ctk.CTkTextbox(self.bottom_frame,
                                           font=("Arial", 12))
            self.notes_text.pack(fill="both", expand=True, padx=5, pady=5)
            
            self.selected_note_id = None
            
            self.context_menu = tk.Menu(self, tearoff=0)
            self.context_menu.add_command(label="Sil", command=self.delete_note)
            
            self.notes_text.bind("<Button-3>", self.show_context_menu)
            self.notes_text.bind("<Button-1>", self.get_selected_note)
            
            self.load_notes()
            self.initialized = True
        
        self.deiconify()
        self.lift()

    def on_closing(self):
        self.withdraw()

    def clear_entry(self):
        self.note_title.delete(0, 'end')
        self.note_entry.delete("1.0", "end")
        
    def add_note(self):
        title = self.note_title.get().strip()
        note = self.note_entry.get("1.0", "end-1c").strip()
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if title and note:
            conn = sqlite3.connect('diet_tracker.db')
            c = conn.cursor()
            c.execute("""INSERT INTO client_notes (client_id, note_title, note, date)
                        VALUES (?, ?, ?, ?)""", 
                     (self.client_id, title, note, current_date))
            conn.commit()
            conn.close()
            
            self.clear_entry()
            self.load_notes()
            messagebox.showinfo("Başarılı", "Not başarıyla eklendi!")
        else:
            messagebox.showwarning("Uyarı", "Başlık ve not alanı boş bırakılamaz!")
            
    def load_notes(self):
        self.notes_text.configure(state="normal")
        self.notes_text.delete("1.0", "end")
        
        conn = sqlite3.connect('diet_tracker.db')
        c = conn.cursor()
        c.execute("""SELECT id, note_title, note, date 
                    FROM client_notes 
                    WHERE client_id = ? 
                    ORDER BY date DESC""", (self.client_id,))
        notes = c.fetchall()
        conn.close()
        
        for note_id, title, note, date in notes:
            self.notes_text.insert("end", f"ID: {note_id}\n")
            self.notes_text.insert("end", f"Tarih: {date}\n")
            self.notes_text.insert("end", f"Başlık: {title}\n")
            self.notes_text.insert("end", f"Not: {note}\n")
            self.notes_text.insert("end", "-" * 50 + "\n\n")
        
        self.notes_text.configure(state="disabled")
    
    def show_context_menu(self, event):
        self.get_selected_note(event)
        if self.selected_note_id:
            self.context_menu.post(event.x_root, event.y_root)
    
    def get_selected_note(self, event):
        index = self.notes_text.index(f"@{event.x},{event.y}")
        line_start = self.notes_text.index(f"{index} linestart")
        line_num = int(float(line_start))
        
        while line_num > 0:
            line = self.notes_text.get(f"{line_num}.0", f"{line_num}.end")
            if line.startswith("ID: "):
                self.selected_note_id = int(line.split("ID: ")[1])
                return
            line_num -= 1
        
        self.selected_note_id = None
    
    def delete_note(self):
        if self.selected_note_id:
            if messagebox.askyesno("Onay", "Bu notu silmek istediğinizden emin misiniz?"):
                conn = sqlite3.connect('diet_tracker.db')
                c = conn.cursor()
                c.execute("DELETE FROM client_notes WHERE id = ?", 
                         (self.selected_note_id,))
                conn.commit()
                conn.close()
                
                self.load_notes()
                messagebox.showinfo("Başarılı", "Not başarıyla silindi!")
                self.selected_note_id = None

class DietApp:
    def __init__(self):
        install_dependencies()
        check_and_create_database()

        self.root = ctk.CTk()
        self.root.title("Diyetisyen Takip Sistemi")
        self.root.geometry("1400x800")
        
        self.create_database()
        
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.left_panel = ctk.CTkFrame(self.main_container, width=300)
        self.left_panel.pack(side="left", fill="y", padx=5, pady=5)
        
        self.middle_panel = ctk.CTkFrame(self.main_container)
        self.middle_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.right_panel = ctk.CTkFrame(self.main_container, width=300)
        self.right_panel.pack(side="right", fill="y", padx=5, pady=5)
        
        self.setup_left_panel()
        self.setup_middle_panel()
        self.setup_right_panel()

    def create_database(self):
        conn = sqlite3.connect('diet_tracker.db')
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS clients
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     surname TEXT NOT NULL)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS weight_records
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     client_id INTEGER,
                     weight REAL NOT NULL,
                     date DATE NOT NULL,
                     FOREIGN KEY (client_id) REFERENCES clients (id))''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS client_notes
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     client_id INTEGER,
                     note_title TEXT NOT NULL,
                     note TEXT NOT NULL,
                     date DATETIME NOT NULL,
FOREIGN KEY (client_id) REFERENCES clients (id))''')
        
        conn.commit()
        conn.close()

    def setup_left_panel(self):
        client_add_frame = ctk.CTkFrame(self.left_panel)
        client_add_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(client_add_frame, text="Yeni Danışan Ekle", 
                    font=("Arial", 14, "bold")).pack(pady=5)
        
        self.name_entry = ctk.CTkEntry(client_add_frame, placeholder_text="Ad")
        self.name_entry.pack(fill="x", padx=5, pady=2)
        
        self.surname_entry = ctk.CTkEntry(client_add_frame, placeholder_text="Soyad")
        self.surname_entry.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkButton(client_add_frame, text="Danışan Ekle", 
                     command=self.add_client).pack(fill="x", padx=5, pady=5)

        client_select_frame = ctk.CTkFrame(self.left_panel)
        client_select_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(client_select_frame, text="Danışan Seç", 
                    font=("Arial", 14, "bold")).pack(pady=5)
        
        self.client_var = ctk.StringVar()
        self.client_option = ctk.CTkOptionMenu(client_select_frame, 
                                             variable=self.client_var,
                                             command=self.update_graph)
        self.client_option.pack(fill="x", padx=5, pady=5)
        
        self.info_frame = ctk.CTkFrame(self.left_panel)
        self.info_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(self.info_frame, text="Danışan Bilgileri",
                    font=("Arial", 14, "bold")).pack(pady=5)
        
        self.client_info_text = ctk.CTkTextbox(self.info_frame, height=150)
        self.client_info_text.pack(fill="x", padx=5, pady=5)
        
        self.update_client_list()

    def setup_middle_panel(self):
        self.graph_label = ctk.CTkLabel(self.middle_panel, 
                                      text="Kilo Takip Grafiği",
                                      font=("Arial", 16, "bold"))
        self.graph_label.pack(pady=5)
        
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.middle_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def setup_right_panel(self):
        weight_frame = ctk.CTkFrame(self.right_panel)
        weight_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(weight_frame, text="Kilo Ekle", 
                    font=("Arial", 14, "bold")).pack(pady=5)
        
        self.weight_entry = ctk.CTkEntry(weight_frame, placeholder_text="Kilo (kg)")
        self.weight_entry.pack(fill="x", padx=5, pady=2)
        
        self.date_picker = DatePicker(weight_frame)
        self.date_picker.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(weight_frame, text="Kilo Ekle", 
                     command=self.add_weight).pack(fill="x", padx=5, pady=5)
        
        ctk.CTkButton(self.right_panel, 
                     text="Danışan Notları",
                     command=self.show_notes).pack(fill="x", padx=5, pady=5)

    def add_client(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        
        if name and surname:
            conn = sqlite3.connect('diet_tracker.db')
            c = conn.cursor()
            c.execute("INSERT INTO clients (name, surname) VALUES (?, ?)", 
                     (name, surname))
            conn.commit()
            conn.close()
            
            self.name_entry.delete(0, 'end')
            self.surname_entry.delete(0, 'end')
            self.update_client_list()
            messagebox.showinfo("Başarılı", "Danışan başarıyla eklendi!")

    def update_client_list(self):
        conn = sqlite3.connect('diet_tracker.db')
        c = conn.cursor()
        c.execute("SELECT id, name, surname FROM clients ORDER BY name, surname")
        clients = c.fetchall()
        conn.close()
        
        client_list = [f"{client[1]} {client[2]}" for client in clients]
        self.client_option.configure(values=client_list)
        if client_list:
            self.client_option.set(client_list[0])
            self.update_graph()

    def add_weight(self):
        if not self.client_var.get():
            messagebox.showwarning("Uyarı", "Lütfen önce bir danışan seçin!")
            return
        
        weight = self.weight_entry.get()
        selected_date = self.date_picker.get_date()
        
        if weight:
            try:
                weight = float(weight)
                conn = sqlite3.connect('diet_tracker.db')
                c = conn.cursor()
                
                client_name = self.client_var.get().split()
                c.execute("SELECT id FROM clients WHERE name=? AND surname=?", 
                         (client_name[0], client_name[1]))
                client_id = c.fetchone()[0]
                
                c.execute("""SELECT id FROM weight_records 
                            WHERE client_id=? AND date=?""", 
                         (client_id, selected_date))
                existing_record = c.fetchone()
                
                if existing_record:
                    if messagebox.askyesno("Uyarı", "Bu tarihte zaten bir kayıt var. Güncellemek ister misiniz?"):
                        c.execute("""UPDATE weight_records 
                                   SET weight=? WHERE client_id=? AND date=?""",
                                (weight, client_id, selected_date))
                else:
                    c.execute("""INSERT INTO weight_records 
                               (client_id, weight, date) VALUES (?, ?, ?)""",
                            (client_id, weight, selected_date))
                
                conn.commit()
                conn.close()
                
                self.weight_entry.delete(0, 'end')
                self.update_graph()
                messagebox.showinfo("Başarılı", "Kilo kaydı eklendi!")
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir kilo değeri girin!")

    def show_notes(self):
        if not self.client_var.get():
            messagebox.showwarning("Uyarı", "Lütfen önce bir danışan seçin!")
            return
            
        client_name = self.client_var.get()
        conn = sqlite3.connect('diet_tracker.db')
        c = conn.cursor()
        c.execute("SELECT id FROM clients WHERE name || ' ' || surname = ?", (client_name,))
        client_id = c.fetchone()[0]
        conn.close()
        
        notes_window = ClientNotes(self.root, client_id, client_name)
        notes_window.focus()

    def update_graph(self, *args):
        if not self.client_var.get():
            return
            
        conn = sqlite3.connect('diet_tracker.db')
        c = conn.cursor()
        
        client_name = self.client_var.get().split()
        
        c.execute("""
            SELECT 
                MIN(weight_records.date) as start_date,
                MAX(weight_records.date) as last_date,
                MIN(weight_records.weight) as min_weight,
                MAX(weight_records.weight) as max_weight,
                COUNT(weight_records.id) as record_count
            FROM clients 
            LEFT JOIN weight_records ON clients.id = weight_records.client_id
            WHERE clients.name=? AND clients.surname=?
        """, (client_name[0], client_name[1]))
        
        info = c.fetchone()
        
        self.client_info_text.configure(state="normal")
        self.client_info_text.delete("1.0", "end")
        self.client_info_text.insert("end", 
            f"Takip Başlangıç: {info[0] or 'Kayıt yok'}\n"
            f"Son Kayıt: {info[1] or 'Kayıt yok'}\n"
            f"En Düşük Kilo: {info[2] or 'Kayıt yok'}\n"
            f"En Yüksek Kilo: {info[3] or 'Kayıt yok'}\n"
            f"Toplam Kayıt: {info[4] or 0}"
        )
        self.client_info_text.configure(state="disabled")
        
        c.execute("""
            SELECT weight_records.weight, weight_records.date 
            FROM weight_records 
            JOIN clients ON weight_records.client_id = clients.id 
            WHERE clients.name=? AND clients.surname=?
            ORDER BY weight_records.date
        """, (client_name[0], client_name[1]))
        
        records = c.fetchall()
        conn.close()
        
        if records:
            weights = [record[0] for record in records]
            dates = [datetime.strptime(record[1], '%Y-%m-%d').date() for record in records]
            
            self.ax.clear()
            self.ax.plot(dates, weights, 'o-', color='blue', linewidth=2, markersize=8)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            
            self.ax.set_title(f"{self.client_var.get()} - Kilo Takibi", 
                            fontsize=12, pad=15)
            self.ax.set_xlabel("Tarih", fontsize=10, labelpad=10)
            self.ax.set_ylabel("Kilo (kg)", fontsize=10, labelpad=10)
            
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
            self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
            
            for i, weight in enumerate(weights):
                self.ax.annotate(f'{weight}kg', 
                               (dates[i], weights[i]),
                               textcoords="offset points",
                               xytext=(0,10),
                               ha='center',
                               fontsize=8)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            self.canvas.draw()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DietApp()
    app.run()