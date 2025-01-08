import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # For resizing icons

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction Categorizer")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.dark_mode = False

        # Set styles
        self.style = ttk.Style()
        self.style.theme_use("arc")
        self.setup_styles()

        # Layout structure
        self.create_header()
        self.create_sidebar()
        self.create_main_area()
        self.create_status_bar()

    def setup_styles(self):
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 12))
        self.style.configure(
            "TButton",
            background="#ffffff",
            foreground="#ffffff",
            font=("Helvetica", 10),
           # padding=5,
        )
        self.style.map("TButton", background=[("active", "#005a9e")])
        self.style.configure("Header.TFrame", background="#0078d7")
        self.style.configure(
            "Header.TLabel", background="#0078d7", foreground="#ffffff"
        )
        self.style.configure("Sidebar.TFrame", background="#ffffff")
        self.style.configure(
            "Sidebar.TLabel", background="#ffffff", foreground="#000000"
        )
        self.style.configure("Card.TFrame", background="#ffffff", relief="raised", borderwidth=2)
        self.style.configure("Card.TLabel", background="#ffffff")

    def create_header(self):
        header = ttk.Frame(self.root, style="Header.TFrame")
        header.pack(side="top", fill="x", pady=10)
        ttk.Label(
            header,
            text="Transaction Categorizer",
            font=("Helvetica", 18, "bold"),
            style="Header.TLabel",
        ).pack(side="left", padx=10)

    def create_sidebar(self):
        self.sidebar = ttk.Frame(self.root, width=200, style="Sidebar.TFrame")
        self.sidebar.pack(side="left", fill="y")

        # Load icons
        self.home_icon = self.load_icon("assets/icons/home.png", (30, 30))
        self.upload_icon = self.load_icon("assets/icons/upload.png", (30, 30))
        self.visualize_icon = self.load_icon("assets/icons/visualize.png", (30, 30))
        self.exit_icon = self.load_icon("assets/icons/exit.png", (30, 30))

        # Sidebar title
        ttk.Label(
            self.sidebar, text="Menu", font=("Helvetica", 14, "bold")
        ).pack(pady=20)

        # Create sidebar buttons
        self.create_sidebar_button("Home", self.home_icon, self.show_home)
        self.create_sidebar_button("Upload CSV", self.upload_icon, self.upload_csv)
        self.create_sidebar_button("Visualize", self.visualize_icon, self.visualize)
        self.create_sidebar_button("Exit", self.exit_icon, self.root.quit)

    def load_icon(self, path, size):
        """Load and resize an icon."""
        try:
            img = Image.open(path).resize(size, Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading icon {path}: {e}")
            return None

    def create_sidebar_button(self, text, icon, command):
        """Create a sidebar button with centered icon and text."""
        button = ttk.Button(
            self.sidebar, text=text, image=icon, compound="top", command=command
        )
        button.pack(fill="x", pady=10, padx=10, ipadx=5, ipady=5)

    def create_main_area(self):
        self.main_area = ttk.Frame(self.root, style="Main.TFrame")
        self.main_area.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Card for home content
        self.home_card = ttk.Frame(self.main_area, style="Card.TFrame")
        self.home_card.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(
            self.home_card,
            text="Welcome to Transaction Categorizer!",
            font=("Helvetica", 16),
            style="Card.TLabel",
        ).pack(pady=20)

    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side="bottom", fill="x")

        self.status_label = ttk.Label(self.status_bar, text="Ready", anchor="w")
        self.status_label.pack(side="left", padx=10)

    def show_home(self):
        print("Home button clicked!")
        self.clear_main_area()
        ttk.Label(self.main_area, text="Home Screen", font=("Helvetica", 16)).pack(
            pady=20
        )

    def upload_csv(self):
        print("Upload CSV button clicked!")
        self.clear_main_area()
        ttk.Label(self.main_area, text="Upload CSV Screen", font=("Helvetica", 16)).pack(
            pady=20
        )

    def visualize(self):
        print("Visualize button clicked!")
        self.clear_main_area()
        ttk.Label(self.main_area, text="Visualize Screen", font=("Helvetica", 16)).pack(
            pady=20
        )

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = GUI(root)
    root.mainloop()
