from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

app = CTk()
app.geometry("856x645")
app.resizable(0, 0)

set_appearance_mode("light")

# Sidebar Frame
sidebar_frame = CTkFrame(master=app, fg_color="#1E3A8A", width=176, height=650, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

logo_img_data = Image.open("assets/images/logo.png")
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

# Sidebar Buttons
buttons = [
    ("Dashboard", "assets/images/analytics_icon.png"),
    ("Transactions", "assets/images/package_icon.png"),
    ("Accounts", "assets/images/list_icon.png"),
    ("Investments", "assets/images/returns_icon.png"),
    ("Settings", "assets/images/settings_icon.png"),
    ("Profile", "assets/images/person_icon.png")
]

for button in buttons:
    img_data = Image.open(button[1])
    img = CTkImage(dark_image=img_data, light_image=img_data)
    CTkButton(master=sidebar_frame, image=img, text=button[0], fg_color="transparent", font=("Arial Bold", 14), hover_color="#3B82F6", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0) if button[0] != "Profile" else (160, 0))

# Main View
main_view = CTkFrame(master=app, fg_color="#F3F4F6", width=680, height=650, corner_radius=0)
main_view.pack_propagate(0)
main_view.pack(side="left")

# Profile Section Header
title_frame = CTkFrame(master=main_view, fg_color="transparent")
title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

CTkLabel(master=title_frame, text="Your Profile", font=("Arial Black", 25), text_color="#1E40AF").pack(anchor="nw", side="left")

# Profile Section
profile_frame = CTkFrame(master=main_view, fg_color="transparent")
profile_frame.pack(pady=(20, 0), padx=27, fill="x")

# Profile Picture
# Profile Picture
profile_img_data = Image.open("assets/images/avatar.png")  # Path for the profile picture
profile_img = CTkImage(dark_image=profile_img_data, light_image=profile_img_data, size=(100, 100))

# Explicitly set the text parameter to an empty string
profile_picture_label = CTkLabel(master=profile_frame, image=profile_img, text="")
profile_picture_label.pack(pady=10, anchor="center")  
# Profile Details with Background Color and Rounded Corners
client_name = "John Doe"
client_email = "johndoe@example.com"
client_balance = "$15,000"
client_phone = "+1 (123) 456-7890"
client_address = "1234 Elm Street, Springfield, IL"

# Custom styled labels (smaller and adjusted)
name_label = CTkLabel(master=profile_frame, text=f"Name: {client_name}", font=("Arial", 14), width=350, height=30, corner_radius=8, fg_color="#4CAF50", text_color="white", anchor="center")
name_label.pack(anchor="center", pady=5, padx=10)

email_label = CTkLabel(master=profile_frame, text=f"Email: {client_email}", font=("Arial", 14), width=350, height=30, corner_radius=8, fg_color="#2196F3", text_color="white", anchor="center")
email_label.pack(anchor="center", pady=5, padx=10)

# Balance, Phone, and Address (more subtle colors)
CTkLabel(master=profile_frame, text=f"Balance: {client_balance}", font=("Arial", 14), width=350, height=30, corner_radius=8, fg_color="#E0E0E0", text_color="#333", anchor="center").pack(anchor="center", pady=5, padx=10)
CTkLabel(master=profile_frame, text=f"Phone: {client_phone}", font=("Arial", 14), width=350, height=30, corner_radius=8, fg_color="#E0E0E0", text_color="#333", anchor="center").pack(anchor="center", pady=5, padx=10)
CTkLabel(master=profile_frame, text=f"Address: {client_address}", font=("Arial", 14), width=350, height=30, corner_radius=8, fg_color="#E0E0E0", text_color="#333", anchor="center").pack(anchor="center", pady=5, padx=10)

# Recent Transactions
recent_transactions_title = CTkLabel(master=profile_frame, text="Recent Transactions", font=("Arial Black", 18), text_color="#1E40AF")
recent_transactions_title.pack(anchor="w", pady=(20, 10))

# Sample Transactions Data
transactions_data = [
    ['01/05/2025', 'Income', '$2,000', 'Completed'],
    ['10/05/2025', 'Expense', '$150', 'Completed'],
    ['15/05/2025', 'Income', '$1,500', 'Pending'],
]

# Transaction Table
table_frame = CTkScrollableFrame(master=profile_frame, fg_color="transparent")
table_frame.pack(expand=True, fill="both", padx=27, pady=10)

table_columns = ["Date", "Category", "Amount", "Status"]

# Change the colors and hover_color to green shades
table = CTkTable(
    master=table_frame, 
    values=[table_columns] + transactions_data, 
    colors=["#D4E8D4", "#C6F1C6"],  # Light green shades for rows
    header_color="#4CAF50",  # Green header
    hover_color="#A8DDA8"  # Lighter green on hover
)

table.edit_row(0, text_color="#fff", hover_color="#7BC674")  # Adjust hover_color if needed
table.pack(expand=True)

app.mainloop()
