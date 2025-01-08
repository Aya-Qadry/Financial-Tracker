from customtkinter import *
from CTkTable import CTkTable
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime
import os
import re
import pytesseract
from tests import parser, categorize

class ReceiptExtractor:
    def __init__(self, main_view):
        self.main_view = main_view
        self.receipts = []
        self.load_receipts()
        self.create_widgets()

    def create_widgets(self):
        # clear   main_view  
        for widget in self.main_view.winfo_children():
            widget.destroy()

        self.button_frame = CTkFrame(self.main_view, fg_color="transparent")
        self.button_frame.pack(pady=10)
        
        CTkButton(self.button_frame, text="Upload Receipt Image", 
                  command=self.upload_image).grid(row=0, column=0, padx=5)
        CTkButton(self.button_frame, text="Manual Entry", 
                  command=self.show_manual_entry).grid(row=0, column=1, padx=5)
        CTkButton(self.button_frame, text="View All Receipts", 
                  command=self.show_all_receipts).grid(row=0, column=2, padx=5)
        
        self.entry_preview_container = CTkFrame(self.main_view, fg_color="transparent")
        self.entry_preview_container.pack(pady=10 , fill="x" , padx=10)

        self.entry_frame = CTkFrame(self.entry_preview_container, fg_color="transparent")
        self.entry_frame.grid(row=0 , column = 0 , padx=(0,10), sticky="nsew")
        
        labels = ["Store Name:", "Date:", "Total Amount:", "Category:"]
        self.entries = {}

        for i, label in enumerate(labels):
            CTkLabel(self.entry_frame, text=label).grid(row=i, column=0, pady=5, padx=5, sticky="w")
            if label == "Category:":
                self.entries[label] = CTkComboBox(self.entry_frame, 
                                        values=["Bank Transfers", "Entertainment", "Food & Drink", 
                                                "General Merchandise", "General Services", "Government + Non-Profit", 
                                                "Income", "Loans", "Medical", "Rent & Utilities", "Transportation", 
                                                "Travel", "Other"])
                self.entries[label].grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            elif label == "Date:":
                self.entries[label] = CTkEntry(self.entry_frame)
                self.entries[label].insert(0, datetime.now().strftime("%Y-%m-%d"))
                self.entries[label].grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            else:
                self.entries[label] = CTkEntry(self.entry_frame)
                self.entries[label].grid(row=i, column=1, pady=5, padx=5, sticky="ew")
        
        self.preview_frame = CTkFrame(self.entry_preview_container, fg_color="transparent" )
        self.preview_frame.grid(row=0 , column=1 , sticky="nsew")
        self.preview_text = CTkTextbox(self.preview_frame  )
        self.preview_text.pack(fill="both", expand=True)

        #first entry one part and the second one part
        self.entry_preview_container.grid_columnconfigure(0, weight=1)
        self.entry_preview_container.grid_columnconfigure(1, weight=1)
        # only one row 
        self.entry_preview_container.grid_rowconfigure(0, weight=1)

        CTkButton(self.entry_frame, text="Save Receipt", 
                  command=self.save_receipt).grid(row=len(labels), column=0, columnspan=2, pady=10)
        
        # Receipt list
        # self.receipt_frame = CTkFrame(self.main_view, fg_color="transparent")
        # self.receipt_frame.pack(fill="both", expand=True, padx=10, pady=10)
        

        # self.table = CTkTable(self.receipt_frame, values=[["Date", "Store", "Amount", "Category"]], 
        #                       colors=["#E6E6E6", "#F3F4F6"], header_color="#1E40AF", hover_color="#B4D8F7")
        # self.table.edit_row(0, text_color="#fff", hover_color="#3B82F6")
        # self.table.pack(fill="both", expand=True)
        
        self.update_receipt_list()

    # Other methods (upload_image, show_manual_entry, save_receipt, etc.) remain the same

    def extract_receipt_info(self, text):
        self.preview_text.delete("1.0", "end")
        print(text)
        receipt_processor = parser.ReceiptProcessor("AIzaSyDJuXkjSgz3w1Ov32Kmb59dB5_bwXewZGg")

        store_name = ""
        total_amount = ""
        date = ""
        
        lines = text.split('\n')
        
        # Regular expressions for matching
        amount_pattern = r'\$?\d+\.\d{2}'
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
                print(f"category : {category}")
                if category:
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
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.entries["Date:"].insert(0, datetime.now().strftime("%Y-%m-%d"))
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
        
        self.receipts.append(receipt)
        self.save_receipts()
        self.update_receipt_list()
        self.show_manual_entry()
        messagebox.showinfo("Success", "Receipt saved successfully!")
    
    def show_all_receipts(self):
        self.update_receipt_list()
    
    def update_receipt_list(self):
        self.table.delete_rows(range(1, len(self.table.values)))
        for receipt in self.receipts:
            self.table.add_row([receipt["date"], receipt["store"], receipt["amount"], receipt["category"]])
    
    def save_receipts(self):
        with open("receipts.json", "w") as f:
            json.dump(self.receipts, f)
    
    def load_receipts(self):
        try:
            with open("receipts.json", "r") as f:
                self.receipts = json.load(f)
        except FileNotFoundError:
            self.receipts = []