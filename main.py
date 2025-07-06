import os
import subprocess
import pytesseract

from PIL import Image
from datetime import datetime
from deep_translator import GoogleTranslator
import tkinter as tk

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
    txt = tk.Text(win, wrap='word')
    txt.insert("1.0", text)
    txt.pack(expand=True, fill='both')
    win.mainloop()

if __name__ == "__main__":
    result = translate_image(lang="eng+rus")
    if result.strip():
        show_result(result)

