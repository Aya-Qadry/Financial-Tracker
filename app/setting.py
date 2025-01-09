from customtkinter import *
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

# Settings Page
settings_frame = CTkFrame(master=main_view, fg_color="transparent")
settings_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

# Title without icon
CTkLabel(master=settings_frame, text="Settings", font=("Arial Black", 25), text_color="#1E40AF").pack(side="left", anchor="w")

# Change Username Section
username_frame = CTkFrame(master=main_view, fg_color="#E5E7EB", height=150)
username_frame.pack(fill="x", padx=27, pady=(20, 0))

# Larger Setting Icon above the username change inputs
setting_icon = Image.open("assets/images/setting.png")
setting_icon_img = CTkImage(dark_image=setting_icon, light_image=setting_icon, size=(80, 80))
CTkLabel(master=username_frame, text="", image=setting_icon_img).pack(pady=(10, 0))

CTkLabel(master=username_frame, text="Change Username", font=("Arial Bold", 18), text_color="#1E3A8A").pack(pady=(10, 5))

username_entry = CTkEntry(master=username_frame, placeholder_text="Enter New Username", width=400)
username_entry.pack(padx=10, pady=5)
CTkButton(master=username_frame, text="Save Username", fg_color="#3B82F6", command=lambda: print(f"Username changed to {username_entry.get()}")).pack(pady=10)

# Change Password Section
password_frame = CTkFrame(master=main_view, fg_color="#E5E7EB", height=200)
password_frame.pack(fill="x", padx=27, pady=(10, 0))

CTkLabel(master=password_frame, text="Change Password", font=("Arial Bold", 18), text_color="#1E3A8A").pack(pady=(10, 5))

# Old Password Entry
old_password_entry = CTkEntry(master=password_frame, placeholder_text="Enter Old Password", width=400, show="*")
old_password_entry.pack(padx=10, pady=5)

# New Password Entry
new_password_entry = CTkEntry(master=password_frame, placeholder_text="Enter New Password", width=400, show="*")
new_password_entry.pack(padx=10, pady=5)

# Confirm New Password Entry
confirm_password_entry = CTkEntry(master=password_frame, placeholder_text="Confirm New Password", width=400, show="*")
confirm_password_entry.pack(padx=10, pady=5)

# Save Password Button
CTkButton(master=password_frame, text="Save Password", fg_color="#3B82F6", command=lambda: print(f"Password changed to {new_password_entry.get()}")).pack(pady=10)

app.mainloop()
