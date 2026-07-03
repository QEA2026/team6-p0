package org.expensemanager.dao;
import org.expensemanager.model.Expense;
import java.util.*;

public interface ExpenseDao {
    Expense getById(int id);
    ArrayList<Expense> getAllExpenses();
}
