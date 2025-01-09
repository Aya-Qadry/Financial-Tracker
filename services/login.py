from customtkinter import *
from PIL import Image
import json

# this will be replaced by things from db
credentials = {
    "user1@example.com": "password123",
    "user2@example.com": "mypassword",
}
with open("credentials.json", "w") as file:
    json.dump(credentials, file)

# Function to handle login
def handle_login():
    with open("credentials.json", "r") as file:
        data = json.load(file)

    email = email_entry.get()
    password = password_entry.get()

    if email in data and data[email] == password:
        display_feedback("Login Successful!", "You have successfully logged in.", success=True)
    else:
        display_feedback("Login Failed", "Incorrect email or password. Please try again.", success=False)

# Function to display feedback cards
# Function to display feedback cards
def display_feedback(title, message, success):
    feedback = CTkToplevel(app)
    feedback.geometry("300x150")
    feedback.overrideredirect(True)  # Remove title bar and borders
    feedback.configure(bg="white")  # Set white background for the entire frame

    # Center feedback over the main app
    x = app.winfo_x() + (app.winfo_width() - 300) // 2
    y = app.winfo_y() + (app.winfo_height() - 150) // 2
    feedback.geometry(f"300x150+{x}+{y}")

    # Card styling
    card_color = "#4CAF50" if success else "#F44336"
    feedback_frame = CTkFrame(feedback, fg_color="white", corner_radius=10)
    feedback_frame.pack(fill="both", expand=True, padx=10, pady=10)

    CTkLabel(
        master=feedback_frame,
        text=title,
        text_color="#ffffff",
        fg_color=card_color,
        font=("Arial Bold", 16),
        corner_radius=5
    ).pack(fill="x", pady=(10, 5), padx=10)
    
    CTkLabel(
        master=feedback_frame,
        text=message,
        text_color="#000000",
        bg_color="white",
        font=("Arial", 12)
    ).pack(pady=10)
    
    CTkButton(
        master=feedback_frame,
        text="OK",
        command=feedback.destroy,
        fg_color="#00509E",
        text_color="#ffffff"
    ).pack(pady=10)

app = CTk()
app.geometry("600x480")
app.resizable(0, 0)

# Image resources
side_img_data = Image.open("../assets/images/side-img.png")
email_icon_data = Image.open("../assets/images/email-icon.png")
password_icon_data = Image.open("../assets/images/password-icon.png")
google_icon_data = Image.open("../assets/images/google-icon.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(309, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(20, 20))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff", corner_radius=0)
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Welcome Back!", text_color="#100e84", anchor="w", justify="left", font=("Arial Bold", 24)).pack(
    anchor="w", pady=(50, 5), padx=(25, 0)
)
CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(
    anchor="w", padx=(25, 0)
)

CTkLabel(master=frame, text="  Email:", text_color="#100e84", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(
    anchor="w", pady=(38, 0), padx=(25, 0)
)
email_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#100e84", border_width=1, text_color="#000000")
email_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#100e84", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(
    anchor="w", pady=(21, 0), padx=(25, 0)
)
password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#100e84", border_width=1, text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

CTkButton(master=frame, text="Login", fg_color="#00509E", hover_color="#003F7F", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=handle_login).pack(
    anchor="w", pady=(40, 0), padx=(25, 0)
)
CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#100e84", width=225, image=google_icon).pack(
    anchor="w", pady=(20, 0), padx=(25, 0)
)

app.mainloop()
