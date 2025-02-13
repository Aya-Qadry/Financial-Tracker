# main.py
import importlib
import time
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

import gui

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, root):
        self.root = root

    def on_modified(self, event):
        if event.src_path.endswith("gui.py"):
            print("Reloading GUI module...")
            self.root.destroy()  # Close the current window
            importlib.reload(gui)  # Reload the module
            root = ThemedTk(theme="arc")  # Recreate the root window
            gui.GUI(root)  # Reinitialize the GUI
            root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":

    data = {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA"
        },
        "hobbies": ["reading", "hiking", "coding"]
    }

    json_str_none = json.dumps(data, indent=None) 
    json_str_1 = json.dumps(data, indent=1)
    json_str_2 = json.dumps(data, indent=2) 
    print("indent=None:\n", json_str_none, "\n")
    print("indent=1:\n", json_str_1, "\n")
    print("indent=2:\n", json_str_2, "\n")
    
    # root = ThemedTk(theme="arc")
    # gui.GUI(root)

    # # Set up file watcher
    # event_handler = ReloadHandler(root)
    # observer = Observer()
    # observer.schedule(event_handler, path=".", recursive=False)
    # observer.start()

    # # Start the Tkinter event loop
    # root.mainloop()

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()