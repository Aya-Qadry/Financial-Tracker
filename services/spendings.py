from collections import defaultdict
import datetime
from app.database import SupabaseDB


class Spendings:
    def __init__(self):
        db_conn = SupabaseDB()
        self.supabase = db_conn
        self.data_periods = {}
        self.category_expenses = {}

    def process_data(self, user_id):
        
        receipts = self.supabase.get_user_receipts(user_id)
        receipts = receipts.data

        weekly = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
        monthly = {month: 0 for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
        quarterly = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
        yearly = {}
        categories = {}
        total_expenses = 0
        for receipt in receipts:
            amount = receipt["total_amount"]
            category = receipt["category"]
            # print(f"category : {category}")

            timestamp = datetime.datetime.fromisoformat(receipt["receipt_date"])

            total_expenses += amount

            day_name = timestamp.strftime("%a")
            if day_name in weekly:
                weekly[day_name] += amount

            # Monthly grouping
            month_name = timestamp.strftime("%b")
            if month_name in monthly:
                monthly[month_name] += amount

            # Quarterly grouping
            quarter = (timestamp.month - 1) // 3 + 1
            quarterly[f"Q{quarter}"] += amount

            # Yearly grouping
            year = timestamp.year
            yearly[str(year)] = yearly.get(str(year), 0) + amount

            categories[category] = categories.get(category, 0) + amount

        if total_expenses > 0:  
            categories = {
                cat: round((amt / total_expenses) * 100, 2)
                for cat, amt in categories.items()
            }
        else:

            categories = {cat: 0 for cat in categories}

        return {
            "data_periods": {
                "Week": weekly,
                "Month": monthly,
                "Quarter": quarterly,
                "Year": yearly,
            },
            "category_expenses": categories,
        }

    def get_monthly_category_spending(self, user_id):
        now = datetime.datetime.now()
        current_month = now.month
        current_year = now.year

        receipts = self.supabase.get_user_receipts(user_id).data

        category_spending = defaultdict(lambda: 0)
        category_currency = {}

        for receipt in receipts:
            receipt_date_str = receipt["receipt_date"]

            if isinstance(receipt_date_str, str):
                receipt_date = datetime.datetime.strptime(receipt_date_str, "%Y-%m-%d")
            else:
                receipt_date = datetime.datetime.fromtimestamp(int(receipt_date_str) / 1000)

            if receipt_date.month == current_month and receipt_date.year == current_year:
                category = receipt["category"]
                amount = receipt["total_amount"]
                currency = receipt["currency"]

                category_spending[category] += amount
                category_currency[category] = currency

        table_data = [["Category Name", "Total Spent"]]

        for category, amount in category_spending.items():
            currency = category_currency.get(category, "$")
            table_data.append([category, f"{amount} {currency}"])

        predefined_categories = ["Food", "Transport", "Shopping", "Bills"]
        for category in predefined_categories:
            if category not in category_spending:
                table_data.append([category, "0"])

        return table_data
