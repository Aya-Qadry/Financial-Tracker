import requests
import json
from typing import Dict, Optional, Any

class ReceiptProcessor:
    def __init__(self, api_key: str):
 
        self.api_key = api_key
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    # either none , or the dictionary as in the json document 
    def process_receipt(self, receipt_text: str) -> Optional[Dict[str, Any]]:
            prompt = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": f"""Return ONLY a valid JSON object according to this structure, with no additional text, comments, or markdown:
                                {{
                                "store_name": string,
                                "date": "YYYY-MM-DD",
                                "time": "HH:mm:ss",
                                "items": [
                                    {{
                                    "name": string,
                                    "total": number
                                    }}
                                ],
                                "subtotal": number,
                                "tax": number,
                                "total_amount": number
                                }}

                                Rules:
                                - Numbers must be actual numbers (not strings)
                                - Use null for missing values
                                - Clean store names of OCR artifacts
                                - Group items by categories when present

                                Receipt text:
                                {receipt_text}"""
                            }
                        ]
                    }
                ]
            }
            
            try:
                # Make API request
                response = requests.post(
                    f"{self.api_url}?key={self.api_key}",
                    json=prompt,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # More thorough cleanup
                    text_response = self._clean_response(text_response)
                    
                    try:
                        receipt_data = json.loads(text_response)
                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error: {str(e)}\nResponse text: {text_response}")
                        return None
                    
                    # Validate and fix the data
                    self.validate_receipt_data(receipt_data)
                    
                    return receipt_data
                
                return None
                
            except requests.RequestException as e:
                print(f"API request error: {str(e)}")
                return None
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return None

    def _clean_response(self, text: str) -> str:
        """Clean the response text of any problematic formatting."""
        # Remove markdown code blocks
        text = text.replace('```json', '').replace('```', '')
        # Remove any leading/trailing whitespace
        text = text.strip()
        # Remove any BOM characters
        text = text.encode('utf-8').decode('utf-8-sig')
        # Remove any non-JSON text before or after the JSON object
        try:
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                text = text[start_idx:end_idx]
        except Exception:
            pass
        return text

    def validate_receipt_data(self, data: Dict[str, Any]) -> None:
        """Validate and fix receipt data."""
        # Ensure all required fields exist with default values
        required_fields = ['store_name', 'date', 'time', 'items', 'subtotal', 'tax', 'total_amount']
        
        # Set default values for missing numeric fields
        data["subtotal"] = data.get("subtotal", 0) or 0
        data["tax"] = data.get("tax", 0) or 0
        data["total_amount"] = data.get("total_amount", 0) or 0

        # Convert string numbers to float if needed
        for field in ['subtotal', 'tax', 'total_amount']:
            if isinstance(data.get(field), str):
                try:
                    data[field] = float(data[field].replace(',', ''))
                except (ValueError, AttributeError):
                    data[field] = 0

        # Check required fields
        for field in required_fields:
            if field not in data:
                print(f"Warning: Missing required field '{field}'")
                data[field] = "" if field in ['store_name', 'date', 'time'] else [] if field == 'items' else 0

        # Validate and fix items
        if "items" in data:
            if not isinstance(data["items"], list):
                data["items"] = []
            
            for item in data["items"]:
                if not isinstance(item, dict):
                    continue
                    
                # Convert string totals to float
                if isinstance(item.get("total"), str):
                    try:
                        item["total"] = float(item["total"].replace(',', ''))
                    except (ValueError, AttributeError):
                        item["total"] = 0
                
                item["total"] = item.get("total", 0) or 0
                item["name"] = item.get("name", "Unknown Item")

        # Validate totals
        if isinstance(data.get('items'), list):
            calculated_total = sum(item.get('total', 0) for item in data['items'])
            if abs(calculated_total - data.get('total_amount', 0)) > 0.01:
                print(f"Warning: Calculated total ({calculated_total}) differs from receipt total ({data.get('total_amount')})")

    def format_receipt(self, receipt_data: Optional[Dict[str, Any]]) -> str:
        if not receipt_data:
            return "Please enter the expense information manually"
        
        formatted_output = f"""
            Store: {receipt_data.get('store_name', 'Unknown')}
            Date: {receipt_data.get('date', 'Unknown')}
            Time: {receipt_data.get('time', 'Unknown')}
            Items Purchased:"""
                    
        items = receipt_data.get('items', [])
        if items:
            for index, item in enumerate(items, start=1):
                formatted_output += f"""
                {index}. {item.get('name', 'Unknown')}:
                Total: {item.get('total', 'N/A')}"""

        formatted_output += f"""
            Subtotal: {receipt_data.get('subtotal', 'N/A')}
            Tax: {receipt_data.get('tax', 'N/A')}
            Total Amount: {receipt_data.get('total_amount', 'N/A')}
            """
        return formatted_output
if __name__ == "__main__":

    processor = ReceiptProcessor("AIzaSyDJuXkjSgz3w1Ov32Kmb59dB5_bwXewZGg")
    
    receipt_text = """Marjane ra] ul po

market

HARJANE HARKET ERRACHIDIA J
TCE: 001531179000052  1.F:01085012 PATENTE: 39502542

02/01/25 ~ 19:26:20 30 7 84113

OPERATION ; VENTE
(5)6111032008583 — FROMAGE FRAIS NS GER

2x 2.95 5.90
(5111126001841 CREHE CHERGUT AROMES

2x 2.50 5.00
CREMERIE 10.90
(5)6281001101192 DEWTIFRICE COLGATE A 20.90
(5)6111254875062  SAVON MAIN LIQUIDE A 13.95
BEAUTE-SANTE 34.85
(5)6111259345430 NUTRY 5 CEREALS 256x 3.10
(5)8410525127465 ROLLER FRATSE

2x 3.95 7.90
(5)40084077 CHOCOLAT KINDER MAKI 4.20
BISCUITERIE 15.20
(5)2000001057186 SAC TNT A BRETELLE 4 1.00
MENAGE 1.00
ee, |
TOTAL : 61.95
CB AUTO 61.95

CLES : 11
Mia SE aes CARTE HARJANE xx

Kea Ng
t de : 52 lh
votre aa sol est de * $2.45 Dh

q ,
VENTILATION Pt vA |
cook «= -TOT.HT-—AUX LV.A a

5 1.6251 20.002 re

" a iN

25010201 391626 140007003008

SERVICE CLIENT 08 02 02 20 i.

"Har Jane Harket votre

Retrouvez Mots sur wv. war arket.wa
ex HERCI DF VOTRE VISITE x=

"""
    
    result = processor.process_receipt(receipt_text)
    
    if result:
        # indent is the space before the embedded value to make them appear more hierarchal
        print(json.dumps(result, indent=2))
    else:
        print("Failed to process receipt")