import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from CTkTable import CTkTable
from customtkinter import CTkScrollableFrame

# from app.database import SupabaseDB   

import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.spendings import Spendings

class Insights:
    def __init__(self, main_view):
        self.main_view = main_view
        self.main_view.grid_propagate(False)
        self.main_view.pack_propagate(False)
        self.spendings_data = Spendings()

        self.fig = None
        self.ax = None
        self.canvas = None
        self.current_highlight = None
        self.chart_type = ctk.StringVar(value="bar")
        self.time_period = ctk.StringVar(value="Month")
        self.categories = ["Bank Transfers", "Entertainment", "Food & Drink", "Merchandise", "General Services",
                           "Government+Non-Profit", "Income", "Loans", "Medical", "Rent & Utilities", "Transportation", "Travel", "Other"]
        
        self.id = 4
        processed_data = self.spendings_data.process_data(self.id)

        self.data_periods = processed_data["data_periods"]  
        
        self.monthly_expenses = self.data_periods["Month"]
        
        self.category_expenses = processed_data["category_expenses"]
        
        self.setup_ui()

    def setup_ui(self):
        for widget in self.main_view.winfo_children():
            widget.destroy()
        self.main_frame = ctk.CTkFrame(self.main_view, fg_color="#F3F4F6")
        self.main_frame.pack(fill="both", expand=True)

        header = ctk.CTkFrame(self.main_frame, fg_color="#1E3A8A", height=60)
        header.pack(fill="x", padx=10, pady=(10, 20))
        
        ctk.CTkLabel(
            header,
            text="Financial Analytics",
            font=("Arial Black", 24),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20, pady=10)
        
        

        scrollable_content = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            height=600  
        )
        scrollable_content.pack(fill="both", expand=True, padx=20)

        stats_frame = ctk.CTkFrame(scrollable_content, fg_color="transparent", height=60)
        stats_frame.pack(pady=(10, 5), padx=20, fill="x")

        frames_container = ctk.CTkFrame(scrollable_content, fg_color="transparent")
        frames_container.pack(pady=(5, 10), padx=20, fill="x")

        top_frame = ctk.CTkFrame(frames_container, fg_color="transparent")
        top_frame.pack(side="top", fill="both", expand=True)
        bottom_frame = ctk.CTkFrame(frames_container, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="both", expand=True, pady=20)

        top_frame_left = ctk.CTkFrame(top_frame, fg_color="#F3F4F6")
        top_frame_left.pack(side="left", fill="both", expand=True, pady=(5, 10))

        top_frame_right = ctk.CTkFrame(top_frame, fg_color="transparent")
        top_frame_right.pack(side="left", fill="both", expand=True, padx=10)
        
        bottom_frame_top = ctk.CTkFrame(bottom_frame, fg_color="#133668")
        bottom_frame_top.pack(side="top", fill="both", expand=True, padx=10 , pady=20)
        
        bottom_frame_bottom = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        bottom_frame_bottom.pack(side="bottom", fill="both", expand=True, padx=10 , pady=20)

        period_frame = ctk.CTkFrame(bottom_frame_top, fg_color="transparent")
        period_frame.pack(side="right", padx=20)
        
        self.period_buttons = {}   
        periods = ["Week", "Month", "Quarter", "Year"]
        
        for period in periods:
            button = ctk.CTkButton(
                period_frame,
                text=period,
                command=lambda p=period: self.change_period(p),
                fg_color="#5dbd76" if period == "Month" else "transparent",
                hover_color="#f51a52",
                text_color="white",
                width=80,
                height=30
            )
            button.pack(side="left", padx=5, pady=10)
            self.period_buttons[period] = button   

        self.create_stats_cards(stats_frame)
        self.create_pie_chart(top_frame_left)
        self.create_categories(top_frame_right)
        self.create_expense_chart(bottom_frame_bottom)     
    
    def create_stats_cards(self, parent):
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("Total Income", "$10,000", "#10B981"),
            ("Total Expenses", "$5,500", "#EF4444"),
            ("Savings", "$4,500", "#3B82F6")
        ]
        
        for title, value, color in stats:
            card = self.create_animated_card(cards_frame, title, value, color)
            card.pack(side="left", fill="both", expand=True, padx=5)

    def create_animated_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=color)
        
        def on_enter(e):
            card.configure(fg_color=self.adjust_color(color, -20))
            value_label.configure(font=("Arial Black", 20))
            
        def on_leave(e):
            card.configure(fg_color=color)
            value_label.configure(font=("Arial Black", 18))
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial Black", 14),
            text_color="#FFFFFF"
        )
        title_label.pack(pady=(10, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial Black", 18),
            text_color="#FFFFFF"
        )
        value_label.pack(pady=(0, 10))
        
        return card
        
    def create_expense_chart(self, parent):
        chart_frame = ctk.CTkFrame(parent, fg_color="#F3F4F6")
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        controls_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            controls_frame,
            text="Expenses Overview",
            font=("Arial Black", 16),
            text_color="#1E3A8A"
        ).pack(side="left")
        
        ctk.CTkButton(
            controls_frame,
            text="Bar",
            command=lambda: self.update_chart_type("bar"),
            width=60,
            fg_color="#3B82F6",
            hover_color="#1E40AF"
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            controls_frame,
            text="Line",
            command=lambda: self.update_chart_type("line"),
            width=60,
            fg_color="#3B82F6",
            hover_color="#1E40AF"
        ).pack(side="right", padx=5)
        
        self.fig = Figure(figsize=(5, 3), facecolor='#F3F4F6')
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.draw()
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial plot
        self.update_expense_chart()
        
        # Setup interactions
        self.setup_chart_interactions()
        
    def create_pie_chart(self, parent):
        chart_frame = ctk.CTkFrame(parent, fg_color="#F3F4F6")
        chart_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            chart_frame,
            text="Expense Categories",
            font=("Arial Black", 16),
            text_color="#1E3A8A"
        ).pack(padx=10)

        fig = Figure(figsize=(3, 3), facecolor='#F3F4F6')
        ax = fig.add_subplot(111)

        values = list(self.category_expenses.values())
        labels = list(self.category_expenses.keys())
        total = sum(values)
        colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#6366F1', '#8B5CF6']

        # Create the pie chart
        wedges, _ = ax.pie(
            values,
            colors=colors,
            wedgeprops={'edgecolor': '#FFFFFF'}
        )

        ax.set_aspect('equal')   
        ax.set_xlim(-0.9, 0.9)   
        ax.set_ylim(-0.9, 0.9)

        annotation = ax.annotate(
            '',
            xy=(0, 0),
            xytext=(20, 20),
            textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#1E3A8A', alpha=0.8),
            color='white',
            fontsize=8
        )
        annotation.set_visible(False)

        def hover(event):
            if event.inaxes == ax:
                for i, wedge in enumerate(wedges):
                    if wedge.contains_point([event.x, event.y]):

                        wedge.set_alpha(0.7)
                        for w in wedges:
                            if w != wedge:
                                w.set_alpha(1.0)

                        #  percentage
                        percentage = (values[i] / total) * 100
                        category = labels[i]
                        annotation.set_text(f'{category}: {percentage:.1f}%')
                        annotation.xy = wedge.center
                        annotation.set_visible(True)
                        canvas.draw_idle()
                        return

                # Reset wedges if no hover
                for w in wedges:
                    w.set_alpha(1.0)
                annotation.set_visible(False)
                canvas.draw_idle()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.mpl_connect('motion_notify_event', hover)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def change_period(self, period):
        self.time_period.set(period)
        for p, button in self.period_buttons.items():
            button.configure(fg_color="#5dbd76" if p == period else "transparent")
    
        self.monthly_expenses = self.data_periods[period]
        self.update_expense_chart()
                
    def update_chart_type(self, chart_type):
        self.chart_type.set(chart_type)
        self.update_expense_chart()
        
    def update_expense_chart(self):
        self.ax.clear()
        
        labels = list(self.monthly_expenses.keys())
        values = list(self.monthly_expenses.values())
        
        if self.chart_type.get() == "bar":
            self.bars = self.ax.bar(labels, values, color='#fa2643')
        else:
            self.ax.plot(labels, values, color='#fa2643', linewidth=2, marker='o')
        
        self.ax.set_facecolor('#FFFFFF')
        self.ax.tick_params(colors='#1E3A8A')
        
        for spine in self.ax.spines.values():
            spine.set_color('#1E3A8A')
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        # Rotate x-axis labels if needed
        if len(labels) > 7:
            plt.xticks(rotation=45)
        
        self.canvas.draw()
        
    def setup_chart_interactions(self):
        def on_hover(event):
            if event.inaxes == self.ax and hasattr(self, 'bars'):
                for i, bar in enumerate(self.bars):
                    if bar.contains(event)[0]:
                        self.highlight_bar(i)
                        return
                        
        self.canvas.mpl_connect('motion_notify_event', on_hover)
        
    def highlight_bar(self, index):
        if self.current_highlight is not None:
            self.bars[self.current_highlight].set_color('#3B82F6')
            
        self.bars[index].set_color('#1E40AF')
        self.current_highlight = index
        self.canvas.draw_idle()
        
    def adjust_color(self, hex_color, factor):
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        new_rgb = tuple(max(0, min(255, c + factor)) for c in rgb)
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"
      

    def create_categories(self, parent_frame):
        container = ctk.CTkFrame(master=parent_frame, fg_color="transparent")
        container.pack(expand=True, fill="both")

        ctk.CTkLabel(
            container,
            text="Monthly Spendings",
            font=("Arial Black", 16),
            text_color="#1E3A8A"
        ).pack(padx=10, pady=5, fill="both", side="top")

        table_frame = ctk.CTkScrollableFrame(master=container, fg_color="transparent")
        table_frame.pack(expand=True, side="bottom", fill="both")


        table_data = self.spendings_data.get_monthly_category_spending(self.id )

        table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#F3F4F6"], header_color="#1E40AF", hover_color="#B4D8F7")
        table.edit_row(0, text_color="#fff", hover_color="#3B82F6")
        table.pack(expand=True)

    def run(self , frame):
        self.main_view.mainloop()
