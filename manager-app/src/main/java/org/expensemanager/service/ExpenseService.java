package org.expensemanager.service;
import org.expensemanager.dao.ApprovalDao;
import org.expensemanager.dao.ExpenseDao;
import org.expensemanager.model.Expense;

import java.util.ArrayList;

public class ExpenseService {

    private ExpenseDao expenseDao;
    private ApprovalDao approvaldao;

    public ExpenseService(ExpenseDao expenseDao, ApprovalDao approvaldao){
        this.expenseDao = expenseDao;
        this.approvaldao = approvaldao;
    }


    public ArrayList<Expense> viewPendingExpenses(){
        return expenseDao.getPending();
    }

    public void reviewExpense(int expenseId, String status, int reviewer, String comment){
        Expense expense = expenseDao.getById(expenseId);
        if(!status.equalsIgnoreCase("approved") && !status.equalsIgnoreCase("denied")){
            System.out.println("Not valid status, please enter 'approved' or 'denied'");
        } else if (expense == null) {
            System.out.println("Expense ID doesn't match Database");
        } else if(approvaldao.getByExpenseId(expenseId)!=null){
            System.out.println("This expense has already been reviewed!");
        } else {
            status = status.toLowerCase();
            approvaldao.submitApproval(expenseId,status,reviewer,comment);
        }
    }

    public void updateComment(int id, String comment){
        if(approvaldao.getById(id)==null){
            System.out.println("Approval ID doesn't match Database");
        }
        else {
            approvaldao.updateComment(id, comment);
        }
    }

    public ArrayList<Expense> generateUserReport(int id){
        if(expenseDao.getById(id)==null){
            System.out.println("No matching user ID exists in Database ");
            return null;
        }
        else {
            return expenseDao.userReport(id);
        }
    }
    public ArrayList<Expense> generateCategoryReport(String category){
        if(expenseDao.categoryReport(category)==null){
            System.out.println("No expenses in category" + category);
            return null;
        }
        else{
            return expenseDao.categoryReport(category);
        }
    }
    public ArrayList<Expense> generateDateReport(String start, String end) {
        if (expenseDao.dateReport(start, end) == null) {
            System.out.println("No expenses in entered date range");
            return null;
        } else {
            return expenseDao.dateReport(start, end);
        }
    }

}
