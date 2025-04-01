"""Database initialization script"""

import sqlite3

# SQL Query to create tables
create_vendors_table = """
    CREATE TABLE IF NOT EXISTS vendors (
        bank_name TEXT,
        short_name TEXT,
        category TEXT,
        name_source TEXT
    )
    """


def initialize_tables():
    """Initialize the database tables"""
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(create_vendors_table)
            print("Tables initialized successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False


def get_tables():
    """Get the list of tables in the database"""
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Folowwing tables are initialised {tables}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False


def seed():
    """Seed the tables - Only for testing"""
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO vendors VALUES
            ('PHONEPE PRIVATE LTD MUMBAI - 20', 'Phonepe', 'Misc', 'HDFC'),
            ('PHONEPE PRIVATE LTD MUMBAI 25', 'Phonepe', 'Misc', 'HDFC'),
            ('INDIAN RAILWAY CATERINGNEW DELHI 10', 'IRCTC', 'Travel', 'HDFC'),
            ('INDIAN RAILWAY CATERINGNEW DELHI - 10', 'IRCTC', 'Travel', 'HDFC'),
            ('INDIAN RAILWAY CATERINGNEW DELHI 20', 'IRCTC', 'Travel', 'HDFC'),
            ('INDIAN RAILWAY CATERINGNEW DELHI - 25', 'IRCTC', 'Travel', 'HDFC'),
            ('INDIAN RAILWAY CATERINGNEW DELHI - 30', 'IRCTC', 'Travel', 'HDFC'),
            ('INDIAN RAILWAY CATERINGNEW DELHI 35', 'IRCTC', 'Travel', 'HDFC'),
            ('TONI AND GUY THRISSUR 15', 'Toni & Guy', 'Personal Care', 'HDFC'),
            ('PADINHA KARA FUELS KOZ KOZHIKOD', 'Petrol', 'Travel', 'HDFC'),
            ('PADINHA KARA FUELS KOZHIKODE', 'Petrol', 'Travel', 'HDFC'),
            ('PETRO SURCHARGE WAIVER', 'Petrol', 'Travel', 'HDFC'),
            ('PlayStationNetwork UNITED KINGD 50', 'PlayStation', 'Entertainment', 'HDFC'),
            ('IGST-VPS2523169270993-RATE 18.0 -29 (Ref# ST242310084000011028173)', 'HDFC', 'Misc', 'HDFC'),
            ('ZOMATO LIMITED GURGAON', 'Zomato', 'Dining', 'HDFC'),
            ('ZOMATO LIMITED GURGAON 5', 'Zomato', 'Dining', 'HDFC'),
            ('ZOMATO LIMITED GURGAON 10', 'Zomato', 'Dining', 'HDFC'),
            ('ZOMATO LIMITED GURGAON 15', 'Zomato', 'Dining', 'HDFC'),
            ('ZOMATO LIMITED GURGAON 20', 'Zomato', 'Dining', 'HDFC')
        """
        cursor.execute(query)


if __name__ == "__main__":
    initialize_tables()
    get_tables()
    # seed()
