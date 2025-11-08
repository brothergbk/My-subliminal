import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import pandas as pd
import pygame
import threading
import time
import json
import os
from pathlib import Path

class SubliminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subliminal Message App")
        self.root.geometry("900x700")

        # Modern color scheme
        self.colors = {
            "bg": "#1e1e2e",
            "fg": "#cdd6f4",
            "primary": "#89b4fa",
            "secondary": "#f38ba8",
            "accent": "#a6e3a1",
            "surface": "#313244",
            "hover": "#45475a"
        }

        # Configure root window
        self.root.configure(bg=self.colors["bg"])

        # Default settings
        self.settings = {
            "flash_duration": 0.1,  # seconds
            "interval": 5,          # seconds between flashes
            "font_size": 36,
            "text_color": "#FFFFFF",
            "bg_color": "#000000",
            "opacity": 0.8
        }

        # Categories and words
        self.categories = {}  # {category_name: [words]}
        self.selected_categories = set()  # Set of selected category names
        self.words = []
        self.current_word_index = 0
        self.is_running = False
        self.flash_thread = None

        self.setup_modern_ui()
        self.load_settings()
        
    def setup_modern_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors for ttk widgets
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"], font=("Segoe UI", 10))
        style.configure("TButton", background=self.colors["primary"], foreground=self.colors["bg"],
                       font=("Segoe UI", 10, "bold"), borderwidth=0, focuscolor='none')
        style.map("TButton", background=[("active", self.colors["hover"])])
        style.configure("Accent.TButton", background=self.colors["accent"], foreground=self.colors["bg"])
        style.configure("TLabelframe", background=self.colors["bg"], foreground=self.colors["fg"],
                       borderwidth=2, relief="flat")
        style.configure("TLabelframe.Label", background=self.colors["bg"], foreground=self.colors["primary"],
                       font=("Segoe UI", 11, "bold"))
        style.configure("TCheckbutton", background=self.colors["bg"], foreground=self.colors["fg"],
                       font=("Segoe UI", 10))

        # Main container with two columns
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Categories
        left_panel = tk.Frame(main_container, bg=self.colors["bg"])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Right panel - Settings and Controls
        right_panel = tk.Frame(main_container, bg=self.colors["bg"])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # === LEFT PANEL ===
        # Category management
        category_frame = ttk.LabelFrame(left_panel, text="📁 Categories", padding="15")
        category_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Category buttons
        cat_button_frame = tk.Frame(category_frame, bg=self.colors["bg"])
        cat_button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(cat_button_frame, text="➕ Add Category",
                  command=self.add_category).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(cat_button_frame, text="📂 Load from File",
                  command=self.load_category_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(cat_button_frame, text="🗑️ Delete",
                  command=self.delete_category, style="Accent.TButton").pack(side=tk.LEFT, padx=5)

        # Category list with checkboxes
        cat_list_frame = tk.Frame(category_frame, bg=self.colors["surface"], relief=tk.FLAT, bd=2)
        cat_list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for categories
        cat_scrollbar = tk.Scrollbar(cat_list_frame, bg=self.colors["surface"])
        cat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.category_listbox = tk.Listbox(cat_list_frame, bg=self.colors["surface"],
                                          fg=self.colors["fg"], selectmode=tk.MULTIPLE,
                                          font=("Segoe UI", 10), borderwidth=0,
                                          highlightthickness=0, selectbackground=self.colors["primary"],
                                          yscrollcommand=cat_scrollbar.set)
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cat_scrollbar.config(command=self.category_listbox.yview)
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)

        # Words in selected categories
        words_frame = ttk.LabelFrame(left_panel, text="📝 Words in Selected Categories", padding="15")
        words_frame.pack(fill=tk.BOTH, expand=True)

        words_list_frame = tk.Frame(words_frame, bg=self.colors["surface"], relief=tk.FLAT, bd=2)
        words_list_frame.pack(fill=tk.BOTH, expand=True)

        words_scrollbar = tk.Scrollbar(words_list_frame, bg=self.colors["surface"])
        words_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.words_text = tk.Text(words_list_frame, bg=self.colors["surface"],
                                 fg=self.colors["fg"], font=("Segoe UI", 10),
                                 borderwidth=0, highlightthickness=0, wrap=tk.WORD,
                                 yscrollcommand=words_scrollbar.set, height=10)
        self.words_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        words_scrollbar.config(command=self.words_text.yview)

        # Update button
        ttk.Button(words_frame, text="✓ Update Active Words",
                  command=self.update_words_from_text).pack(pady=(10, 0))

        # === RIGHT PANEL ===
        # Settings frame
        settings_frame = ttk.LabelFrame(right_panel, text="⚙️ Flash Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Flash duration
        ttk.Label(settings_frame, text="Flash Duration (s):").grid(row=0, column=0, sticky=tk.W)
        self.duration_var = tk.DoubleVar(value=self.settings["flash_duration"])
        ttk.Scale(settings_frame, from_=0.05, to=1.0, variable=self.duration_var, 
                 orient=tk.HORIZONTAL, command=self.update_duration_label).grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.duration_label = ttk.Label(settings_frame, text=f"{self.settings['flash_duration']}s")
        self.duration_label.grid(row=0, column=2, padx=5)
        
        # Interval
        ttk.Label(settings_frame, text="Interval (s):").grid(row=1, column=0, sticky=tk.W)
        self.interval_var = tk.DoubleVar(value=self.settings["interval"])
        ttk.Scale(settings_frame, from_=1, to=30, variable=self.interval_var,
                 orient=tk.HORIZONTAL, command=self.update_interval_label).grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.interval_label = ttk.Label(settings_frame, text=f"{self.settings['interval']}s")
        self.interval_label.grid(row=1, column=2, padx=5)
        
        # Font size
        ttk.Label(settings_frame, text="Font Size:").grid(row=2, column=0, sticky=tk.W)
        self.font_size_var = tk.IntVar(value=self.settings["font_size"])
        ttk.Scale(settings_frame, from_=12, to=72, variable=self.font_size_var,
                 orient=tk.HORIZONTAL, command=self.update_font_size_label).grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.font_size_label = ttk.Label(settings_frame, text=str(self.settings["font_size"]))
        self.font_size_label.grid(row=2, column=2, padx=5)
        
        # Text color
        ttk.Label(settings_frame, text="Text Color:").grid(row=3, column=0, sticky=tk.W)
        self.text_color_var = tk.StringVar(value=self.settings["text_color"])
        color_frame = ttk.Frame(settings_frame)
        color_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Entry(color_frame, textvariable=self.text_color_var, width=10).grid(row=0, column=0, padx=5)
        ttk.Button(color_frame, text="Pick", command=self.pick_text_color).grid(row=0, column=1)
        
        # Background color
        ttk.Label(settings_frame, text="Background Color:").grid(row=4, column=0, sticky=tk.W)
        self.bg_color_var = tk.StringVar(value=self.settings["bg_color"])
        bg_color_frame = ttk.Frame(settings_frame)
        bg_color_frame.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Entry(bg_color_frame, textvariable=self.bg_color_var, width=10).grid(row=0, column=0, padx=5)
        ttk.Button(bg_color_frame, text="Pick", command=self.pick_bg_color).grid(row=0, column=1)
        
        # Opacity
        ttk.Label(settings_frame, text="Opacity:").grid(row=5, column=0, sticky=tk.W)
        self.opacity_var = tk.DoubleVar(value=self.settings["opacity"])
        ttk.Scale(settings_frame, from_=0.1, to=1.0, variable=self.opacity_var,
                 orient=tk.HORIZONTAL, command=self.update_opacity_label).grid(row=5, column=1, sticky=(tk.W, tk.E))
        self.opacity_label = ttk.Label(settings_frame, text=f"{self.settings['opacity']:.1f}")
        self.opacity_label.grid(row=5, column=2, padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.start_button = ttk.Button(control_frame, text="Start Flashing", command=self.start_flashing)
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Flashing", command=self.stop_flashing, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready to load word list")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Words preview
        preview_frame = ttk.LabelFrame(main_frame, text="Loaded Words (Editable - one word per line)", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.words_text = tk.Text(preview_frame, height=8, width=50, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.words_text.yview)
        self.words_text.config(yscrollcommand=scrollbar.set)
        self.words_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Button to update words from edited text
        update_button = ttk.Button(preview_frame, text="Update Words from Text", command=self.update_words_from_text)
        update_button.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
    def update_duration_label(self, value):
        self.duration_label.config(text=f"{float(value):.2f}s")
        
    def update_interval_label(self, value):
        self.interval_label.config(text=f"{float(value):.1f}s")
        
    def update_font_size_label(self, value):
        self.font_size_label.config(text=str(int(float(value))))
        
    def update_opacity_label(self, value):
        self.opacity_label.config(text=f"{float(value):.1f}")
        
    def pick_text_color(self):
        color = self.ask_color(self.text_color_var.get())
        if color:
            self.text_color_var.set(color)
            
    def pick_bg_color(self):
        color = self.ask_color(self.bg_color_var.get())
        if color:
            self.bg_color_var.set(color)
            
    def ask_color(self, initial_color):
        try:
            from tkinter import colorchooser
            color = colorchooser.askcolor(initialcolor=initial_color)
            return color[1] if color[1] else initial_color
        except:
            return initial_color
            
    def load_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                # Stop flashing if currently running
                if self.is_running:
                    self.stop_flashing()

                # Read file as newline-delimited text
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Remove empty lines and strip whitespace
                self.words = [line.strip() for line in lines if line.strip()]

                # Reset word index to start from beginning
                self.current_word_index = 0
                self.file_label.config(text=os.path.basename(file_path))
                self.update_words_preview()
                self.status_label.config(text=f"Loaded {len(self.words)} words (replaced previous list)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
                
    def update_words_preview(self):
        self.words_text.delete(1.0, tk.END)
        if self.words:
            preview = "\n".join(self.words)  # Show all words
            self.words_text.insert(1.0, preview)

    def update_words_from_text(self):
        """Update the word list from the edited text in the preview window"""
        try:
            # Stop flashing if currently running
            if self.is_running:
                self.stop_flashing()

            # Get text from the text widget
            text_content = self.words_text.get(1.0, tk.END)

            # Split by newlines and remove empty lines
            self.words = [line.strip() for line in text_content.split('\n') if line.strip()]

            # Reset word index
            self.current_word_index = 0

            # Update status
            self.status_label.config(text=f"Updated to {len(self.words)} words from edited text")

            messagebox.showinfo("Success", f"Word list updated with {len(self.words)} words")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update words: {str(e)}")
            
    def get_current_settings(self):
        return {
            "flash_duration": self.duration_var.get(),
            "interval": self.interval_var.get(),
            "font_size": self.font_size_var.get(),
            "text_color": self.text_color_var.get(),
            "bg_color": self.bg_color_var.get(),
            "opacity": self.opacity_var.get()
        }
        
    def start_flashing(self):
        if not self.words:
            messagebox.showwarning("Warning", "Please load a CSV file with words first.")
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Minimize the main window
        self.root.iconify()
        
        # Start flashing in a separate thread
        self.flash_thread = threading.Thread(target=self.flash_loop, daemon=True)
        self.flash_thread.start()
        
    def stop_flashing(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Restore the main window
        self.root.deiconify()
        
    def flash_loop(self):
        pygame.init()

        # Get screen info and create fullscreen window
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h

        # Create a borderless window that covers the entire screen
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        pygame.display.set_caption("Subliminal Messages")

        # Set a color key for transparency (magenta is commonly used)
        transparent_color = (255, 0, 255)

        # Make the window always on top and set layered window attributes for transparency (Windows)
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()["window"]
            # Set window to always on top
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
            # Set layered window style
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            LWA_COLORKEY = 0x00000001

            # Get current extended style
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            # Add layered window style
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED)
            # Set the transparent color key
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd,
                ctypes.c_ulong(transparent_color[2] << 16 | transparent_color[1] << 8 | transparent_color[0]),
                0, LWA_COLORKEY)
        except:
            pass  # Fallback if we can't set transparency

        clock = pygame.time.Clock()

        # Fill screen with transparent color initially
        screen.fill(transparent_color)
        pygame.display.flip()

        while self.is_running and self.words:
            settings = self.get_current_settings()

            # Get current word
            word = self.words[self.current_word_index]
            self.current_word_index = (self.current_word_index + 1) % len(self.words)

            # Flash the word
            self.flash_word(screen, screen_width, screen_height, word, settings, transparent_color)

            # Wait for the interval
            for _ in range(int(settings["interval"] * 10)):
                if not self.is_running:
                    break
                time.sleep(0.1)
                # Check for events to prevent freezing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                        break

        pygame.quit()
        
    def flash_word(self, screen, screen_width, screen_height, word, settings, transparent_color):
        # Convert hex color to RGB
        try:
            text_color = self.hex_to_rgb(settings["text_color"])
        except:
            text_color = (255, 255, 255)

        # Create font
        font = pygame.font.SysFont('Arial', settings["font_size"])
        text_surface = font.render(word, True, text_color)
        text_rect = text_surface.get_rect(center=(screen_width//2, screen_height//2))

        # Fill entire screen with transparent color first
        screen.fill(transparent_color)

        # Display only the text (no background)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Keep displayed for flash duration
        start_time = time.time()
        while time.time() - start_time < settings["flash_duration"] and self.is_running:
            clock = pygame.time.Clock()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break

        # Clear screen with transparent color
        screen.fill(transparent_color)
        pygame.display.flip()
        
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def load_settings(self):
        try:
            if os.path.exists("subliminal_settings.json"):
                with open("subliminal_settings.json", "r") as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
                    
                # Update UI with loaded settings
                self.duration_var.set(self.settings["flash_duration"])
                self.interval_var.set(self.settings["interval"])
                self.font_size_var.set(self.settings["font_size"])
                self.text_color_var.set(self.settings["text_color"])
                self.bg_color_var.set(self.settings["bg_color"])
                self.opacity_var.set(self.settings["opacity"])
                
                self.update_duration_label(self.settings["flash_duration"])
                self.update_interval_label(self.settings["interval"])
                self.update_font_size_label(self.settings["font_size"])
                self.update_opacity_label(self.settings["opacity"])
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save_settings(self):
        try:
            self.settings.update(self.get_current_settings())
            with open("subliminal_settings.json", "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def on_closing(self):
        self.stop_flashing()
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SubliminalApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()