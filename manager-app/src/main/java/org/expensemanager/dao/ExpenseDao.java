package org.expensemanager.dao;
import org.expensemanager.model.Expense;
import java.util.*;

public interface ExpenseDao {
    Expense getById(int id);
    ArrayList<Expense> getAllExpenses();
    ArrayList<Expense> getByStatus(String status);
    ArrayList<Expense> getPending();
    ArrayList<Expense> userReport(int id);
    ArrayList<Expense> categoryReport(String category);
    ArrayList<Expense> dateReport(String start, String end);

}
