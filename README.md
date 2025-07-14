# README for Screen Translator

# Screen Translator

Screen Translator is a Python application that captures a selected region of the screen, extracts text from the image using Optical Character Recognition (OCR), translates the text, and displays the result in a graphical user interface (GUI) window.

## Features

- Capture a selected region of the screen.
- Extract text from images using OCR.
- Translate extracted text into a specified language.
- Display the translated text in a user-friendly GUI.

## Requirements

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- `pytesseract`
- `Pillow`
- `deep-translator`

You can install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd screen-translator
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the application:

   ```bash
   python setup.py install
   ```

4. Make the application executable:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

5. Create a desktop entry for easy access:

   The `screen-translator.desktop` file is included in the project. You can copy it to your local applications directory:

   ```bash
   cp screen-translator.desktop ~/.local/share/applications/
   ```

## Usage

To run the application, you can either:

- Launch it from the application menu.
- Run the following command in the terminal:

```bash
python src/main.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.