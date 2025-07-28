# Screen Translator

**Screen Translator** is a simple Linux application that allows you to select a screen region or choose image files, recognize text (OCR), and translate it into Russian. The interface is built with Tkinter.

## Features

- Select images for text recognition or translation.
- Capture a selected screen region (Wayland, grim + slurp).
- Recognize text using Tesseract OCR.
- Translate recognized text into Russian via Google Translator.
- User-friendly graphical interface.

## Installation

Install system dependencies (Arch Linux):
```bash
sudo pacman -S tesseract tesseract-data-eng tesseract-data-rus grim slurp python-pip
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```
or using [uv](https://github.com/astral-sh/uv):
```bash
uv pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. When launched, a window will appear with action choices:
    - Recognize text from images
    - Translate text from images
    - Recognize text from a selected screenshot
    - Translate text from a selected screenshot
2. Follow the instructions in the program window.

## Dependencies

- Python 3.13+
- [pytesseract](https://pypi.org/project/pytesseract/)
- [Pillow](https://pypi.org/project/Pillow/)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
- grim, slurp (for screen capture, Wayland only)

## Notes

- For OCR in Russian, install the `tesseract-data-rus` package.
- The program works only in Wayland environments with grim/slurp.
- Internet connection is required for translation.