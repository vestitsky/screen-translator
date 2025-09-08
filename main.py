import os
import subprocess
import pytesseract

from PIL import Image
from datetime import datetime
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

def select_image_files():
    root = tk.Tk()
    root.withdraw()
    filetypes = [
        ("Изображения", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
        ("Все файлы", "*.*")
    ]
    files = fd.askopenfilenames(
        title="Выберите изображения",
        filetypes=filetypes
    )
    return list(files)

def capture_selected_region():
    try:
        region = subprocess.check_output(["slurp"]).decode().strip()
    except subprocess.CalledProcessError:
        print("Выделение отменено.")
        return None

    filename = f"/tmp/screen_{datetime.now().strftime('%H%M%S')}.png"
    subprocess.run(["grim", "-g", region, filename], check=True)
    return filename

def extract_text_from_image(image_path, lang="eng"):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, lang=lang)
    except Exception as e:
        print(f"OCR ошибка: {e}")
        return ""

def translate_image(lang="eng"):
    path = capture_selected_region()
    if not path:
        return ""
    text = extract_text_from_image(path, lang=lang)
    if os.path.exists(path):
        os.remove(path)
    return GoogleTranslator(source='auto', target='ru').translate(text)


def create_main_window(initial_text=""):
    def translate_current_text():
        current_text = text_widget.get("1.0", tk.END).strip()
        if not current_text:
            return
        
        target_lang = lang_var.get()
        if target_lang == "Выберите язык":
            return
            
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(current_text)
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", translated)
        except Exception as e:
            print(f"Ошибка перевода: {e}")
    
    def add_files_text():
        files = select_image_files()
        if not files:
            return
            
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    file_text = extract_text_from_image(file_path, lang="eng+rus")
                    if file_text.strip():
                        current_text = text_widget.get("1.0", tk.END)
                        if current_text.strip():
                            text_widget.insert(tk.END, "\n\n--- Из файла ---\n")
                        text_widget.insert(tk.END, file_text)
                except Exception as e:
                    print(f"Ошибка обработки файла {file_path}: {e}")
    
    win = tk.Tk()
    win.title("Screen Translator")
    win.geometry("800x600")
    win.configure(bg="black")
    
    # Главный фрейм
    main_frame = tk.Frame(win, bg="black")
    main_frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    # Фрейм для кнопок
    button_frame = tk.Frame(main_frame, bg="black")
    button_frame.pack(fill='x', pady=(0, 10))
    
    # Выпадающий список для выбора языка
    lang_var = tk.StringVar(value="ru")
    lang_options = {
        "ru": "Русский", 
        "en": "English",
        "de": "Deutsch",
        "fr": "Français",
        "es": "Español",
        "it": "Italiano",
        "pt": "Português",
        "pl": "Polski",
        "uk": "Українська"
    }
    
    lang_label = tk.Label(button_frame, text="Перевести на:", bg="black", fg="white", font=("Arial", 12))
    lang_label.pack(side='left', padx=(0, 5))
    
    lang_combo = ttk.Combobox(button_frame, textvariable=lang_var, values=list(lang_options.keys()), 
                              state="readonly", width=12)
    lang_combo.pack(side='left', padx=(0, 10))
    
    # Кнопка перевода
    translate_btn = tk.Button(button_frame, text="Перевести", font=("Arial", 12), 
                             command=translate_current_text, bg="darkblue", fg="white")
    translate_btn.pack(side='left', padx=(0, 10))
    
    # Кнопка добавления файлов
    files_btn = tk.Button(button_frame, text="Распознать файлы", font=("Arial", 12), 
                         command=add_files_text, bg="darkgreen", fg="white")
    files_btn.pack(side='left')
    
    # Текстовое поле
    text_widget = tk.Text(
        main_frame,
        wrap='word',
        bg="black",
        fg="white",
        insertbackground="white",
        font=("Arial", 14)
    )
    text_widget.insert("1.0", initial_text)
    text_widget.pack(expand=True, fill='both')
    
    win.mainloop()


if __name__ == "__main__":
    path = capture_selected_region()
    if path and os.path.exists(path):
        try:
            text = extract_text_from_image(path, lang="eng+rus")
            create_main_window(text)
        finally:
            if os.path.exists(path):
                os.remove(path)
    else:
        print("Скриншот не сделан или отменен.")