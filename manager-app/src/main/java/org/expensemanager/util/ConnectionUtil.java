package org.expensemanager.util;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectionUtil {
    private static final String URL = "jdbc:sqlite:p0.db"; //path to the db

    public static Connection getConnection() throws SQLException{
        return DriverManager.getConnection(URL);
    }
}
