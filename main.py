import keyboard

def callback_function():
    print("Hotkey pressed!")

keyboard.add_hotkey('ctrl+alt+t', callback_function)
keyboard.wait()  # бесконечно ждёт нажатий