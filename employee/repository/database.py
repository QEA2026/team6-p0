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
        conn.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints
        return conn
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            # Drop all tables
            conn.execute("""
                DROP TABLE IF EXISTS approvals
                """)
            conn.commit()
            conn.execute("""
                DROP TABLE IF EXISTS expenses
                """)
            conn.commit()
            conn.execute("""
                DROP TABLE IF EXISTS users
                """)
            conn.commit()

            # Create users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL
                ) """) 
            conn.commit()

            # Create expenses table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    amount NUMERIC CHECK(amount>0),
                    description VARCHAR(255) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    date DATE NOT NULL
                ) """) 
            conn.commit()

            # Create approvals table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS approvals (
                    id INTEGER PRIMARY KEY,
                    expense_id INTEGER REFERENCES expenses(id) ON DELETE CASCADE,
                    status VARCHAR(50) NOT NULL,
                    reviewer INTEGER,
                    comment VARCHAR(255),
                    review_date DATE
                )
            """)
            conn.commit()
            
            
