package org.expensemanager.service;
import org.expensemanager.dao.UserDao;
import org.expensemanager.model.User;


public class UserService {

    private UserDao userDao;
    public UserService(UserDao userDao){
        this.userDao = userDao;
    }

    public User login(String username, String password) {
        User user = userDao.getByUsername(username);

        if (user == null) {
            return null;              // no such username
        }
        if (!user.getPassword().equals(password)) {
            return null;              // wrong password
        }
        return user;                  // success
    }
}
