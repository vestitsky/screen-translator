import os
import subprocess
import pytesseract

from PIL import Image
from datetime import datetime
from deep_translator import GoogleTranslator
import tkinter as tk
from tkinter import filedialog as fd

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

def show_result(text):
    win = tk.Tk()
    win.title("Результат перевода")
    win.geometry("600x400")
    win.configure(bg="black")

    txt = tk.Text(
        win,
        wrap='word',
        bg="black",
        fg="white",
        insertbackground="white",
        font=("Arial", 18)
    )
    txt.insert("1.0", text)
    txt.pack(expand=True, fill='both')
    win.mainloop()

def main_menu():
    def set_mode(val):
        nonlocal mode
        mode = val
        root.destroy()

    mode = None
    root = tk.Tk()
    root.title("Screen Translator — выбор действия")
    root.geometry("400x300")
    root.configure(bg="black")

    outer_frame = tk.Frame(root, bg="black")
    outer_frame.pack(expand=True, fill='both')

    inner_frame = tk.Frame(outer_frame, bg="black")
    inner_frame.place(relx=0.5, rely=0.5, anchor='center')

    btn1 = tk.Button(inner_frame, text="Распознать текст с изображений", font=("Arial", 14), command=lambda: set_mode("extract_images"))
    btn2 = tk.Button(inner_frame, text="Перевести текст с изображений", font=("Arial", 14), command=lambda: set_mode("translate_images"))
    btn3 = tk.Button(inner_frame, text="Распознать текст с выделенного скриншота", font=("Arial", 14), command=lambda: set_mode("extract_screenshot"))
    btn4 = tk.Button(inner_frame, text="Перевести текст с выделенного скриншота", font=("Arial", 14), command=lambda: set_mode("translate_screenshot"))

    for btn in (btn1, btn2, btn3, btn4):
        btn.pack(pady=10, fill='x', padx=20)

    root.mainloop()
    return mode

if __name__ == "__main__":
    mode = main_menu()
    if mode == "extract_images":
        images_list = select_image_files()
        for path in images_list:
            if os.path.exists(path):
                text = extract_text_from_image(path, lang="eng+rus")
                show_result(text)
            else:
                print(f"Файл не найден: {path}")
    elif mode == "translate_images":
        images_list = select_image_files()
        for path in images_list:
            if os.path.exists(path):
                text = extract_text_from_image(path, lang="eng+rus")
                translated = GoogleTranslator(source='auto', target='ru').translate(text)
                show_result(translated)
            else:
                print(f"Файл не найден: {path}")
    elif mode == "extract_screenshot":
        path = capture_selected_region()
        if path and os.path.exists(path):
            text = extract_text_from_image(path, lang="eng+rus")
            show_result(text)
            os.remove(path)
    elif mode == "translate_screenshot":
        result = translate_image(lang="eng+rus")
        if result.strip():
            show_result(result)