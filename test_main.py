import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from main import create_main_window

class TestMainWindow(unittest.TestCase):
    @patch('main.select_image_files')
    @patch('main.extract_text_from_image')
    @patch('main.GoogleTranslator')
    def test_copy_button_exists(self, mock_translator, mock_extract, mock_select):
        # Mock the translator to avoid real API calls
        mock_translator.return_value.translate.return_value = "translated text"

        # We need a root window to run the tests
        root = tk.Tk()
        # Prevent the window from showing up
        root.withdraw()

        # We need to pass our root to create_main_window
        # but it creates its own, so we need to patch tk.Tk()
        with patch('tkinter.Tk', return_value=root):
            create_main_window("initial text")

            # Find the copy button
            copy_button = None
            # Search for the button in the root window's children
            for widget in root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for sub_widget in widget.winfo_children():
                        if isinstance(sub_widget, tk.Frame):
                             for button_widget in sub_widget.winfo_children():
                                if isinstance(button_widget, tk.Button) and button_widget.cget("text") == "Копировать":
                                    copy_button = button_widget
                                    break
            
            self.assertIsNotNone(copy_button, "Copy button not found")
            
            # Check the button's command
            self.assertIsNotNone(copy_button.cget("command"), "Copy button has no command")
            
            # Test the copy functionality
            text_widget = root.winfo_children()[0].winfo_children()[2]
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", "text to copy")
            
            # Mock clipboard methods
            root.clipboard_clear = MagicMock()
            root.clipboard_append = MagicMock()
            
            # Call the button's command
            copy_button.invoke()
            
            root.clipboard_clear.assert_called_once()
            root.clipboard_append.assert_called_once_with("text to copy")

        # Destroy the window after the test
        root.destroy()

if __name__ == '__main__':
    unittest.main()
