"""
Database connection and initalization
"""
import sqlite3
import os
from typing import Optional

# Root project directory path
_DEFAULT_DB_PATH = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'p0.db')

class DatabaseConnection:
    """Handles SQLite database connections and initalizations"""

    # Defaults to provided db path, then env db path, then default path
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv('DATABASE_PATH', _DEFAULT_DB_PATH)

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row # enable dict acces to rows
        return conn
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            # Create users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password NOT NULL,
                    role TEXT NOT NULL
                ) """) 
            conn.commit()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    amount NUMERICAL CHECK(amount>0),
                    description VARCHAR NOT NULL,
                    date DATE NOT NULL
                ) """) 
            conn.commit()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS approvals (
                    id INTEGER PRIMARY KEY,
                    expense_id INTEGER REFERENCES expenses(id),
                    status VARCHAR NOT NULL,
                    reviewer INTEGER,
                    comment VARCHAR,
                    review_date DATE
                )
            """)
            conn.commit()

            # Create expenses table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                         )
                         """)
            
            
