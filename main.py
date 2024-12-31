import tkinter as tk
from tkinter import messagebox
import logging
from src.gui import DirectoryCreatorGUI

def main():
    try:
        root = tk.Tk()
        app = DirectoryCreatorGUI(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        messagebox.showerror("Fatal Error", 
            f"A fatal error occurred: {str(e)}\nPlease check the logs for details.")

if __name__ == "__main__":
    main()
