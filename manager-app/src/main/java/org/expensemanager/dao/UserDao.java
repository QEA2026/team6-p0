package org.expensemanager.dao;
import org.expensemanager.model.User;

import java.util.ArrayList;

public interface UserDao {
    User getByUsername(String username);
    User getByPassword(String password);
    User getById(int id);
    ArrayList<User> getAllUsers();
}
