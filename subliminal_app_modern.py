import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import pygame
import threading
import time
import json
import os
from pathlib import Path

class SubliminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subliminal Message App - Modern")
        self.root.geometry("1000x750")

        # Modern color scheme (Catppuccin Mocha inspired)
        self.colors = {
            "bg": "#1e1e2e",
            "fg": "#cdd6f4",
            "primary": "#89b4fa",
            "secondary": "#f38ba8",
            "accent": "#a6e3a1",
            "surface": "#313244",
            "hover": "#45475a",
            "overlay": "#6c7086"
        }

        # Configure root window
        self.root.configure(bg=self.colors["bg"])

        # Default settings
        self.settings = {
            "flash_duration": 0.1,
            "interval": 5,
            "font_size": 36,
            "text_color": "#FFFFFF"
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
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"],
                       font=("Segoe UI", 10))
        style.configure("TButton", background=self.colors["primary"], foreground="#000000",
                       font=("Segoe UI", 10, "bold"), borderwidth=0, focuscolor='none', padding=8)
        style.map("TButton", background=[("active", self.colors["hover"])])

        style.configure("Accent.TButton", background=self.colors["accent"], foreground="#000000")
        style.configure("Danger.TButton", background=self.colors["secondary"], foreground="#000000")

        style.configure("TLabelframe", background=self.colors["bg"], foreground=self.colors["fg"],
                       borderwidth=2, relief="flat")
        style.configure("TLabelframe.Label", background=self.colors["bg"], foreground=self.colors["primary"],
                       font=("Segoe UI", 11, "bold"))

        # Main container with two columns
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Left panel - Categories
        left_panel = tk.Frame(main_container, bg=self.colors["bg"])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        # Right panel - Settings and Controls
        right_panel = tk.Frame(main_container, bg=self.colors["bg"])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

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
                  command=self.delete_category, style="Danger.TButton").pack(side=tk.LEFT, padx=5)

        # Category list with checkboxes
        cat_list_frame = tk.Frame(category_frame, bg=self.colors["surface"], relief=tk.FLAT, bd=2)
        cat_list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for categories
        cat_scrollbar = tk.Scrollbar(cat_list_frame, bg=self.colors["surface"])
        cat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.category_listbox = tk.Listbox(cat_list_frame, bg=self.colors["surface"],
                                          fg=self.colors["fg"], selectmode=tk.MULTIPLE,
                                          font=("Segoe UI", 11), borderwidth=0,
                                          highlightthickness=0, selectbackground=self.colors["primary"],
                                          selectforeground="#000000",
                                          yscrollcommand=cat_scrollbar.set, activestyle='none')
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
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
                                 yscrollcommand=words_scrollbar.set, height=10,
                                 insertbackground=self.colors["primary"])
        self.words_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        words_scrollbar.config(command=self.words_text.yview)

        # Update button
        ttk.Button(words_frame, text="✓ Update Active Words",
                  command=self.update_words_from_text, style="Accent.TButton").pack(pady=(10, 0), fill=tk.X)

        # === RIGHT PANEL ===
        # Settings frame
        settings_frame = ttk.LabelFrame(right_panel, text="⚙️ Flash Settings", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Create modern sliders
        def create_slider(parent, row, label, var, from_, to_, format_str="{:.2f}"):
            label_widget = ttk.Label(parent, text=label)
            label_widget.grid(row=row, column=0, sticky=tk.W, pady=10, padx=(0, 10))

            slider_container = tk.Frame(parent, bg=self.colors["bg"])
            slider_container.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=10)

            scale = ttk.Scale(slider_container, from_=from_, to=to_, variable=var, orient=tk.HORIZONTAL)
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

            value_label = tk.Label(slider_container, text=format_str.format(var.get()),
                                  bg=self.colors["bg"], fg=self.colors["accent"],
                                  font=("Segoe UI", 10, "bold"), width=6)
            value_label.pack(side=tk.RIGHT, padx=(10, 0))

            scale.config(command=lambda v: value_label.config(text=format_str.format(float(v))))
            return scale, value_label

        # Flash Duration
        self.flash_duration_var = tk.DoubleVar(value=self.settings["flash_duration"])
        create_slider(settings_frame, 0, "⚡ Flash Duration (s):", self.flash_duration_var, 0.05, 1.0, "{:.2f}")

        # Interval
        self.interval_var = tk.DoubleVar(value=self.settings["interval"])
        create_slider(settings_frame, 1, "⏱️ Interval (s):", self.interval_var, 1, 30, "{:.1f}")

        # Font Size
        self.font_size_var = tk.IntVar(value=self.settings["font_size"])
        create_slider(settings_frame, 2, "🔤 Font Size:", self.font_size_var, 12, 100, "{:.0f}")

        # Text Color
        color_label = ttk.Label(settings_frame, text="🎨 Text Color:")
        color_label.grid(row=3, column=0, sticky=tk.W, pady=10, padx=(0, 10))

        color_container = tk.Frame(settings_frame, bg=self.colors["bg"])
        color_container.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=10)

        self.text_color_var = tk.StringVar(value=self.settings["text_color"])

        self.color_display = tk.Frame(color_container, bg=self.settings["text_color"],
                                width=40, height=30, relief=tk.RAISED, bd=2)
        self.color_display.pack(side=tk.LEFT, padx=(0, 10))

        def choose_color():
            color = colorchooser.askcolor(initialcolor=self.text_color_var.get())[1]
            if color:
                self.text_color_var.set(color)
                self.color_display.config(bg=color)

        ttk.Button(color_container, text="Choose Color", command=choose_color).pack(side=tk.LEFT)

        settings_frame.columnconfigure(1, weight=1)

        # Control buttons
        control_frame = ttk.LabelFrame(right_panel, text="🎮 Controls", padding="15")
        control_frame.pack(fill=tk.X, pady=(0, 10))

        self.start_button = ttk.Button(control_frame, text="▶️ Start Flashing",
                                      command=self.start_flashing, style="Accent.TButton")
        self.start_button.pack(fill=tk.X, pady=5)

        self.stop_button = ttk.Button(control_frame, text="⏹️ Stop Flashing",
                                     command=self.stop_flashing, state=tk.DISABLED,
                                     style="Danger.TButton")
        self.stop_button.pack(fill=tk.X, pady=5)

        # Status
        status_frame = ttk.LabelFrame(right_panel, text="📊 Status", padding="15")
        status_frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(status_frame, text="Ready - Add categories to begin",
                                    bg=self.colors["surface"], fg=self.colors["accent"],
                                    font=("Segoe UI", 10), relief=tk.FLAT,
                                    padx=15, pady=15, anchor=tk.W, wraplength=350)
        self.status_label.pack(fill=tk.BOTH, expand=True)

        self.category_count_label = tk.Label(status_frame, text="Categories: 0 | Selected: 0 | Words: 0",
                                            bg=self.colors["surface"], fg=self.colors["fg"],
                                            font=("Segoe UI", 9), relief=tk.FLAT,
                                            padx=15, pady=10, anchor=tk.W)
        self.category_count_label.pack(fill=tk.X)



    def add_category(self):
        """Add a new category with a name"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Category")
        dialog.geometry("400x150")
        dialog.configure(bg=self.colors["bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Category Name:").pack(pady=10)

        name_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=30)
        name_entry.pack(pady=5)
        name_entry.focus()

        def save_category():
            name = name_entry.get().strip()
            if name:
                if name in self.categories:
                    messagebox.showwarning("Duplicate", f"Category '{name}' already exists!")
                else:
                    self.categories[name] = []
                    self.update_category_list()
                    self.update_status()
                    dialog.destroy()
            else:
                messagebox.showwarning("Invalid", "Please enter a category name!")

        button_frame = tk.Frame(dialog, bg=self.colors["bg"])
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Save", command=save_category,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        name_entry.bind('<Return>', lambda e: save_category())

    def load_category_from_file(self):
        """Load a category from a file"""
        file_path = filedialog.askopenfilename(
            title="Select word list file",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            try:
                # Read file as newline-delimited text
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Remove empty lines and strip whitespace
                words = [line.strip() for line in lines if line.strip()]

                if not words:
                    messagebox.showwarning("Empty File", "The selected file contains no words!")
                    return

                # Ask for category name
                category_name = os.path.splitext(os.path.basename(file_path))[0]

                dialog = tk.Toplevel(self.root)
                dialog.title("Name Category")
                dialog.geometry("400x150")
                dialog.configure(bg=self.colors["bg"])
                dialog.transient(self.root)
                dialog.grab_set()

                ttk.Label(dialog, text="Category Name:").pack(pady=10)

                name_entry = tk.Entry(dialog, font=("Segoe UI", 11), width=30)
                name_entry.insert(0, category_name)
                name_entry.pack(pady=5)
                name_entry.focus()
                name_entry.select_range(0, tk.END)

                def save_category():
                    name = name_entry.get().strip()
                    if name:
                        if name in self.categories:
                            result = messagebox.askyesno("Duplicate",
                                f"Category '{name}' already exists! Replace it?")
                            if not result:
                                return

                        self.categories[name] = words
                        self.update_category_list()
                        self.update_status()
                        self.status_label.config(text=f"Loaded category '{name}' with {len(words)} words")
                        dialog.destroy()
                    else:
                        messagebox.showwarning("Invalid", "Please enter a category name!")

                button_frame = tk.Frame(dialog, bg=self.colors["bg"])
                button_frame.pack(pady=15)

                ttk.Button(button_frame, text="Save", command=save_category,
                          style="Accent.TButton").pack(side=tk.LEFT, padx=5)
                ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

                name_entry.bind('<Return>', lambda e: save_category())

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def delete_category(self):
        """Delete selected categories"""
        selected_indices = self.category_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select categories to delete!")
            return

        selected_names = [self.category_listbox.get(i) for i in selected_indices]

        result = messagebox.askyesno("Confirm Delete",
            f"Delete {len(selected_names)} category(ies)?")

        if result:
            for name in selected_names:
                if name in self.categories:
                    del self.categories[name]
                if name in self.selected_categories:
                    self.selected_categories.remove(name)

            self.update_category_list()
            self.update_words_display()
            self.update_status()

    def on_category_select(self, event):
        """Handle category selection changes"""
        selected_indices = self.category_listbox.curselection()
        self.selected_categories = {self.category_listbox.get(i) for i in selected_indices}
        self.update_words_display()
        self.update_status()

    def update_category_list(self):
        """Update the category listbox"""
        self.category_listbox.delete(0, tk.END)
        for category in sorted(self.categories.keys()):
            self.category_listbox.insert(tk.END, category)

        # Restore selection
        for i, category in enumerate(sorted(self.categories.keys())):
            if category in self.selected_categories:
                self.category_listbox.selection_set(i)

    def update_words_display(self):
        """Update the words text widget with words from selected categories"""
        self.words_text.delete(1.0, tk.END)

        all_words = []

        # If only one category is selected, show just the words (editable)
        if len(self.selected_categories) == 1:
            category = list(self.selected_categories)[0]
            if category in self.categories:
                all_words = self.categories[category]
                self.words_text.insert(1.0, "\n".join(all_words))
        # If multiple categories selected, show words with category labels
        elif len(self.selected_categories) > 1:
            for category in sorted(self.selected_categories):
                if category in self.categories:
                    all_words.extend(self.categories[category])
            self.words_text.insert(1.0, "\n".join(all_words))

        self.words = all_words if all_words else []

    def update_words_from_text(self):
        """Update the active word list from the edited text and save back to categories"""
        try:
            # Stop flashing if currently running
            if self.is_running:
                self.stop_flashing()

            # Get text from the text widget
            text_content = self.words_text.get(1.0, tk.END)

            # Split by newlines and remove empty lines
            new_words = [line.strip() for line in text_content.split('\n') if line.strip()]

            # If we have selected categories, update them with the new words
            if self.selected_categories:
                # If only one category is selected, save all words to it
                if len(self.selected_categories) == 1:
                    category = list(self.selected_categories)[0]
                    self.categories[category] = new_words
                    self.status_label.config(text=f"Updated category '{category}' with {len(new_words)} words")
                else:
                    # Multiple categories selected - distribute words evenly or ask user
                    # For now, just update the active words without modifying categories
                    self.status_label.config(text=f"Updated {len(new_words)} active words (from multiple categories)")
            else:
                self.status_label.config(text=f"Updated {len(new_words)} active words (no category selected)")

            # Update the active word list
            self.words = new_words

            # Reset word index
            self.current_word_index = 0

            # Update status
            self.update_status()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update words: {str(e)}")

    def update_status(self):
        """Update the status labels"""
        total_cats = len(self.categories)
        selected_cats = len(self.selected_categories)
        total_words = len(self.words)

        self.category_count_label.config(
            text=f"Categories: {total_cats} | Selected: {selected_cats} | Words: {total_words}"
        )

    def start_flashing(self):
        """Start the flashing thread"""
        if not self.words:
            messagebox.showwarning("No Words", "Please select categories or add words first!")
            return

        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"Flashing {len(self.words)} words...")

        # Start flashing in a separate thread
        self.flash_thread = threading.Thread(target=self.flash_loop, daemon=True)
        self.flash_thread.start()

        # Minimize the main window
        self.root.iconify()

    def stop_flashing(self):
        """Stop the flashing"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Stopped")

        # Restore the main window
        self.root.deiconify()

    def flash_loop(self):
        """Main flashing loop"""
        pygame.init()

        # Get screen info
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        # Create fullscreen window
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        pygame.display.set_caption("Subliminal Flash")

        # Set a color key for transparency (magenta is commonly used)
        transparent_color = (255, 0, 255)

        # Make the window always on top and set layered window attributes for transparency (Windows)
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()["window"]

            # Windows API constants
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TOPMOST = 0x00000008
            WS_EX_TRANSPARENT = 0x00000020
            LWA_COLORKEY = 0x00000001
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_SHOWWINDOW = 0x0040

            # Get current extended style
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

            # Add layered, topmost, and transparent (click-through) styles
            new_ex_style = ex_style | WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_ex_style)

            # Set the transparent color key
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd,
                ctypes.c_ulong(transparent_color[2] << 16 | transparent_color[1] << 8 | transparent_color[0]),
                0, LWA_COLORKEY)

            # Set window to always on top
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                             SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        except:
            pass  # Fallback if we can't set transparency

        # Fill screen with transparent color initially
        screen.fill(transparent_color)
        pygame.display.flip()

        # Main loop
        while self.is_running:
            # Get current settings
            settings = {
                "flash_duration": self.flash_duration_var.get(),
                "interval": self.interval_var.get(),
                "font_size": self.font_size_var.get(),
                "text_color": self.text_color_var.get()
            }

            # Get next word
            if self.current_word_index >= len(self.words):
                self.current_word_index = 0

            word = self.words[self.current_word_index]
            self.current_word_index += 1

            # Flash the word
            self.flash_word(screen, screen_width, screen_height, word, settings, transparent_color)

            # Wait for interval
            start_time = time.time()
            while time.time() - start_time < settings["interval"] and self.is_running:
                time.sleep(0.1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                        break

        pygame.quit()

    def flash_word(self, screen, screen_width, screen_height, word, settings, transparent_color):
        """Flash a single word on screen"""
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
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def load_settings(self):
        """Load settings from file"""
        settings_file = Path("subliminal_settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    data = json.load(f)
                    self.settings = data.get("settings", self.settings)
                    self.categories = data.get("categories", {})

                    # Update UI with loaded settings
                    self.flash_duration_var.set(self.settings.get("flash_duration", 0.1))
                    self.interval_var.set(self.settings.get("interval", 5))
                    self.font_size_var.set(self.settings.get("font_size", 36))
                    self.text_color_var.set(self.settings.get("text_color", "#FFFFFF"))

                    # Update category list
                    self.update_category_list()
                    self.update_status()
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save settings to file"""
        self.settings = {
            "flash_duration": self.flash_duration_var.get(),
            "interval": self.interval_var.get(),
            "font_size": self.font_size_var.get(),
            "text_color": self.text_color_var.get()
        }

        data = {
            "settings": self.settings,
            "categories": self.categories
        }

        try:
            with open("subliminal_settings.json", 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

def main():
    root = tk.Tk()
    app = SubliminalApp(root)

    # Save settings on close
    def on_closing():
        if app.is_running:
            app.stop_flashing()
            time.sleep(0.5)
        app.save_settings()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
