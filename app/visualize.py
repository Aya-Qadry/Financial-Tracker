from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, set_appearance_mode
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
from database import SupabaseDB
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

class ModernSpendingDashboard:
    def __init__(self, user_id):
        self.client = SupabaseDB()
        self.user_id = user_id
        
        # Initialize App Window
        self.app = CTk()
        self.app.geometry("1200x800")
        self.app.resizable(False, False)
        set_appearance_mode("light")

        # Colors and Style
        self.colors = {
            "primary": "#4F46E5",
            "hover": "#3B82F6",
            "background": "#F8FAFC",
            "surface": "#FFFFFF",
            "text": "#334155",
        }
        
        # Fetch Data
        self.fetch_data()

        # Build Layout
        self.create_sidebar()
        self.create_main_layout()
        
    def create_sidebar(self):
        sidebar_frame = CTkFrame(master=self.app, fg_color="#1E3A8A", width=176, corner_radius=0)
        sidebar_frame.pack_propagate(False)
        sidebar_frame.pack(fill="y", side="left")
        
        # Add Logo
        logo_img_data = Image.open("assets/images/logo.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(78, 85))
        CTkLabel(master=sidebar_frame, image=logo_img, text="").pack(pady=(38, 0))

        # Sidebar Buttons
        self.add_sidebar_button(sidebar_frame, "Dashboard", "assets/images/analytics_icon.png")
        self.add_sidebar_button(sidebar_frame, "Transactions", "assets/images/package_icon.png")
        self.add_sidebar_button(sidebar_frame, "Accounts", "assets/images/list_icon.png")
        self.add_sidebar_button(sidebar_frame, "Investments", "assets/images/returns_icon.png")

    def add_sidebar_button(self, parent, text, image_path):
        img_data = Image.open(image_path)
        img = CTkImage(dark_image=img_data, light_image=img_data)
        CTkButton(
            master=parent,
            image=img,
            text=text,
            fg_color="transparent",
            font=("Arial Bold", 14),
            hover_color=self.colors["hover"],
            anchor="w",
        ).pack(anchor="center", pady=16, ipady=5)

    def create_main_layout(self):
        main_frame = CTkFrame(master=self.app, fg_color=self.colors["background"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top Controls
        self.create_controls(main_frame)

        # Chart Area
        self.chart_container = CTkFrame(master=main_frame, fg_color=self.colors["surface"], corner_radius=12)
        self.chart_container.pack(fill="both", expand=True, pady=(15, 0))
        self.create_charts()

    def create_controls(self, parent):
        controls_frame = CTkFrame(master=parent, fg_color=self.colors["surface"], corner_radius=12)
        controls_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        # Time Period Options
        periods = ["Last Month", "Last 3 Months", "Last 6 Months", "Last Year"]
        self.period_var = tk.StringVar(value=periods[0])
        for period in periods:
            CTkButton(
                master=controls_frame,
                text=period,
                command=self.update_charts,
                fg_color=self.colors["primary"],
                hover_color=self.colors["hover"],
                height=36,
                corner_radius=8,
            ).pack(side="left", padx=10, pady=10)

    def create_charts(self):
        if self.df.empty:
            CTkLabel(
                master=self.chart_container,
                text="No spending data available",
                text_color=self.colors["text"],
            ).pack(expand=True)
            return
        
        # Clear old charts
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        # Matplotlib Figure
        fig = Figure(figsize=(10, 6), facecolor=self.colors["background"])
        
        # Subplots
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        # Example Charts
        self.create_pie_chart(ax1)
        self.create_line_chart(ax2)
        
        # Embed Chart
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def create_pie_chart(self, ax):
        categories = self.df.groupby('category')['total_amount'].sum()
        ax.pie(
            categories,
            labels=categories.index,
            autopct='%1.1f%%',
            colors=plt.cm.Pastel1(np.linspace(0, 1, len(categories))),
        )
        ax.set_title("Spending by Category", color=self.colors["text"])

    def create_line_chart(self, ax):
        monthly = self.df.groupby(pd.Grouper(key='receipt_date', freq='M'))['total_amount'].sum()
        ax.plot(monthly.index, monthly.values, color=self.colors["primary"], linewidth=2)
        ax.set_title("Monthly Spending Trend", color=self.colors["text"])
        ax.grid(True, alpha=0.3)

    def fetch_data(self):
        response = self.client.get_user_receipts(self.user_id)
        self.df = pd.DataFrame(response.data)
        self.df['receipt_date'] = pd.to_datetime(self.df['receipt_date'])
        self.df['total_amount'] = pd.to_numeric(self.df['total_amount'], errors='coerce')
        
    def update_charts(self):
        self.create_charts()

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    USER_ID = 4
    app = ModernSpendingDashboard(USER_ID)
    app.run()
