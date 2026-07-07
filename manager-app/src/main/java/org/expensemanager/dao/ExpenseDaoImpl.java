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

            ps.setInt(1, id);
            try(ResultSet rs = ps.executeQuery()){
                if(rs.next()){
                    return new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
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
                    results.add(new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
                    ));
                }
            }
            return results;
        }catch(SQLException e){
            e.printStackTrace();
        }
        return null;
    }

    // For "approved" / "denied" — statuses that exist as approval rows
    @Override
    public ArrayList<Expense> getByStatus(String status){
        String sql = """
                SELECT e.*
                FROM expenses e
                JOIN approvals a ON e.id = a.expense_id
                WHERE a.status = ?;
                """;
        ArrayList<Expense> expenses = new ArrayList<>();
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setString(1, status);
            try(ResultSet rs = ps.executeQuery()){
                while(rs.next()){
                    expenses.add(new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
                    ));
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return expenses;
    }

    // For "pending" - expenses with no approval row
    @Override
    public ArrayList<Expense> getPending(){
        String sql = """
                SELECT e.*
                FROM expenses e
                LEFT JOIN approvals a ON e.id = a.expense_id
                WHERE status = 'pending';
                """;
        ArrayList<Expense> expenses = new ArrayList<>();
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            try(ResultSet rs = ps.executeQuery()){
                while(rs.next()){
                    expenses.add(new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
                    ));
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return expenses;
    }

    @Override
    public ArrayList<Expense> userReport(int id){
        String sql = """
                SELECT *
                FROM expenses
                WHERE user_id = ?;
                """;
        ArrayList<Expense> expenses = new ArrayList<>();
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setInt(1, id);
            try(ResultSet rs = ps.executeQuery()){
                while(rs.next()){
                    expenses.add(new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
                    ));
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return expenses;
    }
    @Override
    public ArrayList<Expense> categoryReport(String category){
        String sql = """
               SELECT *
               FROM expenses
               WHERE category = ?;
                """;
        ArrayList<Expense> expenses = new ArrayList<>();
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setString(1, category);
            try(ResultSet rs = ps.executeQuery()){
                while(rs.next()){
                    expenses.add(new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
                    ));
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return expenses;
    }

    @Override
    public ArrayList<Expense> dateReport(String start, String end){
        String sql = """
              SELECT * 
              FROM expenses 
              WHERE date BETWEEN ? AND ?;
              """;
        ArrayList<Expense> expenses = new ArrayList<>();
        try(Connection conn = ConnectionUtil.getConnection();
            PreparedStatement ps = conn.prepareStatement(sql)){

            ps.setString(1, start);
            ps.setString(2, end);
            try(ResultSet rs = ps.executeQuery()){
                while(rs.next()){
                    expenses.add(new Expense(
                            rs.getInt("id"),
                            rs.getInt("user_id"),
                            rs.getDouble("amount"),
                            rs.getString("description"),
                            rs.getString("date"),
                            rs.getString("category")
                    ));
                }
            }
        }catch(SQLException e){
            e.printStackTrace();
        }
        return expenses;
    }




}