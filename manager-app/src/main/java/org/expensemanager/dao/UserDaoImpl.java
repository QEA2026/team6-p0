package org.expensemanager.dao;
import org.expensemanager.model.User;
import org.expensemanager.util.ConnectionUtil;
import java.sql.*;

public class UserDaoImpl implements UserDao {
    @Override //Overriding the getByUsername method in UserDao interface
    public User getByUsername(String username) {
        //Sql query: find rows where username = given username
        String sql = "SELECT * FROM users WHERE username = ?";

        // Open new connection, in try block so it closes automatically
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){
        //Modify the sql statement to have username variable in ?, avoiding SQL injection
            ps.setString(1,username);

            try(ResultSet rs = ps.executeQuery()){
                //if username is found in db, make new user object we can use
                if(rs.next()){
                    return new User(
                            rs.getInt("id"),
                            rs.getString("username"),
                            rs.getString("password"),
                            rs.getString("role")
                    );
                }

            }
        }
        catch (SQLException e){
            e.printStackTrace();
        }
        return null;
    }
    @Override
    public User getByPassword(String password) {
        //Sql query: find rows where pw = given pw
        String sql = "SELECT * FROM users WHERE password = ?";

        // Open new connection, in try block so it closes automatically
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){
            //Modify the sql statement to have pw variable in ?, avoiding SQL injection
            ps.setString(1,password);

            try(ResultSet rs = ps.executeQuery()){
                //if pw is found in db, make new user object we can use
                if(rs.next()){
                    return new User(
                            rs.getInt("id"),
                            rs.getString("username"),
                            rs.getString("password"),
                            rs.getString("role")
                    );
                }

            }
        }
        catch (SQLException e){
            e.printStackTrace();
        }
        return null;
    }

}
