from tkinter import *
from tkinter.ttk import Progressbar
import sys
import os

# Initialize the main windowq
root = Tk()
root.resizable(False, False)
image = PhotoImage(file='assets\\images\\logo.png')

# Set window size and position it in the center
height = 430
width = 530
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.overrideredirect(True)  # Remove title bar for a clean look
root.wm_attributes('-topmost', True)
root.config(background='#123768')

# Welcome label
welcome_label = Label(root, text='WELCOME TO YOUR FIN-TRACKER', bg='#123768', font=("yu gothic ui", 18, "bold"), fg='white')
welcome_label.place(x=70, y=25)

# Logo
bg_label = Label(root, image=image, bg='#123768')
bg_label.place(x=178, y=80)

# Progress label
progress_label = Label(root, text="Please Wait...", font=('yu gothic ui', 14, 'bold'), fg='white', bg='#123768')
progress_label.place(x=190, y=300)

# Progress bar
progress = Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
progress.place(x=15, y=350)

# Exit button
exit_btn = Button(root, text='x', bg='#123768', command=lambda: exit_window(), bd=0, font=("yu gothic ui", 16, "bold"),
                  activebackground='#fd6a36', fg='white')
exit_btn.place(x=490, y=0)

def exit_window():
    sys.exit(root.destroy())

# Function to hide the loading screen and open the next window
def top():
    root.withdraw()
    os.system("python app\\AccountSystem.py")
    root.destroy()

# Load function to simulate progress bar update
i = 0
def load():
    global i
    if i <= 10:
        txt = f'Please Wait...  {10 * i}%'
        progress_label.config(text=txt)
        progress['value'] = 10 * i
        i += 1
        progress_label.after(1000, load)  # Update progress every second
    else:
        top()  # Once completed, open the next window

# Start loading process
load()

# Run the Tkinter main loop
root.mainloop()
