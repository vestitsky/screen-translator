#!/bin/bash

# This script automates the installation process for the screen-translator application.

# Update package list and install required packages
sudo pacman -Syu --noconfirm python python-pip python-virtualenv

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt

# Copy the .desktop file to the applications directory
desktop_file="$HOME/.local/share/applications/screen-translator.desktop"
if [ -f "screen-translator.desktop" ]; then
    cp screen-translator.desktop "$desktop_file"
    echo "Desktop entry created at $desktop_file"
else
    echo "Desktop entry file not found."
fi

# Deactivate the virtual environment
deactivate

echo "Installation completed. You can launch the application from your application menu."