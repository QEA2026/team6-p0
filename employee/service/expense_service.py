from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple, List
from repository.expense_model import Expense
from repository.expense_repository import ExpenseRepository

class ExpenseService:

    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repository = expense_repository

    def submit_expense(self, user_id: int, amount: float, description: str, category: str, date: str = None) -> Expense:
        # Submit a new expense for the employee
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not description.strip():
            raise ValueError("Description is required")
        if not category.strip():
            raise ValueError("Category is required")
        
        # Enforce Categories
        if category.strip().lower() not in ["supplies", "meals", "entertainment", "travel", "lodging", "other"]:
            raise ValueError("Category label must exist.")
        
        # Use current date if none is provided
        if not date:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        expense = Expense(
            user_id=user_id,
            amount=amount,
            description=description,
            category=category.capitalize(),
            date=date
        )
        return self.expense_repository.create(expense)

    def get_expense_by_id(self, expense_id, user_id) -> Optional[Expense]:
        # Get an expense by expense id, ensuring it belongs to the current user
        expense = self.expense_repository.find_by_id(expense_id)
        if expense and expense.user_id == user_id:
            return expense
        return None

    def update_expense(self, expense_id, user_id, amount, description, category, date) -> Optional[Expense]:
        # Update expense by id, validating user_id matches
        result = self.expense_repository.find_by_id(expense_id)
        
        # Check if result exists and that the given user id is correct
        if not result or result.user_id != user_id:
            return None

        # Validate other fields are valid
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if not description.strip():
            raise ValueError("Description is required")
        if not category.strip():
            raise ValueError("Category is required")
        
        # Enforce Categories
        if category.strip().lower() not in ["supplies", "meals", "entertainment", "travel", "lodging", "other"]:
            raise ValueError("Category label must exist.")

        # Use current date if none is provided
        if not date:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result.amount = amount
        result.description = description
        result.category = category.capitalize()
        result.date = date

        return self.expense_repository.update(result)

    def delete_expense(self, expense_id, user_id) -> bool:
        # Delete expense by id, validating user_id matches
        result = self.expense_repository.find_by_id(expense_id)

        if not result or result.user_id != user_id:
            return None
        
        return self.expense_repository.delete(result.id)
    
    def get_user_expenses(self, user_id) -> List[Expense]:
        # Get all expenses for the current user
        return self.expense_repository.find_by_user_id(user_id)
    