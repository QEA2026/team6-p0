package org.expensemanager.dao;
import org.expensemanager.model.Approval;

public interface AprovalDao {
    public Approval getById(int id);
    public Approval submitApproval()
}
