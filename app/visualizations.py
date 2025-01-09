import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import PhotoImage
from PIL import Image, ImageTk

from app.database import SupabaseDB   

class Insights:

    def __init__(self, main_view):
        self.db_conn = SupabaseDB()
        self.main_view = main_view
        self.receipts = []
        self.create_widgets()
    
    def create_widgets(self):
        self.main_view.grid_propagate(False)
        self.main_view.pack_propagate(False)
        
        for widget in self.main_view.winfo_children():
            widget.destroy()
