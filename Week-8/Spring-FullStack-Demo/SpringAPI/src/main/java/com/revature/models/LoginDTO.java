package com.revature.models;

/*Remember a DTO is a Data Transfer Object - it helps us move certain data around

I like having a model for certain things that will never hit the DB.
    -In this case username/login credentials. We'll pass this around during login

Yes, you could just have a constructor in User that only has username/password instead */
public class LoginDTO {

    private String username;
    private String password;

    public LoginDTO() {
    }

    public LoginDTO(String username, String password) {
        this.username = username;
        this.password = password;
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

    @Override
    public String toString() {
        return "LoginDTO{" +
                "username='" + username + '\'' +
                ", password='" + password + '\'' +
                '}';
    }
}
