from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
# from utils import ReceiptExtractor
from visualizations import Insights

app = CTk()
app.geometry("856x645")
app.resizable(0, 0)

set_appearance_mode("light")

sidebar_frame = CTkFrame(master=app, fg_color="#1E3A8A", width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

logo_img_data = Image.open("assets/images/logo.png")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

dashboard_img_data = Image.open("assets/images/analytics_icon.png")
dashboard_img = CTkImage(dark_image=dashboard_img_data, light_image=dashboard_img_data)

CTkButton(master=sidebar_frame, image=dashboard_img, text="Dashboard", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w").pack(anchor="center", ipady=5, pady=(60, 0))

transactions_img_data = Image.open("assets/images/package_icon.png")
transactions_img = CTkImage(dark_image=transactions_img_data, light_image=transactions_img_data)

main_view = CTkFrame(master=app, fg_color="#F3F4F6", width=680, height=650, corner_radius=0)

def show_insights():
    Insights(main_view)

add_expenseBtn = CTkButton(
    master=sidebar_frame, 
    text="Spending Insights", 
    font=("Arial Black", 14), 
    fg_color="transparent",
    image=transactions_img, 
    hover_color="#3B82F6", 
    anchor="w",
    command=show_insights
).pack(anchor="center", ipady=5, pady=(16, 0))


accounts_img_data = Image.open("assets/images/list_icon.png")
accounts_img = CTkImage(dark_image=accounts_img_data, light_image=accounts_img_data)
CTkButton(master=sidebar_frame, image=accounts_img, text="Accounts", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

investments_img_data = Image.open("assets/images/returns_icon.png")
investments_img = CTkImage(dark_image=investments_img_data, light_image=investments_img_data)
CTkButton(master=sidebar_frame, image=investments_img, text="Investments", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

settings_img_data = Image.open("assets/images/settings_icon.png")
settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))

profile_img_data = Image.open("assets/images/person_icon.png")
profile_img = CTkImage(dark_image=profile_img_data, light_image=profile_img_data)
CTkButton(master=sidebar_frame, image=profile_img, text="Profile", fg_color="transparent", font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w").pack(anchor="center", ipady=5, pady=(160, 0))

main_view.pack_propagate(0)
main_view.pack(side="left")

title_frame = CTkFrame(master=main_view, fg_color="transparent")
title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

CTkLabel(master=title_frame, text="Financial Tracker", font=("Arial Black", 25), text_color="#1E40AF").pack(anchor="nw", side="left")


# def show_receipt_extractor():
#     ReceiptExtractor(main_view)

add_expenseBtn = CTkButton(
    master=title_frame, 
    text="+ New Expense", 
    font=("Arial Black", 15), 
    text_color="#fff", 
    fg_color="#EF4444", 
    hover_color="#B91C1C",
    # command=show_receipt_extractor
).pack(anchor="ne", side="right")


metrics_frame = CTkFrame(master=main_view, fg_color="transparent")
metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

income_metric = CTkFrame(master=metrics_frame, fg_color="#10B981", width=200, height=60)
income_metric.grid_propagate(0)
income_metric.pack(side="left")

income_img_data = Image.open("assets/images/logistics_icon.png")
income_img = CTkImage(light_image=income_img_data, dark_image=income_img_data, size=(43, 43))

CTkLabel(master=income_metric, image=income_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

CTkLabel(master=income_metric, text="Income", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=income_metric, text="$10,000", text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


expenses_metric = CTkFrame(master=metrics_frame, fg_color="#EF4444", width=200, height=60)
expenses_metric.grid_propagate(0)
expenses_metric.pack(side="left", expand=True, anchor="center")

expenses_img_data = Image.open("assets/images/shipping_icon.png")
expenses_img = CTkImage(light_image=expenses_img_data, dark_image=expenses_img_data, size=(43, 43))

CTkLabel(master=expenses_metric, image=expenses_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

CTkLabel(master=expenses_metric, text="Expenses", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=expenses_metric, text="$5,500", text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

savings_metric = CTkFrame(master=metrics_frame, fg_color="#3B82F6", width=200, height=60)
savings_metric.grid_propagate(0)
savings_metric.pack(side="right",)

savings_img_data = Image.open("assets/images/delivered_icon.png")
savings_img = CTkImage(light_image=savings_img_data, dark_image=savings_img_data, size=(43, 43))

CTkLabel(master=savings_metric, image=savings_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

CTkLabel(master=savings_metric, text="Savings", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
CTkLabel(master=savings_metric, text="$4,500", text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

search_container = CTkFrame(master=main_view, height=50, fg_color="#F3F4F6")
search_container.pack(fill="x", pady=(45, 0), padx=27)

CTkEntry(master=search_container, width=305, placeholder_text="Search Transaction", border_color="#1E40AF", border_width=2).pack(side="left", padx=(13, 0), pady=15)

CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent", "Least Recent"], button_color="#1E40AF", border_color="#1E40AF", border_width=2, button_hover_color="#3B82F6", dropdown_hover_color="#3B82F6", dropdown_fg_color="#1E40AF", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

CTkComboBox(master=search_container, width=125, values=["Status", "Pending", "Completed", "Cancelled"], button_color="#1E40AF", border_color="#1E40AF", border_width=2, button_hover_color="#3B82F6", dropdown_hover_color="#3B82F6", dropdown_fg_color="#1E40AF", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

table_data = [
    ["Transaction ID", "Category", "Amount", "Date", "Status"],
    ['12345', 'Income', '$2,000', '2025-01-01', 'Completed'],
    ['67890', 'Expense', '$150', '2025-01-05', 'Completed'],
    ['11223', 'Income', '$1,500', '2025-01-10', 'Pending'],
    ['44556', 'Expense', '$200', '2025-01-15', 'Cancelled'],
    ['78901', 'Income', '$3,000', '2025-01-20', 'Completed'],
    ['23456', 'Expense', '$50', '2025-01-22', 'Pending']
]

table_frame = CTkScrollableFrame(master=main_view, fg_color="transparent")
table_frame.pack(expand=True, fill="both", padx=27, pady=21)
table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#F3F4F6"], header_color="#1E40AF", hover_color="#B4D8F7")
table.edit_row(0, text_color="#fff", hover_color="#3B82F6")
table.pack(expand=True)

app.mainloop()