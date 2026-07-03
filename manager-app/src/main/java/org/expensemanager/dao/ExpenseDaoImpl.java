package org.expensemanager.dao;
import org.expensemanager.model.Expense;
import org.expensemanager.util.ConnectionUtil;
import java.sql.*;
import java.util.*;

public class ExpenseDaoImpl implements ExpenseDao {
    @Override
    public Expense getById(int id){
        String sql = "SELECT * FROM expenses WHERE id = ?";
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setInt(1,id);
            try(ResultSet rs = ps.executeQuery()){
                if(rs.next()){
                    return new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date")
                            );
                }
            }

        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }
    @Override
    public ArrayList<Expense> getAllExpenses(){
        String sql = "SELECT * FROM expenses";
        try(Connection conn = ConnectionUtil.getConnection();
            Statement s = conn.createStatement()){
            ArrayList<Expense> results = new ArrayList<>();
            try(ResultSet rs = s.executeQuery(sql)){
                while(rs.next()){
                    results.add( new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date")
                    ));
                }
            }
        return results;
        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }
}
