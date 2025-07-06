import os

import subprocess
import pytesseract

from PIL import Image
from datetime import datetime
from deep_translator import GoogleTranslator

def capture_selected_region():
    """Выделение области и захват скриншота"""
    try:
        # Получить координаты выделенной области
        region = subprocess.check_output(["slurp"]).decode().strip()
    except subprocess.CalledProcessError:
        print("Выделение области отменено.")
        return None

    # Путь к временному файлу
    filename = f"/tmp/screen_region_{datetime.now().strftime('%H%M%S')}.png"

    # Сделать скриншот
    subprocess.run(["grim", "-g", region, filename], check=True)

    return filename

def extract_text_from_image(image_path, lang="eng"):
    """Извлекает текст из изображения"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        print(f"OCR ошибка: {e}")
        return ""

def capture_and_ocr(lang="eng"):
    """Комбинированный шаг: выделение + захват + OCR"""
    image_path = capture_selected_region()
    if not image_path:
        return ""

    text = extract_text_from_image(image_path, lang=lang)

    # Удалить скриншот после использования
    if os.path.exists(image_path):
        os.remove(image_path)

    return text

def translate(lang="eng"):
    """Комбинированный шаг: выделение + захват + OCR + перевод"""
    image_path = capture_selected_region()
    if not image_path:
        return ""

    text = extract_text_from_image(image_path, lang=lang)

    # Удалить скриншот
    if os.path.exists(image_path):
        os.remove(image_path)

    # Перевод
    translated = GoogleTranslator(source='auto', target='ru').translate(text)
    return translated


# Пример запуска
if __name__ == "__main__":
    result = translate(lang="eng+rus")
    print("Распознанный текст:\n")
    print(result)

