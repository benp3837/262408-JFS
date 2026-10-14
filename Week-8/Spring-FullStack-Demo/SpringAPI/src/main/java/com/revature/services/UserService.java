package com.revature.services;

import com.revature.models.User;
import com.revature.repositories.UserDAO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service //make this class a bean!
public class UserService {

    //Constructor Inject the UserDAO

    private final UserDAO userDAO;

    @Autowired
    public UserService(UserDAO userDAO) {
        this.userDAO = userDAO;
    }

    //Get all Users
    public List<User> getAllUsers(){

        //Don't really need to error handle
        //Let's obscure the passwords though

        //Thank you Spring Data! findAll() was generated for us :)
        List<User> users = userDAO.findAll();

        //Kind of janky solution, really would prefer something like BCrypt
        for(User u : users){
            u.setPassword("********");
        }

        return users;

    }


}
