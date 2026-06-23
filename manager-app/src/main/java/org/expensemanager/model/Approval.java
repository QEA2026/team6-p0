package org.expensemanager.model;

public class Approval {
    private int id;
    private int expenseId;
    private String status;

    private Integer reviewer; // not int bc has to be nullable (null until a manager reviews it)
    private String comment;
    private String reviewDate;

    //constructor
    public Approval(int id, int expenseId, String status, Integer reviewer, String comment, String reviewDate){
        this.id = id;
        this.expenseId = expenseId;
        this.status = status;
        this.reviewer = reviewer;
        this.comment = comment;
        this.reviewDate = reviewDate;
    }

    //getters
    public int getId(){
        return this.id;
    }
    public int getExpenseId(){
        return this.expenseId;
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
        return this.reviewDate;
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
    public void setReviewDate(String reviewDate){
        this.reviewDate = reviewDate;
    }


}
