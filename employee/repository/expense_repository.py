from .expense_model import Expense
from .database import DatabaseConnection
from datetime import datetime

class ExpenseRepository:
    """Repo for expense related db operations"""
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def create(self, expense: Expense):
        with self.db_connection.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO expenses (user_id, amount, description, date) VALUES (?, ?, ?, ?)",
                (expense.user_id, expense.amount, expense.description, expense.date)
                )
            # return the last row id inserted by this cursor
            expense.id = cursor.lastrowid
            conn.commit()
        return expense

    def find_by_id(self, expense_id: int): 
        with self.db_connection.get_connection() as conn:
            cursor = conn.execute("SELECT id, user_id, amount, description, date FROM expenses WHERE id = ?", 
                                  (expense_id))
            row = cursor.fetchone()
            if(row):
                return Expense(id=row['id'],user_id=['user_id'],amount=['amount'],description=['description'],date=['date'])
        return None
        
    def find_by_user_id(self, user_id: int):
        with self.db_connection.get_connection() as conn:
            expenses = []
            cursor = conn.execute("SELECT id, user_id, amount, description, date FROM expenses WHERE user_id = ?",
                                  (user_id,))
            for row in cursor.fetchall():
                expenses.append(Expense(id=row['id'], user_id=row['user_id'], amount=row['amount'], description=row[
                                'description'], date=row['date']))
            return expenses

    def update(self, expense: Expense):
        with self.db_connection.get_connection() as conn:
            conn.execute("UPDATE expenses SET amount = ?, description = ?, date = ? WHERE id = ?",
                                  (expense.amount, expense.description, expense.date, expense.id))
            conn.commit()
        return expense
    
    def delete(self, expense_id: int):
        with self.db_connection.get_connection() as conn:
            cursor = conn.execute("DELETE FROM expense WHERE id = ?",
                                  (expense_id)
                                  )
            conn.commit()
        # Number of rows effected by the cursor statement, TRUE means successful delete and vice versa
        return cursor.rowcount > 0
