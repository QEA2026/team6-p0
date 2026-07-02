package org.expensemanager.dao;
import org.expensemanager.model.Expense;
import org.expensemanager.util.ConnectionUtil;
import java.sql.*;

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
                            rs.getInt("userId"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("status"),
                            rs.getString("category")
                            );
                }
            }

        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }
}
