package org.expensemanager.dao;
import org.expensemanager.model.User;

public interface UserDao {
    User getByUsername(String username);
    User getByPassword(String password);
    User getById(int id);
}
