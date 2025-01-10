from customtkinter import *
from CTkTable import CTkTable
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime
import re
import pytesseract
from tests import parser, categorize
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.receipt import Receipt
from app.database import SupabaseDB

class ReceiptExtractor:
    def __init__(self, main_view):
        self.db_conn = SupabaseDB()
        self.main_view = main_view
        self.receipts = []
        # self.load_receipts()
        self.create_widgets()

    
    def setup_table(self, user_id: int):
        # Clear any existing table
        if hasattr(self, 'receipt_frame'):
            self.receipt_frame.destroy()
        
        self.main_view.update_idletasks()

        self.receipt_frame = CTkFrame(self.main_view, fg_color="transparent")
        self.receipt_frame.pack(fill="both", expand=True, padx=20, pady=15)  # Increased padding

        # Create scrollable frame
        self.table_scroll = CTkScrollbar(self.receipt_frame, button_color="#6366F1", button_hover_color="#4F46E5")
        self.table_scroll.pack(side="right", fill="y")

        # Create canvas with softer background
        self.canvas = tk.Canvas(self.receipt_frame, bg="#F8FAFC", highlightthickness=0)  # Lighter, modern background
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        self.table_scroll.configure(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.table_scroll.set)

        # Create inner frame for table
        self.inner_frame = CTkFrame(self.canvas, fg_color="transparent")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Create table with enhanced colors
        self.table = CTkTable(
            master=self.inner_frame,
            values=[["Date", "Store", "Amount", "Category"]],
            colors=["#FFFFFF", "#F1F5F9"],  # Subtle alternating colors
            header_color="#4F46E5",  # Modern indigo
            hover_color="#EEF2FF",  # Light indigo hover
            width=100
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure canvas scrolling
        def configure_scroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.canvas.itemconfig(self.canvas_frame, width=event.width)

        self.inner_frame.bind("<Configure>", configure_scroll)
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(
            self.canvas_frame, width=e.width))

        # Populate data
        self.populate_initial_receipts(user_id)

    def create_widgets(self):
        self.main_view.grid_propagate(False)
        self.main_view.pack_propagate(False)
        
        for widget in self.main_view.winfo_children():
            widget.destroy()

        # Button frame with modern styling
        self.button_frame = CTkFrame(self.main_view, fg_color="transparent")
        self.button_frame.pack(pady=20)  # Increased padding
        
        button_style = {
            "fg_color": "#4F46E5",  # Modern indigo
            "hover_color": "#4338CA",  # Darker indigo on hover
            "corner_radius": 8,
            "border_width": 0,
            "text_color": "#FFFFFF",
            "height": 36  # Taller buttons
        }
        
        CTkButton(self.button_frame, text="Upload Receipt Image", 
                command=self.upload_image, **button_style).grid(row=0, column=0, padx=8)
        CTkButton(self.button_frame, text="Manual Entry", 
                command=self.show_manual_entry, **button_style).grid(row=0, column=1, padx=8)
        CTkButton(self.button_frame, text="View All Receipts", 
                command=self.show_all_receipts, **button_style).grid(row=0, column=2, padx=8)
        
        # Entry and preview container with enhanced spacing
        self.entry_preview_container = CTkFrame(self.main_view, fg_color="transparent")
        self.entry_preview_container.pack(pady=20, fill="x", padx=20)

        self.entry_frame = CTkFrame(self.entry_preview_container, fg_color="#FFFFFF", corner_radius=12)
        self.entry_frame.grid(row=0, column=0, padx=(0,15), sticky="nsew")
        
        labels = ["Store Name:", "Date:", "Total Amount:", "Category:"]
        self.entries = {}

        # Enhanced entry styling
        entry_style = {
            "fg_color": "#F8FAFC",  # Light gray background
            "border_color": "#E2E8F0",  # Subtle border
            "corner_radius": 6,
            "height": 32
        }

        for i, label in enumerate(labels):
            CTkLabel(self.entry_frame, text=label, text_color="#334155").grid(row=i, column=0, pady=8, padx=12, sticky="w")
            if label == "Category:":
                self.entries[label] = CTkComboBox(
                    self.entry_frame,
                    values=["Bank Transfers", "Entertainment", "Food & Drink", 
                        "General Merchandise", "General Services", "Government + Non-Profit", 
                        "Income", "Loans", "Medical", "Rent & Utilities", "Transportation", 
                        "Travel", "Other"],
                    fg_color="#F8FAFC",
                    button_color="#4F46E5",
                    button_hover_color="#4338CA",
                    border_color="#E2E8F0",
                    dropdown_hover_color="#EEF2FF",
                    corner_radius=6,
                    height=32
                )
                self.entries[label].grid(row=i, column=1, pady=8, padx=12, sticky="ew")
            else:
                self.entries[label] = CTkEntry(self.entry_frame, **entry_style)
                if label == "Date:":
                    self.entries[label].insert(0, datetime.now().strftime("%Y-%m-%d"))
                self.entries[label].grid(row=i, column=1, pady=8, padx=12, sticky="ew")
        
        # Preview frame with enhanced styling
        self.preview_frame = CTkFrame(self.entry_preview_container, fg_color="#FFFFFF", corner_radius=12)
        self.preview_frame.grid(row=0, column=1, sticky="nsew")
        self.preview_text = CTkTextbox(self.preview_frame, fg_color="#F8FAFC", corner_radius=6)
        self.preview_text.pack(fill="both", expand=True, padx=12, pady=12)

        self.entry_preview_container.grid_columnconfigure(0, weight=1)
        self.entry_preview_container.grid_columnconfigure(1, weight=1)
        self.entry_preview_container.grid_rowconfigure(0, weight=1)

        # Save button with enhanced styling
        CTkButton(self.entry_frame, text="Save Receipt", 
                command=self.save_receipt,
                fg_color="#4F46E5",
                hover_color="#4338CA",
                corner_radius=8,
                height=36).grid(row=len(labels), column=0, columnspan=2, pady=15, padx=12)
        
        self.setup_table(4)
        self.update_receipt_list()
       
    
    def populate_initial_receipts(self, user_id: int):
        try:
            response = self.db_conn.get_user_receipts(user_id)
            
            if response.data:
                self.receipts = response.data
                table_values = [["Date", "Store", "Amount", "Category"]]
                
                for receipt in self.receipts:
                    formatted_amount = f"{receipt['total_amount']:.2f} {receipt['currency']}"
                    table_values.append([
                        str(receipt["receipt_date"]),
                        str(receipt["store_name"]),
                        formatted_amount,
                        str(receipt["category"])
                    ])
                
                # Update table with new values
                self.table.configure(values=table_values)
                self.table.edit_row(0, text_color="#fff", hover_color="#3B82F6")
            else:
                self.receipts = []
                self.table.configure(values=[["Date", "Store", "Amount", "Category"]])
                
        except Exception as e:
            print(f"Error populating receipts: {e}")
            
    
    def extract_receipt_info(self, text):
        self.preview_text.delete("1.0", "end")
        print(text)
        receipt_processor = parser.ReceiptProcessor("AIzaSyDJuXkjSgz3w1Ov32Kmb59dB5_bwXewZGg")

        store_name = ""
        total_amount = ""
        date = ""
        
        lines = text.split('\n')
        
        # Regular expressions for matching
        amount_pattern = r'\d+\.\d{2}'
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        
        # Usually the store name is at the top of the receipt
        for line in lines[:3]:
            if line.strip() and not any(char.isdigit() for char in line):
                store_name = line.strip()
                break
        
        for line in lines:
            line = line.upper()
            if "TOTAL" in line or "AMOUNT" in line or "DUE" in line or "BALANCE" in line:
                amounts = re.findall(amount_pattern, line)
                if amounts:
                    total_amount = amounts[-1]
        
        for line in lines:
            date_match = re.search(date_pattern, line)
            if date_match:
                date = date_match.group()
                try:
                    parsed_date = datetime.strptime(date, "%m/%d/%Y")
                    date = parsed_date.strftime("%Y-%m-%d")
                except:
                    try:
                        parsed_date = datetime.strptime(date, "%m/%d/%y")
                        date = parsed_date.strftime("%Y-%m-%d")
                    except:
                        date = datetime.now().strftime("%Y-%m-%d")
        
        added_text = f"with a total of {total_amount}"        
        result = receipt_processor.process_receipt(text + added_text)
        new_text = receipt_processor.format_receipt(result)
        new_text = new_text.strip()
        self.preview_text.insert("end", new_text)
        print(f"in the function {store_name}")
        return {
            "store": store_name.split()[0],
            "amount": total_amount,
            "date": date,
            "data": new_text
        }


    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                receipt_info = self.extract_receipt_info(text)
                
                category = categorize.categorize_exepense(receipt_info["data"])
                #print(f"category : {category}")
                if category:
                    #category = categorize.categorize_exepense(text)
                    self.entries["Category:"].set(category)

                if receipt_info["store"]:
                    self.entries["Store Name:"].delete(0, "end")
                    self.entries["Store Name:"].insert(0, receipt_info["store"])
                
                if receipt_info["amount"]:
                    self.entries["Total Amount:"].delete(0, "end")
                    self.entries["Total Amount:"].insert(0, receipt_info["amount"])
                
                if receipt_info["date"]:
                    self.entries["Date:"].delete(0, "end")
                    self.entries["Date:"].insert(0, receipt_info["date"])
                
                messagebox.showinfo("Success", "Image processed. Please verify and correct the extracted information if needed.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
    
    def show_manual_entry(self):
        for label, entry in self.entries.items():
            if label == "Category:":
                entry.set("Bank Transfers")
            else:
                entry.delete(0, "end")
                if label == "Date:":
                    entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.preview_text.delete("1.0", "end")

    def save_receipt(self):
        for label, entry in self.entries.items():
            if not entry.get():
                messagebox.showerror("Error", f"{label} cannot be empty")
                return

        receipt = {
            "date": self.entries["Date:"].get(),
            "store": self.entries["Store Name:"].get(),
            "amount": self.entries["Total Amount:"].get(),
            "category": self.entries["Category:"].get()
        }

        new_receipt = Receipt(
            user_id=4 ,
            store_name=receipt["store"],
            receipt_date=receipt["date"],
            total_amount=receipt["amount"],
            category=receipt["category"]
        )

        receipt_dict = new_receipt.to_dict()
        db_response = self.db_conn.insert("receipts", receipt_dict)
        new_receipt = db_response.data
        if new_receipt :  
            self.receipts.append(new_receipt[0])
            print(f"new receipt : {new_receipt[0]}")
            new_receipt = Receipt.from_dict(new_receipt[0])
            messagebox.showinfo("Success", "Receipt saved successfully!")  
            self.update_receipt_list()
            self.show_manual_entry()

        else : 
            raise ValueError("Failed to register User")
    
        #self.save_receipts()
        # messagebox.showinfo("Success", "Receipt saved successfully!")
    
    def show_all_receipts(self):
        self.update_receipt_list()
    
    def update_receipt_list(self):
    # Clear all rows except the header
        self.table.delete_rows(range(1, len(self.table.values)))

        # Add rows from the current receipt list
        for receipt in self.receipts:
            #print(f"re : {receipt}")
            self.table.add_row([
                receipt.get("receipt_date", "N/A"),  # Correct field for the date
                receipt.get("store_name", "N/A"),   # Correct field for the store name
                f'{receipt.get("total_amount", "N/A")} {receipt.get("currency", "N/A")}',  # Amount with currency
                receipt.get("category", "N/A")     # Correct field for the category
            ])
    # def save_receipts(self):
    #     with open("receipts.json", "w") as f:
    #         json.dump(self.receipts, f)
    
    # def load_receipts(self):
    #     try:
    #         with open("receipts.json", "r") as f:
    #             self.receipts = json.load(f)
    #     except FileNotFoundError:
    #         self.receipts = []