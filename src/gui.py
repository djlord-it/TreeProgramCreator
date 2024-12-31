import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from src.security import SecurityValidator
from src.creator import DirectoryCreator
from src.logger import setup_logging

class DirectoryCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Structure Creator")
        self.root.geometry("800x600")
        self.logger = setup_logging()
        self.validator = SecurityValidator()
        self.creator = DirectoryCreator()
        self.setup_ui()
        
    def setup_ui(self):
        style = ttk.Style()
        style.configure('TButton', padding=6)
        style.configure('TFrame', padding=10)
        

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        

        input_frame = ttk.LabelFrame(main_frame, text="Tree Structure Input", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.text_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        

        self.load_default_text()
        

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.path_var = tk.StringVar(value="Select destination directory...")
        path_label = ttk.Label(button_frame, textvariable=self.path_var, wraplength=600)
        path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(button_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        create_btn = ttk.Button(button_frame, text="Create Structure", 
            command=self.create_structure_with_confirmation)
        create_btn.pack(side=tk.RIGHT)
        

        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=600)
        status_label.pack(fill=tk.X, pady=5)

    def load_default_text(self):
        default_text = """This/
├── is/
│   ├── a/
│   │   └── file.txt
│   ├── and.txt
│   └── another/
│       └── file.txt
├── and/
│   └── a directory.txt
└── structure.txt
"""
        self.text_area.insert(tk.END, default_text)

    def browse_directory(self):
        try:
            directory = filedialog.askdirectory()
            if directory:
                is_safe, message = self.validator.is_safe_path(directory, check_exists=True)
                if is_safe:
                    self.path_var.set(directory)
                    self.logger.info(f"Selected directory: {directory}")
                else:
                    self.show_error(f"Invalid directory: {message}")
        except Exception as e:
            self.logger.error(f"Error in directory browser: {str(e)}")
            self.show_error("Error selecting directory")

    def create_structure_with_confirmation(self):
        if not self.path_var.get() or self.path_var.get() == "Select destination directory...":
            self.show_error("Please select a destination directory first!")
            return

        if not messagebox.askyesno("Confirm", 
            "Are you sure you want to create the directory structure?"):
            return
            
        try:
            tree_lines = self.text_area.get("1.0", tk.END).splitlines()
            success, message = self.creator.create_structure_from_tree(
                tree_lines, self.path_var.get())
            
            if success:
                self.status_var.set(message)
                self.logger.info("Structure created successfully")
                self.root.after(2000, lambda: self.status_var.set(""))
            else:
                self.show_error(message)
                
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self.show_error(f"An unexpected error occurred: {str(e)}")

    def show_error(self, message):
        self.status_var.set(f"Error: {message}")
        messagebox.showerror("Error", message)
        self.logger.error(message)
