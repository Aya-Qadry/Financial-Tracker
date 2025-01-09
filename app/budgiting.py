from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

app = CTk()
app.geometry("856x645")
app.resizable(0, 0)

set_appearance_mode("light")

# Sidebar
sidebar_frame = CTkFrame(master=app, fg_color="#1E3A8A", width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

logo_img_data = Image.open("assets/images/logo.png")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

# Sidebar Buttons
buttons_info = [
    ("Dashboard", "assets/images/analytics_icon.png"),
    ("Transactions", "assets/images/package_icon.png"),
    ("Accounts", "assets/images/list_icon.png"),
    ("Investments", "assets/images/returns_icon.png"),
    ("Settings", "assets/images/settings_icon.png"),
    ("Profile", "assets/images/person_icon.png"),
]
for i, (text, img_path) in enumerate(buttons_info):
    img_data = Image.open(img_path)
    img = CTkImage(dark_image=img_data, light_image=img_data)
    CTkButton(
        master=sidebar_frame, image=img, text=text, fg_color="transparent",
        font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w"
    ).pack(anchor="center", ipady=5, pady=(60 if i == 0 else 16, 0))

# Main View
main_view = CTkFrame(master=app, fg_color="#F3F4F6", width=680, height=650, corner_radius=0)
main_view.pack_propagate(0)
main_view.pack(side="left")

title_frame = CTkFrame(master=main_view, fg_color="transparent")
title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
CTkLabel(master=title_frame, text="Budgeting Overview", font=("Arial Black", 25), text_color="#1E40AF").pack(anchor="nw", side="left")

# Insights Section
insights_frame = CTkFrame(master=main_view, fg_color="#E5E7EB", height=100)
insights_frame.pack(fill="x", padx=27, pady=(10, 0))

insights = [
    ("Total Budget", "$4,300", "#1E3A8A", "assets/images/totbudget.png"),
    ("Total Spent", "$3,800", "#EF4444", "assets/images/totspent.png"),
    ("Remaining Budget", "$500", "#10B981", "assets/images/remainigng.png"),
    ("Largest Spending", "Housing", "#F59E0B", "assets/images/largest.png"),
]

for i, (label, value, color, icon_path) in enumerate(insights):
    insight_frame = CTkFrame(master=insights_frame, fg_color="transparent")
    insight_frame.pack(side="left", expand=True, padx=10, pady=10)
    
    icon_img_data = Image.open(icon_path)
    icon_img = CTkImage(dark_image=icon_img_data, light_image=icon_img_data, size=(30, 30))
    CTkLabel(master=insight_frame, text="", image=icon_img).pack(anchor="center")
    
    CTkLabel(master=insight_frame, text=label, font=("Arial", 12), text_color="#374151").pack(anchor="center")
    CTkLabel(master=insight_frame, text=value, font=("Arial Bold", 16), text_color=color).pack(anchor="center")

# Pie Chart Simulation (Budget Percentages)
budget_frame = CTkFrame(master=main_view, fg_color="#E5E7EB", height=200)
budget_frame.pack(fill="x", padx=27, pady=(10, 0))

CTkLabel(master=budget_frame, text="Budget Breakdown", font=("Arial Bold", 18), text_color="#1E3A8A").pack(pady=(10, 5))
categories = [("Housing", 30), ("Food", 20), ("Transportation", 15), ("Savings", 25), ("Entertainment", 10)]
for i, (category, percentage) in enumerate(categories):
    # Define colors based on category
    progress_color = "#1E3A8A"  # Default blue color
    if category == "Savings":
        progress_color = "#10B981"  # Green for savings
    elif category == "Food":
        progress_color = "#EF4444"  # Red for food overspending

    progress = CTkProgressBar(master=budget_frame, progress_color=progress_color, width=400)
    progress.set(percentage / 100)
    CTkLabel(master=budget_frame, text=f"{category} - {percentage}%", font=("Arial", 12), text_color="#1E3A8A").pack(pady=2)
    progress.pack(pady=(5, 10) if i == len(categories) - 1 else 5)  # Add extra space after the last item

# Table for Budget Details
table_data = [
    ["Category", "Planned Budget", "Actual Spent", "Remaining"],
    ["Housing", "$1,500", "$1,200", "$300"],
    ["Food", "$800", "$700", "$100"],
    ["Transportation", "$600", "$550", "$50"],
    ["Savings", "$1,000", "$1,000", "$0"],
    ["Entertainment", "$400", "$350", "$50"],
]

table_frame = CTkScrollableFrame(master=main_view, fg_color="transparent")
table_frame.pack(expand=True, fill="both", padx=27, pady=21)
table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#F3F4F6"], header_color="#1E40AF", hover_color="#B4D8F7")
table.edit_row(0, text_color="#fff", hover_color="#3B82F6")
table.pack(expand=True)

# Interactive Adjustments Section
adjustments_frame = CTkFrame(master=main_view, fg_color="#E5E7EB", height=150)
adjustments_frame.pack(fill="x", padx=27, pady=(10, 0))

CTkLabel(master=adjustments_frame, text="Adjust Budget", font=("Arial Bold", 18), text_color="#1E3A8A").pack(pady=(10, 5))
for category in ["Housing", "Food", "Transportation", "Savings", "Entertainment"]:
    adjustment_label = CTkLabel(master=adjustments_frame, text=f"{category}:", font=("Arial", 12), text_color="#1E3A8A")
    adjustment_label.pack(side="left", padx=5, pady=5)
    adjustment_slider = CTkSlider(master=adjustments_frame, from_=0, to=100, number_of_steps=100)
    adjustment_slider.pack(side="left", padx=5, pady=5)

app.mainloop()
