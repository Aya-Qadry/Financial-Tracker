import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

class ModernFinanceDashboard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Financial Dashboard")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("light")
        
        # Initialize chart-related attributes
        self.fig = None
        self.ax = None
        self.canvas = None
        self.current_highlight = None
        self.chart_type = ctk.StringVar(value="bar")
        self.time_period = ctk.StringVar(value="Month")
        
        # Sample data for different time periods
        self.data_periods = {
            "Week": {
                "Mon": 1200, "Tue": 950, "Wed": 1100,
                "Thu": 1300, "Fri": 1450, "Sat": 900, "Sun": 800
            },
            "Month": {
                'Jan': 1200, 'Feb': 1150, 'Mar': 1400,
                'Apr': 1100, 'May': 1300, 'Jun': 1250,
                'Jul': 1500, 'Aug': 1350, 'Sep': 1200,
                'Oct': 1450, 'Nov': 1300, 'Dec': 1600
            },
            "Quarter": {
                "Q1": 3750, "Q2": 3650, "Q3": 4050, "Q4": 4350
            },
            "Year": {
                "2021": 42000, "2022": 45000, "2023": 48000, "2024": 51000
            }
        }
        
        self.monthly_expenses = self.data_periods["Month"]
        
        self.category_expenses = {
            'Housing': 35,
            'Food': 20,
            'Transportation': 15,
            'Entertainment': 10,
            'Utilities': 12,
            'Others': 8
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#F3F4F6")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create header
        header = ctk.CTkFrame(self.main_frame, fg_color="#1E3A8A", height=60)
        header.pack(fill="x", padx=10, pady=(10, 20))
        
        ctk.CTkLabel(
            header,
            text="Financial Analytics",
            font=("Arial Black", 24),
            text_color="#FFFFFF"
        ).pack(side="left", padx=20, pady=10)
        
        # Time period selector
        period_frame = ctk.CTkFrame(header, fg_color="transparent")
        period_frame.pack(side="right", padx=20)
        
        periods = ["Week", "Month", "Quarter", "Year"]
        for period in periods:
            ctk.CTkButton(
                period_frame,
                text=period,
                command=lambda p=period: self.change_period(p),
                fg_color="#3B82F6" if period == "Month" else "transparent",
                hover_color="#1E40AF",
                text_color="#FFFFFF",
                width=80,
                height=30
            ).pack(side="left", padx=5)
        
        # Create main content
        content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20)
        
        # Create two columns
        left_frame = ctk.CTkFrame(content, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = ctk.CTkFrame(content, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Add components
        self.create_stats_cards(left_frame)
        self.create_expense_chart(left_frame)
        self.create_pie_chart(right_frame)
        
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
        chart_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Chart controls
        controls_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            controls_frame,
            text="Expenses Overview",
            font=("Arial Black", 16),
            text_color="#1E3A8A"
        ).pack(side="left")
        
        # Chart type toggle
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
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 4), facecolor='#FFFFFF')
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
        chart_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        ctk.CTkLabel(
            chart_frame,
            text="Expense Categories",
            font=("Arial Black", 16),
            text_color="#1E3A8A"
        ).pack(padx=10, pady=10)
        
        fig = Figure(figsize=(6, 6), facecolor='#FFFFFF')
        ax = fig.add_subplot(111)
        
        values = list(self.category_expenses.values())
        labels = list(self.category_expenses.keys())
        colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#6366F1', '#8B5CF6']
        
        # Create the pie chart
        wedges, texts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct=None,
            textprops={'color': '#1E3A8A'},
            wedgeprops={'edgecolor': '#FFFFFF'}
        )
        
        # Add annotation object for hover percentage
        annotation = ax.annotate(
            '',
            xy=(0, 0),
            xytext=(0, 0),
            textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='#1E3A8A', alpha=0.8),
            color='white',
            fontsize=10
        )
        annotation.set_visible(False)
        
        def hover(event):
            if event.inaxes == ax:
                for i, wedge in enumerate(wedges):
                    if wedge.contains_point([event.x, event.y]):
                        # Highlight the hovered wedge
                        wedge.set_alpha(0.7)
                        for w in wedges:
                            if w != wedge:
                                w.set_alpha(1.0)
                        
                        # Display the percentage
                        percentage = f'{values[i]}%'
                        annotation.set_text(percentage)
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
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


    def change_period(self, period):
        self.time_period.set(period)
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
            self.bars = self.ax.bar(labels, values, color='#3B82F6')
        else:
            self.ax.plot(labels, values, color='#3B82F6', linewidth=2, marker='o')
        
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
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernFinanceDashboard()
    app.run()