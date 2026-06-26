package org.expensemanager.model;

public class Expense {

    private int id;
    private int userId;
    private double amount;
    private String description;
    private String date;
    private String category;
    private String status;

    //constructor
    public Expense(int id, int userId, double amount, String description, String date, String status, String category){
        this.id = id;
        this.userId = userId;
        this.amount = amount;
        this.description = description;
        this.date = date;
        this.status = status;
        this.category = category;
    }

    //getters
    public int getId(){
        return this.id;
    }
    public int getUserId(){
        return this.userId;
    }
    public double getAmount(){
        return this.amount;
    }
    public String getDescription(){
        return this.description;
    }
    public String getDate(){
        return this.date;
    }
    public String getStatus(){
        return this.status;
    }
    public String getCategory(){
        return this.category;
    }

    //setters
    public void setAmount(double amount){
        this.amount = amount;
    }
    public void setDescription(String description){
        this.description = description;
    }
    public void setDate(String date){
        this.date = date;
    }
    public void setStatus(String status){
        this.status = status;
    }
    public void setCategory(String category){
        this.category = category;
    }
}
