package org.expensemanager.dao;
import org.expensemanager.model.Approval;
import org.expensemanager.dao.AprovalDao;
import org.expensemanager.model.Expense;
import org.expensemanager.util.ConnectionUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ApprovalDaoImpl implements AprovalDao {
    @Override
    public Approval getById(int id) {
        String sql = "SELECT * FROM approvals WHERE id = ?";
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setInt(1,id);
            try(ResultSet rs = ps.executeQuery()){
                if(rs.next()){
                    return new Approval(
                            rs.getInt("id"),
                            rs.getInt("expenseId"),
                            rs.getString("status"),
                            rs.getObject("reviewer", Integer.class),
                            rs.getString("comment"),
                            rs.getString("reviewDate")
                    );
                }
            }

        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }
}
