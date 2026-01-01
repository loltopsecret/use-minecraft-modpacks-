import os
import sys
import json
import shutil
import zipfile
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import subprocess
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

TRANSLATIONS = {
    'en': {
        'title': 'Minecraft Modpack Organizer',
        'header': 'Organize Minecraft Modpack',
        'modpack_file': 'Modpack file:',
        'not_selected': 'Not selected',
        'select': 'Select',
        'archive_format': 'Archive format:',
        'ready': 'Ready to work',
        'create_archive': 'Organize',
        'file_selected': 'File selected',
        'select_file': 'Select modpack file',
        'error': 'Error',
        'select_modpack_error': 'Select modpack file',
        'extracting': 'Extracting modpack...',
        'organizing': 'Organizing files...',
        'creating_zip': 'Creating ZIP archive...',
        'creating_7z': 'Creating 7z archive...',
        'success': 'Organized successfully!',
        'success_msg': 'Modpack organized!\n\nPath: {}',
        'open_folder': 'Open folder?',
        'open_folder_msg': 'Open folder with files?',
        'error_creating': 'Error organizing',
        'error_msg': 'An error occurred:\n{}',
        'zip_files': 'ZIP archives',
        'all_files': 'All files',
        '7z_not_found': '7z not found',
        '7z_error': '7z error: {}',
        'found_mods': 'Mods: {}',
        'found_resourcepacks': 'Resource Packs: {}',
        'found_shaders': 'Shaders: {}',
        'downloading_mods': 'Downloading {}/{}...',
        'parsing_manifest': 'Parsing manifest...',
        'copying_overrides': 'Copying files...',
        'use_custom_key': 'API Keys',
        'custom_key_title': 'Manage API Keys',
        'custom_key_msg': 'Get key from:\nhttps://console.curseforge.com',
        'key_saved': 'Keys saved!',
        'using_default': 'Using default key',
        'using_custom': 'Using {} custom key(s)',
        'stop_download': 'Stop',
        'include_mods': 'Include Mods',
        'include_resourcepacks': 'Include Resource Packs',
        'include_shaders': 'Include Shaders',
        'history': 'History',
        'clear_history': 'Clear History',
        'download_stopped': 'Stopped by user',
        'parallel_settings': 'Parallel Downloads',
        'max_workers': 'Max parallel downloads:',
        'add_key': 'Add Key',
        'remove_key': 'Remove',
        'workers_limited': 'Limited to 5 with default key',
        'workers_unlocked': 'Up to {} with custom keys',
        'use_default_key': 'Use Default Key',
        'original_modpack': 'Original: {}',
        'default_key_error': 'Cannot use default key!',
        'default_key_error_msg': 'This is the default key used by everyone.\nPlease get your own key from:\nhttps://console.curseforge.com',
        'key_exists_error': 'Key already exists!',
        'key_exists_msg': 'This key is already in your list.'
    },
    'ru': {
        'title': 'Организатор модпаков Minecraft',
        'header': 'Организация модпака Minecraft',
        'modpack_file': 'Файл модпака:',
        'not_selected': 'Не выбран',
        'select': 'Выбрать',
        'archive_format': 'Формат архива:',
        'ready': 'Готов к работе',
        'create_archive': 'Организовать',
        'file_selected': 'Файл выбран',
        'select_file': 'Выберите файл модпака',
        'error': 'Ошибка',
        'select_modpack_error': 'Пожалуйста, выберите файл модпака',
        'extracting': 'Распаковка модпака...',
        'organizing': 'Организация файлов...',
        'creating_zip': 'Создание ZIP архива...',
        'creating_7z': 'Создание 7z архива...',
        'success': 'Успешно!',
        'success_msg': 'Модпак организован!\n\nПуть: {}',
        'open_folder': 'Открыть папку?',
        'open_folder_msg': 'Открыть папку с файлами?',
        'error_creating': 'Ошибка при организации',
        'error_msg': 'Произошла ошибка:\n{}',
        'zip_files': 'ZIP архивы',
        'all_files': 'Все файлы',
        '7z_not_found': '7z не найден в системе',
        '7z_error': 'Ошибка 7z: {}',
        'found_mods': 'Найдено модов: {}',
        'found_resourcepacks': 'Найдено ресурспаков: {}',
        'found_shaders': 'Найдено шейдеров: {}',
        'downloading_mods': 'Загрузка модов: {}/{}...',
        'parsing_manifest': 'Обработка manifest.json...',
        'copying_overrides': 'Копирование дополнительных файлов...',
        'use_custom_key': 'Управление API ключами',
        'custom_key_title': 'Управление API ключами',
        'custom_key_msg': 'Получить свой ключ можно здесь:\nhttps://console.curseforge.com',
        'key_saved': 'Ключи сохранены!',
        'using_default': 'Используется стандартный ключ',
        'using_custom': 'Используется ключей: {}',
        'stop_download': 'Остановить',
        'include_mods': 'Включить моды',
        'include_resourcepacks': 'Включить ресурспаки',
        'include_shaders': 'Включить шейдеры',
        'history': 'История обработки',
        'clear_history': 'Очистить историю',
        'download_stopped': 'Остановлено пользователем',
        'parallel_settings': 'Настройки параллельной загрузки',
        'max_workers': 'Максимум параллельных загрузок:',
        'add_key': 'Добавить ключ',
        'remove_key': 'Удалить выбранный',
        'workers_limited': 'Максимум 5 со стандартным ключом',
        'workers_unlocked': 'До {} с вашими ключами',
        'use_default_key': 'Сбросить на стандартный',
        'original_modpack': 'Исходный модпак: {}',
        'default_key_error': 'Нельзя использовать стандартный ключ!',
        'default_key_error_msg': 'Это стандартный ключ, который используют все.\nПолучите свой собственный ключ здесь:\nhttps://console.curseforge.com',
        'key_exists_error': 'Ключ уже добавлен!',
        'key_exists_msg': 'Этот ключ уже есть в вашем списке.'
    }
}

DEFAULT_API_KEY = "$2a$10$bL4bIL5pUWqfcO7KQtnMReakwtfHbNKh6v1uTpKlzhwoueEJQnPnm"

class ModpackArchiver:
    def __init__(self, language='en'):
        self.language = language
        self.t = TRANSLATIONS[language]
        
        self.root = tk.Tk()
        self.root.title(self.t['title'])
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        self.modpack_path = None
        self.stop_requested = False
        self.executor = None
        
        self.archive_format = tk.StringVar(value="zip")
        self.include_mods = tk.BooleanVar(value=True)
        self.include_resourcepacks = tk.BooleanVar(value=True)
        self.include_shaders = tk.BooleanVar(value=True)
        
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        
        self.config_file = os.path.join(base, "config.json")
        self.history_file = os.path.join(base, "history.json")
        
        self.load_config()
        self.load_history()
        
        print(f"DEBUG: Loaded max_workers={self.max_workers}")
        print(f"DEBUG: Loaded api_keys={len(self.api_keys)}")
        
        self.main_container = tk.Frame(self.root, bg="#1a1a2e")
        self.main_container.pack(fill="both", expand=True)
        
        self.setup_ui()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_keys = config.get('api_keys', [])
                    self.max_workers = config.get('max_workers', 5)
            else:
                self.api_keys = []
                self.max_workers = 5
        except:
            self.api_keys = []
            self.max_workers = 5
    
    def save_config(self):
        try:
            config = {
                'api_keys': self.api_keys, 
                'max_workers': self.max_workers
            }
            print(f"DEBUG: save_config - Saving: {config}")
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"DEBUG: save_config - Config saved successfully")
                
        except Exception as e:
            print(f"DEBUG: save_config - ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except:
            self.history = []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[-10:], f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def add_to_history(self, output_path, original_modpack):
        self.history.append({
            'output_path': output_path,
            'output_name': os.path.basename(output_path),
            'original_modpack': os.path.basename(original_modpack),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.save_history()
    
    def get_api_keys_distribution(self):
        workers = self.get_max_workers()
        all_keys = [DEFAULT_API_KEY] + self.api_keys
        num_keys = len(all_keys)
        
        if num_keys == 0:
            return [DEFAULT_API_KEY] * workers
        
        base = workers // num_keys
        remainder = workers % num_keys
        
        distributed_keys = []
        for i, key in enumerate(all_keys):
            count = base + (1 if i < remainder else 0)
            distributed_keys.extend([key] * count)
        
        print(f"DEBUG: get_api_keys_distribution - workers={workers}, keys={len(distributed_keys)}")
        
        return distributed_keys
    
    def get_max_workers(self):
        max_limit = 5 + (len(self.api_keys) * 10)
        return min(self.max_workers, max_limit)
    
    def setup_ui(self):
        main = tk.Frame(self.main_container, bg="#1a1a2e")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(main, text=self.t['header'], font=("Arial", 16, "bold"), bg="#1a1a2e", fg="#fff").pack(pady=(0,20))
        
        top_bar = tk.Frame(main, bg="#1a1a2e")
        top_bar.pack(fill="x", pady=10)
        
        left_section = tk.Frame(top_bar, bg="#1a1a2e")
        left_section.pack(side="left", fill="x", expand=True)
        
        api_text = self.t['using_custom'].format(len(self.api_keys)) if self.api_keys else self.t['using_default']
        self.api_label = tk.Label(left_section, text=api_text, font=("Arial", 8), bg="#1a1a2e", 
                                  fg="#4ade80" if self.api_keys else "#888", wraplength=350, anchor="w", justify="left")
        self.api_label.pack(side="left", anchor="w")
        
        right_section = tk.Frame(top_bar, bg="#1a1a2e")
        right_section.pack(side="right")
        
        tk.Button(right_section, text=self.t['history'], command=self.show_history, bg="#5b21b6", fg="white",
                 font=("Arial", 9, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="right", padx=(0,10), ipadx=10, ipady=5)
        
        tk.Button(right_section, text=self.t['parallel_settings'], command=self.show_parallel_settings, bg="#5b21b6", fg="white",
                 font=("Arial", 9, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="right", padx=(0,10), ipadx=10, ipady=5)
        
        tk.Button(right_section, text=self.t['use_custom_key'], command=self.manage_keys, bg="#5b21b6", fg="white",
                 font=("Arial", 9, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="right", ipadx=10, ipady=5)
        
        file_frame = tk.Frame(main, bg="#1a1a2e")
        file_frame.pack(pady=10, fill="x")
        tk.Label(file_frame, text=self.t['modpack_file'], font=("Arial", 10), bg="#1a1a2e", fg="#b0b0b0").pack(anchor="w")
        
        file_select = tk.Frame(file_frame, bg="#1a1a2e")
        file_select.pack(fill="x", pady=5)
        
        self.file_label = tk.Label(file_select, text=self.t['not_selected'], bg="#2d2d44", fg="#888",
                                   anchor="w", padx=10, font=("Arial", 9), relief="flat")
        self.file_label.pack(side="left", fill="x", expand=True, padx=(0,10), ipady=8)
        
        tk.Button(file_select, text=self.t['select'], command=self.select_file, bg="#7c3aed", fg="white",
                 font=("Arial", 9, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="right", ipadx=15, ipady=8)
        
        fmt_frame = tk.Frame(main, bg="#1a1a2e")
        fmt_frame.pack(pady=15, fill="x")
        tk.Label(fmt_frame, text=self.t['archive_format'], font=("Arial", 10), bg="#1a1a2e", fg="#b0b0b0").pack(anchor="w")
        
        radio = tk.Frame(fmt_frame, bg="#1a1a2e")
        radio.pack(anchor="w", pady=5)
        tk.Radiobutton(radio, text="ZIP", variable=self.archive_format, value="zip", font=("Arial", 10),
                      bg="#1a1a2e", fg="#fff", selectcolor="#7c3aed", activebackground="#1a1a2e", cursor="hand2").pack(side="left", padx=(0,20))
        tk.Radiobutton(radio, text="7z", variable=self.archive_format, value="7z", font=("Arial", 10),
                      bg="#1a1a2e", fg="#fff", selectcolor="#7c3aed", activebackground="#1a1a2e", cursor="hand2").pack(side="left")
        
        opt_frame = tk.Frame(main, bg="#1a1a2e")
        opt_frame.pack(pady=10, fill="x")
        tk.Label(opt_frame, text="Include:" if self.language=='en' else "Включить:", font=("Arial", 10), bg="#1a1a2e", fg="#b0b0b0").pack(anchor="w")
        
        checks = tk.Frame(opt_frame, bg="#1a1a2e")
        checks.pack(anchor="w", pady=5)
        tk.Checkbutton(checks, text=self.t['include_mods'], variable=self.include_mods, font=("Arial", 9),
                      bg="#1a1a2e", fg="#fff", selectcolor="#7c3aed", activebackground="#1a1a2e").pack(side="left", padx=(0,15))
        tk.Checkbutton(checks, text=self.t['include_resourcepacks'], variable=self.include_resourcepacks, font=("Arial", 9),
                      bg="#1a1a2e", fg="#fff", selectcolor="#7c3aed", activebackground="#1a1a2e").pack(side="left", padx=(0,15))
        tk.Checkbutton(checks, text=self.t['include_shaders'], variable=self.include_shaders, font=("Arial", 9),
                      bg="#1a1a2e", fg="#fff", selectcolor="#7c3aed", activebackground="#1a1a2e").pack(side="left")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("purple.Horizontal.TProgressbar", troughcolor='#2d2d44', background='#7c3aed',
                       darkcolor='#7c3aed', lightcolor='#7c3aed', bordercolor='#2d2d44', borderwidth=0)
        
        self.progress = ttk.Progressbar(main, length=710, mode='determinate', style="purple.Horizontal.TProgressbar")
        self.progress.pack(pady=20)
        
        self.status = tk.Label(main, text=self.t['ready'], font=("Arial", 9), fg="#4ade80", bg="#1a1a2e")
        self.status.pack(pady=5)
        
        self.detail = tk.Label(main, text="", font=("Arial", 8), fg="#888", bg="#1a1a2e")
        self.detail.pack(pady=2)
        
        btns = tk.Frame(main, bg="#1a1a2e")
        btns.pack(pady=15)
        
        self.create_btn = tk.Button(btns, text=self.t['create_archive'], command=self.start_thread, font=("Arial", 12, "bold"),
                                    bg="#7c3aed", fg="white", width=20, height=2, state="disabled", relief="flat", cursor="hand2", bd=0)
        self.create_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(btns, text=self.t['stop_download'], command=self.stop, font=("Arial", 11, "bold"),
                                 bg="#dc2626", fg="white", width=10, height=2, state="disabled", relief="flat", cursor="hand2", bd=0)
        self.stop_btn.pack(side="left", padx=5)
    
    def select_file(self):
        f = filedialog.askopenfilename(title=self.t['select_file'], filetypes=[(self.t['zip_files'], "*.zip"), (self.t['all_files'], "*.*")])
        if f:
            self.modpack_path = f
            self.file_label.config(text=os.path.basename(f), fg="#fff")
            self.create_btn.config(state="normal")
            self.status.config(text=self.t['file_selected'], fg="#4ade80")
    
    def update_status(self, msg, color="#fff"):
        self.status.config(text=msg, fg=color)
        self.root.update()
    
    def update_detail(self, msg):
        self.detail.config(text=msg)
        self.root.update()
    
    def update_progress(self, val):
        self.progress['value'] = val
        self.root.update()
    
    def show_history(self):
        d = tk.Toplevel(self.root)
        d.title(self.t['history'])
        d.geometry("700x550")
        d.configure(bg="#1a1a2e")
        d.resizable(True, True)
        d.transient(self.root)
        d.grab_set()
        
        tk.Label(d, text=self.t['history'], font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#fff").pack(pady=15)
        
        f = tk.Frame(d, bg="#1a1a2e")
        f.pack(fill="both", expand=True, padx=20, pady=10)
        
        sb = tk.Scrollbar(f)
        sb.pack(side="right", fill="y")
        
        lb = tk.Listbox(f, yscrollcommand=sb.set, bg="#2d2d44", fg="#fff", font=("Arial", 9), selectbackground="#7c3aed", bd=0)
        lb.pack(fill="both", expand=True)
        sb.config(command=lb.yview)
        
        for e in reversed(self.history):
            date_str = e.get('date', 'Unknown')
            output_name = e.get('output_name', e.get('name', 'Unknown'))
            original = e.get('original_modpack', 'Unknown')
            lb.insert("end", f"{date_str}")
            lb.insert("end", f"  {'Output' if self.language=='en' else 'Результат'}: {output_name}")
            lb.insert("end", f"  {self.t['original_modpack'].format(original)}")
            lb.insert("end", "")
        
        btn_frame = tk.Frame(d, bg="#1a1a2e")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text=self.t['clear_history'], command=lambda: self.clear_hist(d), bg="#dc2626", fg="white",
                 font=("Arial", 11, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="left", padx=5, ipadx=15, ipady=10)
        tk.Button(btn_frame, text="Close" if self.language=='en' else "Закрыть", command=d.destroy, bg="#5b21b6", fg="white",
                 font=("Arial", 11, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="left", padx=5, ipadx=15, ipady=10)
    
    def clear_hist(self, d):
        self.history = []
        self.save_history()
        d.destroy()
        messagebox.showinfo(self.t['history'], "Cleared!" if self.language=='en' else "История очищена!")
    
    def show_parallel_settings(self):
        d = tk.Toplevel(self.root)
        d.title(self.t['parallel_settings'])
        d.geometry("500x700")
        d.configure(bg="#1a1a2e")
        d.resizable(True, True)
        d.transient(self.root)
        d.grab_set()
        
        tk.Label(d, text=self.t['parallel_settings'], font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#fff").pack(pady=15)
        
        keys_frame = tk.LabelFrame(d, text="Available API Keys:" if self.language=='en' else "Доступные API ключи:", bg="#1a1a2e", fg="#b0b0b0", font=("Arial", 10, "bold"))
        keys_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(keys_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = tk.Scrollbar(keys_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        default_var = tk.BooleanVar(value=True)
        default_frame = tk.Frame(scrollable_frame, bg="#2d2d44", relief="raised", bd=1)
        default_frame.pack(fill="x", padx=5, pady=3)
        
        default_text = "Default CurseForge Key" if self.language=='en' else "Стандартный ключ CurseForge"
        tk.Checkbutton(default_frame, text=default_text, variable=default_var,
                      font=("Arial", 9, "bold"), bg="#2d2d44", fg="#4ade80", selectcolor="#1a1a2e",
                      activebackground="#2d2d44", state="disabled").pack(anchor="w", padx=10, pady=8)
        
        key_vars = []
        for idx, key in enumerate(self.api_keys, 1):
            var = tk.BooleanVar(value=True)
            key_vars.append((key, var))
            
            key_frame = tk.Frame(scrollable_frame, bg="#2d2d44", relief="raised", bd=1)
            key_frame.pack(fill="x", padx=5, pady=3)
            
            key_label = "Custom Key" if self.language=='en' else "Пользовательский ключ"
            display = f"{key_label} #{idx}: {key[:30]}..." if len(key) > 30 else f"{key_label} #{idx}: {key}"
            tk.Checkbutton(key_frame, text=display, variable=var, font=("Arial", 9),
                          bg="#2d2d44", fg="#fff", selectcolor="#1a1a2e",
                          activebackground="#2d2d44").pack(anchor="w", padx=10, pady=8)
        
        slider_frame = tk.Frame(d, bg="#1a1a2e")
        slider_frame.pack(pady=15)
        
        tk.Label(slider_frame, text=self.t['max_workers'], font=("Arial", 10, "bold"), bg="#1a1a2e", fg="#fff").pack()
        
        max_allowed = 5 + (len(self.api_keys) * 10)
        
        val_label = tk.Label(slider_frame, text=str(self.max_workers), font=("Arial", 16, "bold"), bg="#1a1a2e", fg="#7c3aed", width=3)
        val_label.pack(pady=5)
        
        def on_change(v):
            workers = int(float(v))
            val_label.config(text=str(workers))
            
            active_keys = 1 + sum(1 for _, var in key_vars if var.get())
            if active_keys > 0:
                base = workers // active_keys
                remainder = workers % active_keys
                
                distribution = []
                for i in range(active_keys):
                    if i < remainder:
                        distribution.append(base + 1)
                    else:
                        distribution.append(base)
                
                dist_label_text = "Distribution" if self.language=='en' else "Распределение"
                dist_text = f"{dist_label_text}: {' + '.join(map(str, distribution))} = {workers}"
                dist_label.config(text=dist_text)
        
        slider = tk.Scale(d, from_=1, to=max_allowed, orient="horizontal", command=on_change,
                         bg="#2d2d44", fg="#fff", troughcolor="#1a1a2e", highlightthickness=0,
                         length=400, sliderlength=30)
        slider.set(min(self.max_workers, max_allowed))
        slider.pack()
        
        dist_label = tk.Label(d, text="", font=("Arial", 9), bg="#1a1a2e", fg="#888")
        dist_label.pack(pady=5)
        
        on_change(slider.get())
        
        limit_text = self.t['workers_limited'] if not self.api_keys else self.t['workers_unlocked'].format(max_allowed)
        tk.Label(d, text=limit_text, font=("Arial", 9), bg="#1a1a2e", fg="#888").pack(pady=5)
        
        def save():
            self.max_workers = int(slider.get())
            active_custom_keys = [key for key, var in key_vars if var.get()]
            self.api_keys = active_custom_keys
            self.save_config()
            
            text = self.t['using_custom'].format(len(self.api_keys)) if self.api_keys else self.t['using_default']
            color = "#4ade80" if self.api_keys else "#888"
            self.api_label.config(text=text, fg=color)
            d.destroy()
        
        save_text = "Save" if self.language=='en' else "Сохранить"
        tk.Button(d, text=save_text, command=save, bg="#7c3aed", fg="white",
                 font=("Arial", 11, "bold"), relief="flat", cursor="hand2", bd=0).pack(pady=10, ipadx=25, ipady=10)
    
    def manage_keys(self):
        d = tk.Toplevel(self.root)
        d.title(self.t['custom_key_title'])
        d.geometry("600x500")
        d.configure(bg="#1a1a2e")
        d.resizable(True, True)
        d.transient(self.root)
        d.grab_set()
        
        tk.Label(d, text=self.t['custom_key_msg'], font=("Arial", 10), bg="#1a1a2e", fg="#b0b0b0").pack(pady=15, padx=20)
        
        list_frame = tk.Frame(d, bg="#1a1a2e")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        sb = tk.Scrollbar(list_frame)
        sb.pack(side="right", fill="y")
        
        keys_list = tk.Listbox(list_frame, yscrollcommand=sb.set, bg="#2d2d44", fg="#fff", 
                              font=("Arial", 9), selectbackground="#7c3aed", bd=0, height=10)
        keys_list.pack(fill="both", expand=True)
        sb.config(command=keys_list.yview)
        
        def refresh_list():
            keys_list.delete(0, "end")
            for idx, key in enumerate(self.api_keys, 1):
                display = f"{idx}. {key[:20]}..." if len(key) > 20 else f"{idx}. {key}"
                keys_list.insert("end", display)
        
        refresh_list()
        
        btn_frame = tk.Frame(d, bg="#1a1a2e")
        btn_frame.pack(pady=10)
        
        def add():
            add_dialog = tk.Toplevel(d)
            add_dialog.title(self.t['add_key'])
            add_dialog.geometry("550x250")
            add_dialog.configure(bg="#1a1a2e")
            add_dialog.transient(d)
            add_dialog.grab_set()
            
            tk.Label(add_dialog, text=self.t['custom_key_msg'], font=("Arial", 10), bg="#1a1a2e", fg="#b0b0b0").pack(pady=15)
            
            entry_frame = tk.Frame(add_dialog, bg="#2d2d44")
            entry_frame.pack(pady=10, padx=20, fill="both", expand=True)
            
            entry = tk.Entry(entry_frame, font=("Arial", 10), bg="#2d2d44", fg="#fff", insertbackground="#fff", 
                           relief="flat", bd=0)
            entry.pack(fill="both", expand=True, padx=10, pady=10)
            
            def paste_text(event=None):
                try:
                    text = add_dialog.clipboard_get()
                    if text and len(text) > 500:
                        text = text[:500]
                    entry.delete(0, "end")
                    entry.insert(0, text)
                except Exception as e:
                    print(f"DEBUG: Paste error: {e}")
                    status_label.config(text="Error pasting" if self.language=='en' else "Ошибка вставки")
                return "break"
            
            entry.bind('<Control-v>', paste_text)
            entry.bind('<Control-V>', paste_text)
            entry.bind('<Button-3>', paste_text)
            entry.focus_force()
            add_dialog.after(100, lambda: entry.focus_force())
            
            paste_btn_frame = tk.Frame(add_dialog, bg="#1a1a2e")
            paste_btn_frame.pack(pady=5)
            
            paste_text_btn = "📋 Paste Key" if self.language=='en' else "📋 Вставить ключ"
            tk.Button(paste_btn_frame, text=paste_text_btn, 
                     command=paste_text, bg="#5b21b6", fg="white",
                     font=("Arial", 10, "bold"), relief="flat", cursor="hand2", bd=0).pack(ipadx=15, ipady=8)
            
            status_label = tk.Label(add_dialog, text="", font=("Arial", 9), bg="#1a1a2e", fg="#f87171")
            status_label.pack(pady=5)
            
            def validate_key(key):
                if not key or len(key.strip()) == 0:
                    return False, "empty"
                key = key.strip()
                if len(key) > 200:
                    return False, "too_long"
                if key == DEFAULT_API_KEY:
                    return False, "default_key"
                if key in self.api_keys:
                    return False, "duplicate"
                if len(key) < 20:
                    return False, "too_short"
                if not key.startswith('$2'):
                    return False, "invalid_format"
                return True, "OK"
            
            def save_new():
                new_key = entry.get().strip()
                if new_key:
                    valid, msg = validate_key(new_key)
                    if valid:
                        self.api_keys.append(new_key)
                        self.save_config()
                        self.load_config()
                        refresh_list()
                        self.api_label.config(text=self.t['using_custom'].format(len(self.api_keys)), fg="#4ade80")
                        add_dialog.destroy()
                    else:
                        if msg == "default_key":
                            messagebox.showerror(self.t['default_key_error'], self.t['default_key_error_msg'], parent=add_dialog)
                        elif msg == "duplicate":
                            messagebox.showerror(self.t['key_exists_error'], self.t['key_exists_msg'], parent=add_dialog)
                        elif msg == "too_short":
                            status_label.config(text="Error: Key too short (min 20 chars)" if self.language=='en' else "Ошибка: Ключ слишком короткий (мин. 20 символов)")
                        elif msg == "too_long":
                            status_label.config(text="Error: Key too long (max 200 chars)" if self.language=='en' else "Ошибка: Ключ слишком длинный (макс. 200 символов)")
                        elif msg == "invalid_format":
                            status_label.config(text="Error: Invalid format (must start with $2)" if self.language=='en' else "Ошибка: Неверный формат (должен начинаться с $2)")
                        elif msg == "empty":
                            status_label.config(text="Please enter API key" if self.language=='en' else "Пожалуйста, введите API ключ")
                else:
                    enter_key_text = "Please enter API key" if self.language=='en' else "Пожалуйста, введите API ключ"
                    status_label.config(text=enter_key_text)
            
            btn_frame_add = tk.Frame(add_dialog, bg="#1a1a2e")
            btn_frame_add.pack(pady=15)
            
            add_text = "Add" if self.language=='en' else "Добавить"
            tk.Button(btn_frame_add, text=add_text, command=save_new, bg="#7c3aed", fg="white",
                     font=("Arial", 11, "bold"), relief="flat", cursor="hand2", bd=0).pack(ipadx=25, ipady=10)
        
        def remove():
            sel = keys_list.curselection()
            if sel:
                idx = sel[0]
                self.api_keys.pop(idx)
                self.save_config()
                refresh_list()
                text = self.t['using_custom'].format(len(self.api_keys)) if self.api_keys else self.t['using_default']
                color = "#4ade80" if self.api_keys else "#888"
                self.api_label.config(text=text, fg=color)
        
        def use_default():
            self.api_keys = []
            self.save_config()
            refresh_list()
            self.api_label.config(text=self.t['using_default'], fg="#888")
        
        tk.Button(btn_frame, text=self.t['add_key'], command=add, bg="#7c3aed", fg="white",
                 font=("Arial", 10, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="left", padx=5, ipadx=15, ipady=8)
        tk.Button(btn_frame, text=self.t['remove_key'], command=remove, bg="#dc2626", fg="white",
                 font=("Arial", 10, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="left", padx=5, ipadx=15, ipady=8)
        tk.Button(btn_frame, text=self.t['use_default_key'], command=use_default, bg="#5b21b6", fg="white",
                 font=("Arial", 10, "bold"), relief="flat", cursor="hand2", bd=0).pack(side="left", padx=5, ipadx=15, ipady=8)
    
    def stop(self):
        self.stop_requested = True
        if self.executor:
            self.executor.shutdown(wait=False)
        self.update_status(self.t['download_stopped'], "#f87171")
        self.stop_btn.config(state="disabled")
    
    def extract_modpack(self, path, temp):
        self.update_status(self.t['extracting'], "#60a5fa")
        self.update_progress(10)
        with zipfile.ZipFile(path, 'r') as z:
            z.extractall(temp)
        return temp
    
    def download_mod(self, pid, fid, mods_dir, api_key):
        try:
            print(f"DEBUG: Downloading mod {pid}/{fid} with key {api_key[:20]}...")
            url = f"https://api.curseforge.com/v1/mods/{pid}/files/{fid}"
            req = urllib.request.Request(url, headers={'Accept': 'application/json', 'x-api-key': api_key})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            dl_url = data['data'].get('downloadUrl')
            if not dl_url:
                print(f"DEBUG: No download URL for {pid}/{fid}")
                return False
            fname = data['data'].get('fileName', f"{pid}_{fid}.jar")
            mod_path = os.path.join(mods_dir, fname)
            print(f"DEBUG: Downloading {fname}...")
            req = urllib.request.Request(dl_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                with open(mod_path, 'wb') as f:
                    f.write(r.read())
            success = os.path.exists(mod_path) and os.path.getsize(mod_path) > 0
            print(f"DEBUG: Download {'SUCCESS' if success else 'FAILED'}: {fname}")
            return success
        except Exception as e:
            print(f"DEBUG: Error downloading {pid}/{fid}: {e}")
            return False
    
    def organize_files(self, src, tgt):
        self.update_status(self.t['organizing'], "#60a5fa")
        self.update_progress(20)
        
        mods_dir = os.path.join(tgt, "mods")
        rp_dir = os.path.join(tgt, "resourcepacks")
        sh_dir = os.path.join(tgt, "shaders")
        
        os.makedirs(mods_dir, exist_ok=True)
        os.makedirs(rp_dir, exist_ok=True)
        os.makedirs(sh_dir, exist_ok=True)
        
        manifest = os.path.join(src, "manifest.json")
        
        if os.path.exists(manifest) and self.include_mods.get():
            self.update_status(self.t['parsing_manifest'], "#60a5fa")
            self.update_progress(30)
            
            with open(manifest, 'r', encoding='utf-8') as f:
                m = json.load(f)
            
            if 'files' in m and not self.stop_requested:
                total = len(m['files'])
                self.update_status(self.t['downloading_mods'].format(0, total), "#60a5fa")
                
                api_keys_pool = self.get_api_keys_distribution()
                
                self.executor = ThreadPoolExecutor(max_workers=self.get_max_workers())
                futures = []
                
                for idx, fi in enumerate(m['files']):
                    if self.stop_requested:
                        break
                    pid = fi.get('projectID')
                    fid = fi.get('fileID')
                    if pid and fid:
                        key_to_use = api_keys_pool[idx % len(api_keys_pool)]
                        futures.append(self.executor.submit(self.download_mod, pid, fid, mods_dir, key_to_use))
                
                dlcount = 0
                for idx, fut in enumerate(as_completed(futures), 1):
                    if self.stop_requested:
                        break
                    try:
                        if fut.result():
                            dlcount += 1
                    except:
                        pass
                    prog = 30 + (40 * idx / total)
                    self.update_progress(prog)
                    self.update_status(self.t['downloading_mods'].format(idx, total), "#60a5fa")
                
                self.executor.shutdown(wait=True)
                self.executor = None
                
                print(f"DEBUG: Downloaded {dlcount} mods successfully")
        
        if self.stop_requested:
            return
        
        self.update_status(self.t['copying_overrides'], "#60a5fa")
        self.update_progress(70)
        
        ovr = os.path.join(src, "overrides")
        
        if os.path.exists(ovr):
            if self.include_shaders.get():
                for sfold in ["shaderpacks", "shaders"]:
                    sp = os.path.join(ovr, sfold)
                    if os.path.exists(sp):
                        for item in os.listdir(sp):
                            if self.stop_requested:
                                break
                            s = os.path.join(sp, item)
                            d = os.path.join(sh_dir, item)
                            if os.path.isfile(s):
                                shutil.copy2(s, d)
                            elif os.path.isdir(s):
                                shutil.copytree(s, d, dirs_exist_ok=True)
            
            if self.include_resourcepacks.get():
                rp = os.path.join(ovr, "resourcepacks")
                if os.path.exists(rp):
                    for item in os.listdir(rp):
                        if self.stop_requested:
                            break
                        s = os.path.join(rp, item)
                        d = os.path.join(rp_dir, item)
                        if os.path.isfile(s):
                            shutil.copy2(s, d)
                        elif os.path.isdir(s):
                            shutil.copytree(s, d, dirs_exist_ok=True)
        
        if self.stop_requested:
            return
        
        self.update_progress(80)
    
    def get_next_name(self, dir, base, ext):
        c = 1
        while True:
            fn = f"{base}.{ext}" if c == 1 else f"{base} ({c}).{ext}"
            fp = os.path.join(dir, fn)
            if not os.path.exists(fp):
                return fp
            c += 1
    
    def create_zip(self, src, out):
        self.update_status(self.t['creating_zip'], "#60a5fa")
        self.update_progress(85)
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(src):
                for file in files:
                    fp = os.path.join(root, file)
                    an = os.path.relpath(fp, src)
                    z.write(fp, an)
        self.update_progress(100)
    
    def create_7z(self, src, out):
        self.update_status(self.t['creating_7z'], "#60a5fa")
        self.update_progress(85)
        try:
            subprocess.run(['7z'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        except:
            raise Exception(self.t['7z_not_found'])
        cmd = ['7z', 'a', '-t7z', out, os.path.join(src, '*')]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise Exception(self.t['7z_error'].format(res.stderr.decode()))
        self.update_progress(100)
    
    def create_archive(self):
        if not self.modpack_path:
            messagebox.showerror(self.t['error'], self.t['select_modpack_error'])
            return
        
        self.create_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.stop_requested = False
        self.progress['value'] = 0
        
        try:
            dl = str(Path.home() / "Downloads")
            if not os.path.exists(dl):
                dl = str(Path.home())
            
            with tempfile.TemporaryDirectory() as t1:
                with tempfile.TemporaryDirectory() as t2:
                    self.extract_modpack(self.modpack_path, t1)
                    if self.stop_requested:
                        return
                    self.organize_files(t1, t2)
                    if self.stop_requested:
                        return
                    fmt = self.archive_format.get()
                    out = self.get_next_name(dl, "lrshk", fmt)
                    if fmt == "zip":
                        self.create_zip(t2, out)
                    else:
                        self.create_7z(t2, out)
                    if self.stop_requested:
                        if os.path.exists(out):
                            os.remove(out)
                        return
                    self.update_status(self.t['success'], "#4ade80")
                    self.add_to_history(out, self.modpack_path)
                    messagebox.showinfo(self.t['success'], self.t['success_msg'].format(out))
                    if messagebox.askyesno(self.t['open_folder'], self.t['open_folder_msg']):
                        if sys.platform == "win32":
                            os.startfile(dl)
                        elif sys.platform == "darwin":
                            subprocess.run(["open", dl])
                        else:
                            subprocess.run(["xdg-open", dl])
        except Exception as e:
            self.update_status(self.t['error_creating'], "#f87171")
            messagebox.showerror(self.t['error'], self.t['error_msg'].format(str(e)))
        finally:
            self.create_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.stop_requested = False
    
    def start_thread(self):
        threading.Thread(target=self.create_archive, daemon=True).start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    lang = 'en'
    if len(sys.argv) > 1:
        lang = sys.argv[1]
    else:
        exe = os.path.basename(sys.argv[0])
        if '_ru' in exe.lower() or '_RU' in exe or 'Organizer_RU' in exe:
            lang = 'ru'
    app = ModpackArchiver(lang)
    app.run()