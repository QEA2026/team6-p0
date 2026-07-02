package org.expensemanager.model;

public class Approval {
    private int id;
    private int expense_id;
    private String status;

    private Integer reviewer; // not int bc has to be nullable (null until a manager reviews it)
    private String comment;
    private String review_date;

    //constructor
    public Approval(int id, int expense_id, String status, Integer reviewer, String comment, String review_date){
        this.id = id;
        this.expense_id = expense_id;
        this.status = status;
        this.reviewer = reviewer;
        this.comment = comment;
        this.review_date = review_date;
    }

    //getters
    public int getId(){
        return this.id;
    }
    public int getExpenseId(){
        return this.expense_id;
    }
    public String getStatus(){
        return this.status;
    }
    public Integer getReviewer(){
        return this.reviewer;
    }
    public String getComment(){
        return this.comment;
    }
    public String getReviewDate(){
        return this.review_date;
    }


    //setters
    public void setStatus(String status){
        this.status = status;
    }
    public void setReviewer(Integer reviewer){
        this.reviewer = reviewer;
    }
    public void setComment(String comment){
        this.comment = comment;
    }
    public void setReviewDate(String review_date){
        this.review_date = review_date;
    }


}
