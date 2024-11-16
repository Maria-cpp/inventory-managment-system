import sqlite3
from hashlib import sha256

# Initialize the database
# Database setup
class Database:
    def __init__(self) -> None:
        pass

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Initialize database tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price REAL,
                stock_quantity INTEGER
            )
        ''')

        conn.commit()

    def get_db_connection(self):
        try:
            conn = sqlite3.connect('inventory.db')
            print("Databse connected")
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None


    def initialize_db(self):
        conn = self.get_db_connection()
        if conn is None:
            print("Failed to initialize database.")
            return

        try:
            cursor = conn.cursor()

            # Load and execute SQL from init.sql
            with open('init.sql', 'r') as f:
                sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            print("Database initialized successfully from init.sql.")
            
        except (sqlite3.Error, IOError) as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()
