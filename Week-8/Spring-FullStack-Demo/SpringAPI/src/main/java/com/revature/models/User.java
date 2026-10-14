package com.revature.models;

import jakarta.persistence.*;

import java.util.List;
import java.util.Set;

//No @Component here - we're going to make it a Database Entity

@Entity //This tells Spring Data that this Class is meant to be a DB entity (DB table)
@Table(name = "users") //This helps us set table configs like the name
public class User {

    //Make sure all variable names are camelCase - this will help Spring Data
    //Spring Data doesn't play nice with snake_case, and the errors will be super vague

    @Id //Sets this field as the Primary Key (PK)
    @GeneratedValue(strategy = GenerationType.IDENTITY) //This is what makes the PK autoincrement
    private int userId;

    //@Column - this is not needed to make a field a column!!!
        //BUT, we need it to apply constraints

    @Column(unique = true, nullable = false)
    private String username;

    private String password;

    private String role;

    //TODO: one-to-many relationship with Game


    //boilerplate---------------------------------

    //no args, all args minus ID, all args, getter/setter, toString

    public User() {
    }

    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public User(int userId, String username, String password, String role) {
        this.userId = userId;
        this.password = password;
        this.username = username;
        this.role = role;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", role='" + role + '\'' +
                '}';
    }
}
