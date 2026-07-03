package org.expensemanager.model;

public class Expense {

    private int id;
    private int user_id;
    private double amount;
    private String description;
    private String date;

    //constructor
    public Expense(int id, int user_id, double amount, String description, String date){
        this.id = id;
        this.user_id = user_id;
        this.amount = amount;
        this.description = description;
        this.date = date;
    }

    //getters
    public int getId(){
        return this.id;
    }
    public int getUserId(){
        return this.user_id;
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

}
