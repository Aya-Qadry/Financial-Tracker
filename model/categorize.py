from transformers import pipeline
import pandas as pd

# pipe = pipeline("text-classification", model="distilbert-base-uncased")

# label_dict = model.config.id2label
# print("Label Dictionary:", label_dict)

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("jonjimenez/transaction-categorization")
model = AutoModelForSequenceClassification.from_pretrained("jonjimenez/transaction-categorization")

# Load the CSV file
transactions_df = pd.read_csv('personal_transactions.csv')

name_column = transactions_df.iloc[:, 1]  

# Process the first 10 transactions
for tran in name_column.tail(10):
    # Tokenize the transaction text
    inputs = tokenizer(tran, return_tensors="pt", truncation=True, padding=True)
    
    # Get model predictions
    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(**inputs)
    
    # Convert logits to probabilities
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # Get the predicted class (label with the highest probability)
    predicted_class = torch.argmax(probs, dim=-1).item()
    
    # Map the predicted class to the actual label
    predicted_label = model.config.id2label[predicted_class]
    
    # Print the result
    print(f"Transaction: {tran} → Predicted Category: {predicted_label}")

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        print(probs)
print(model.config.id2label)