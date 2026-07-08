from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple, List
from repository.expense_model import Expense
from repository.approval_model import Approval
from repository.expense_repository import ExpenseRepository
from repository.approval_repository import ApprovalRepository

class ExpenseService:

    def __init__(self, expense_repository: ExpenseRepository, approval_repository: ApprovalRepository):
        self.expense_repository = expense_repository
        self.approval_repository = approval_repository

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

        # Validate date
        if not self.validate_date(date):
            raise ValueError("Invalid date. Please use the format YYYY-MM-DD HH:MM:SS.")

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
    
    def get_expense_with_status(self, expense_id: int, user_id: int) -> Optional[Tuple[Expense, Approval]]:
        # Get expense with its approval status, ensuring it belongs to the user.
        expense = self.get_expense_by_id(expense_id, user_id)
        if expense:
            approval = self.approval_repository.find_by_expense_id(expense_id)
            if approval:
                return expense, approval
        return None

    def update_expense(self, expense_id, user_id, amount, description, category, date) -> Optional[Expense]:
        # Update expense by id, validating user_id matches
        result = self.get_expense_with_status(expense_id, user_id)
        
        # Check if result exists and that the given user id is correct
        if not result or result[0].user_id != user_id:
            return None
        
        expense, approval = result

        # Only allow update if expense is still pending
        if approval.status != 'pending':
            raise ValueError("Cannot updated expense that has been reviewed")

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

        # Validate date
        if not self.validate_date(date):
            raise ValueError("Invalid date. Please use the format YYYY-MM-DD HH:MM:SS.")
        
        expense.amount = amount
        expense.description = description
        expense.category = category.capitalize()
        expense.date = date

        return self.expense_repository.update(expense)

    def delete_expense(self, expense_id, user_id) -> bool:
        # Delete expense by id, validating user_id matches
        result = self.get_expense_with_status(expense_id, user_id)

        if not result or result[0].user_id != user_id:
            return None
        
        expense, approval = result

        # Only allow deletion if expense is still pending
        if approval.status != 'pending':
            raise ValueError("Cannot delete expense that has been reviewed.")
        
        return self.expense_repository.delete(expense.id)
    
    def get_expense_history(self, user_id: int, status_filter: str = None, filter_out: bool = False) -> List[Tuple[Expense, Approval]]:
        """Get expense history with optional status filter."""
        all_expenses = self.approval_repository.find_expenses_with_status_for_user(user_id)

        if status_filter and status_filter in ['pending', 'approved', 'denied']:
            if not filter_out:
                return [(expense, approval) for expense, approval in all_expenses
                        if approval.status == status_filter]
            else:
                return [(expense, approval) for expense, approval in all_expenses
                        if approval.status != status_filter]

        return all_expenses
    
    def validate_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False
