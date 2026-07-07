package org.expensemanager.dao;
import org.expensemanager.model.Approval;
import org.expensemanager.util.ConnectionUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;

public class ApprovalDaoImpl implements ApprovalDao {

    @Override
    public Approval getById(int id) {
        String sql = "SELECT * FROM approvals WHERE id = ?";
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setInt(1, id);
            try(ResultSet rs = ps.executeQuery()){
                if(rs.next()){
                    return new Approval(
                            rs.getInt("id"),
                            rs.getInt("expense_id"),
                            rs.getString("status"),
                            rs.getObject("reviewer", Integer.class),
                            rs.getString("comment"),
                            rs.getString("review_date")
                    );
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public Approval getByExpenseId(int expenseId) {
        String sql = "SELECT * FROM approvals WHERE expense_id = ?";
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setInt(1, expenseId);
            try(ResultSet rs = ps.executeQuery()){
                if(rs.next()){
                    return new Approval(
                            rs.getInt("id"),
                            rs.getInt("expense_id"),
                            rs.getString("status"),
                            rs.getObject("reviewer", Integer.class),
                            rs.getString("comment"),
                            rs.getString("review_date")
                    );
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public void submitApproval(int expenseId, String status, int reviewer, String comment){
        String reviewDate = LocalDate.now().toString();
        String sql = """
                INSERT INTO approvals(expense_id, status, reviewer, comment, review_date)
                VALUES (?, ?, ?, ?, ?);
                """;
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){
            ps.setInt(1, expenseId);
            ps.setString(2, status);
            ps.setInt(3, reviewer);
            ps.setString(4, comment);
            ps.setString(5, reviewDate);
            ps.executeUpdate();
        }catch (SQLException e){
            e.printStackTrace();
        }
    }

    @Override
    public void updateComment(int id, String comment){
        String sql = """
                UPDATE approvals
                SET comment = ?
                WHERE id = ?;
                """;
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){
            ps.setString(1, comment);
            ps.setInt(2, id);
            ps.executeUpdate();
        }catch(SQLException e){
            e.printStackTrace();
        }
    }
}