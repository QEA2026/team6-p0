package org.expensemanager.model;

public class User {
    private int id;
    private String username;
    private String password;
    private String role;
//user constuctor
    public User(int id, String username, String password, String role ){
        this.id = id;
        this.username = username;
        this.password = password;
        this.role = role;
    }
//getters
    public String getUsername(){
        return this.username;
    }
    public int getId(){
        return this.id;
    }
    public String getRole(){
        return this.role;
    }
    public String getPassword(){ // consider hashing this and compare hashes
        return this.password;
    }
    //setters
    public void setUsername(String username){
        this.username = username;
    }
    public void setPassword(String password){
        this.password = password;
    }
    public void setRole(String role){
        this.role = role;
    }
}
