import cv2
import pytesseract
import re
import pandas as pd

# Step 1: Preprocess the image
image = cv2.imread("C:/Users/ayaqa/OneDrive/Documents/FSTE/S3/Financial Tracker/receipts/rest.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Step 2: Extract text with layout analysis
extracted_text = pytesseract.image_to_string(thresh, config='--psm 6')

# Step 3: Parse the text
date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{4}[/-]\d{1,2}[/-]\d{1,2})"
total_pattern = r"(Total|TOTAL|Amount)\s*[\$€]?\s*(\d+\.\d{2})"
item_pattern = r"(\d+)\s+([\w\s]+)\s+[\$€]?\s*(\d+\.\d{2})"

date = re.search(date_pattern, extracted_text)
total = re.search(total_pattern, extracted_text)
items = re.findall(item_pattern, extracted_text)

# Step 4: Handle missing fields
date = date.group() if date else "Unknown"
total = total.group(2) if total else "Unknown"

# Step 5: Organize the data
data = {
    "Item": [item[1] for item in items],
    "Quantity": [item[0] for item in items],
    "Price": [item[2] for item in items]
}
df = pd.DataFrame(data)

metadata = {
    "Date": [date],
    "Total Amount": [total]
}
df_metadata = pd.DataFrame(metadata)

# Display the data
print("Extracted Text:\n", extracted_text)
print("\nItems:\n", df)
print("\nMetadata:\n", df_metadata)