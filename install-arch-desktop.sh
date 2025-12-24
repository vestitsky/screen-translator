#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Определяем директорию скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$HOME/.local/share/applications/screen-translator.desktop"
ICON_FILE="$HOME/.local/share/applications/translate icon.png"
VENV_DIR="$SCRIPT_DIR/.venv"

echo -e "${BLUE}=== Screen Translator Installation ===${NC}\n"

# Проверяем системные зависимости
echo -e "${YELLOW}→ Проверка системных зависимостей...${NC}"
MISSING_DEPS=()

command -v tesseract &>/dev/null || MISSING_DEPS+=("tesseract")
command -v grim &>/dev/null || MISSING_DEPS+=("grim")
command -v slurp &>/dev/null || MISSING_DEPS+=("slurp")

# Проверяем наличие tk/tkinter
if ! pacman -Q tk &>/dev/null; then
  MISSING_DEPS+=("tk")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
  echo -e "${RED}✗ Отсутствуют системные зависимости: ${MISSING_DEPS[*]}${NC}"
  echo -e "${YELLOW}Установите их командой:${NC}"
  echo "sudo pacman -S tesseract tesseract-data-eng tesseract-data-rus grim slurp tk"
  exit 1
fi
echo -e "${GREEN}✓ Системные зависимости установлены${NC}"

# Проверяем tkinter в Python
echo -e "${YELLOW}→ Проверка tkinter...${NC}"
if ! python -c "import tkinter" 2>/dev/null; then
  echo -e "${RED}✗ tkinter не доступен в Python${NC}"
  echo -e "${YELLOW}Установите tk:${NC} sudo pacman -S tk"
  exit 1
fi
echo -e "${GREEN}✓ tkinter доступен${NC}"

# Удаляем старое виртуальное окружение если есть pyproject.toml
if [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
  echo -e "${YELLOW}→ Удаление старого pyproject.toml...${NC}"
  rm -f "$SCRIPT_DIR/pyproject.toml"
fi

# Создаем виртуальное окружение
if [ -d "$VENV_DIR" ]; then
  echo -e "${YELLOW}→ Виртуальное окружение существует, пересоздаем...${NC}"
  rm -rf "$VENV_DIR"
fi

echo -e "${YELLOW}→ Создание виртуального окружения с доступом к системным пакетам...${NC}"
python -m venv --system-site-packages "$VENV_DIR"
echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"

# Активируем и устанавливаем зависимости
echo -e "${YELLOW}→ Установка Python зависимостей...${NC}"
source "$VENV_DIR/bin/activate"

# Обновляем pip
pip install --upgrade pip >/dev/null 2>&1

# Устанавливаем зависимости (без tkinter)
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
  # Фильтруем tkinter из requirements.txt
  grep -v "^tkinter" "$SCRIPT_DIR/requirements.txt" >/tmp/requirements_filtered.txt
  pip install -r /tmp/requirements_filtered.txt
  rm /tmp/requirements_filtered.txt
else
  pip install pytesseract Pillow deep-translator
fi

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ Python зависимости установлены${NC}"
else
  echo -e "${RED}✗ Ошибка при установке зависимостей${NC}"
  exit 1
fi

deactivate

# Создаем директорию для desktop файла
mkdir -p "$HOME/.local/share/applications"

# Создаем/обновляем .desktop файл
echo -e "${YELLOW}→ Создание desktop entry...${NC}"
cat >"$DESKTOP_FILE" <<DESKTOP
[Desktop Entry]
Version=1.0
Name=Screen Translator
Comment=Capture screen region, extract text, and translate it
Exec=/bin/sh -c 'cd $SCRIPT_DIR && source .venv/bin/activate && python main.py'
Icon=$ICON_FILE
Terminal=false
Type=Application
Categories=Utility;Application;
DESKTOP

# Делаем .desktop файл исполняемым
chmod +x "$DESKTOP_FILE"

# Обновляем базу данных desktop-файлов
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo ""
echo -e "${GREEN}✓ Desktop entry установлен/обновлен:${NC} $DESKTOP_FILE"
echo -e "${GREEN}✓ Путь к проекту:${NC} $SCRIPT_DIR"
echo -e "${GREEN}✓ Виртуальное окружение:${NC} $VENV_DIR"
echo ""
echo -e "${BLUE}Готово! Способы запуска:${NC}"
echo -e "  1. ${YELLOW}gtk-launch screen-translator${NC}"
echo -e "  2. ${YELLOW}Super+Shift+T${NC} (в Hyperland)"
echo -e "  3. ${YELLOW}cd $SCRIPT_DIR && source .venv/bin/activate && python main.py${NC}"
echo ""

# Опционально: тестовый запуск
read -p "Хотите протестировать запуск сейчас? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[YyДд]$ ]]; then
  echo -e "${YELLOW}→ Запуск приложения...${NC}"
  cd "$SCRIPT_DIR"
  source .venv/bin/activate
  python main.py &
  PID=$!
  sleep 2
  if ps -p $PID >/dev/null; then
    echo -e "${GREEN}✓ Приложение запущено (PID: $PID)${NC}"
  else
    echo -e "${RED}✗ Ошибка при запуске${NC}"
  fi
fi
