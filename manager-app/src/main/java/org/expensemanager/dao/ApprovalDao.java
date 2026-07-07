package org.expensemanager.dao;
import org.expensemanager.model.Approval;

public interface ApprovalDao {
    public Approval getById(int id);
    public void submitApproval(int expense_id, String status, int reviewer, String comment);
    Approval getByExpenseId(int expenseId);
    void updateComment(int id, String comment);
}
