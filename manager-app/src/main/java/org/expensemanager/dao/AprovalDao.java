package org.expensemanager.dao;
import org.expensemanager.model.Approval;

public interface AprovalDao {
    public Approval getById(int id);
    public void submitApproval(int expense_id, String status, int reviewer, String comment);
}
