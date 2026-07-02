package org.expensemanager.dao;
import org.expensemanager.model.Expense;

public interface ExpenseDao {
    Expense getById(int id);
}
