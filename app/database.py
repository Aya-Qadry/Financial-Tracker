from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional


import psycopg2
from dotenv import load_dotenv
import os


class SupabaseDB:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
 
        self.supabase_url = "https://hbfavkypztytwucqjfuc.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhiZmF2a3lwenR5dHd1Y3FqZnVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzYyMzU2ODQsImV4cCI6MjA1MTgxMTY4NH0.YefbLK5XG64emVKPD34P1oi-zLuwr85nVKacTGn3Igg"
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found. Please provide URL and key or set environment variables.")
        try : 
            self.client = create_client(self.supabase_url, self.supabase_key)
        except : 
            print("connection couldnt be established with the DB")

    def select_all(self, table_name: str):
        """Get all records from a table"""
        return self.client.table(table_name).select("*").execute()

    def select_by_id(self, table_name: str, id: int):
        """Get a record by ID"""
        return self.client.table(table_name).select("*").eq("id", id).execute()

    def insert(self, table_name: str, data: Dict[str, Any]):
        """Insert a new record"""
        return self.client.table(table_name).insert(data).execute()

    def insert_many(self, table_name: str, data: list[Dict[str, Any]]):
        """Insert multiple records"""
        return self.client.table(table_name).insert(data).execute()

    def update(self, table_name: str, id: int, data: Dict[str, Any]):
        """Update a record by ID"""
        return self.client.table(table_name).update(data).eq("id", id).execute()

    def delete(self, table_name: str, id: int):
        """Delete a record by ID"""
        return self.client.table(table_name).delete().eq("id", id).execute()

    def filter(self, table_name: str, column: str, value: Any):
        """Filter records by column value"""
        return self.client.table(table_name).select("*").eq(column, value).execute()

    def existing_user(self, table_name: str, email: str, phone_number: str):
        try:
            data = self.client.from_(table_name)\
                .select("*")\
                .or_(f"email.eq.{email},phone_number.eq.{phone_number}")\
                .execute()
            
            # Convert the response to a list and check if it's empty
            result = list(data)
            print("Debug - Query result:", result)
            return bool(result)
        except Exception as e:
            print(f"Debug - Error in query: {str(e)}")
            raise e
    
    def custom_query(self, table_name: str, query_builder):
        """
        Execute a custom query using a query builder function
        
        Example:
        def query_builder(query):
            return query.select("*").eq("status", "active").order("created_at", desc=True)
        """
        base_query = self.client.table(table_name)
        return query_builder(base_query).execute()

# Example usage
def main():
    # Initialize with environment variables
    db = SupabaseDB()
    
    # Or initialize with explicit credentials
    # db = SupabaseDB(url="your_url", key="your_key")
    
    # Example operations
    try:
        # Insert a record
        new_record = {"first_name": "John Doe", "email": "john@example.com"}
        result = db.insert("User", new_record)
        print("Inserted:", result)
        
        # Select all records
        all_User = db.select_all("User")
        print("All User:", all_User)
        
        # Custom query example
        def custom_query_builder(query):
            return query.select("*")\
                       .eq("status", "active")\
                       .order("created_at", desc=True)\
                       .limit(10)
        
        active_User = db.custom_query("User", custom_query_builder)
        print("Active User:", active_User)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()