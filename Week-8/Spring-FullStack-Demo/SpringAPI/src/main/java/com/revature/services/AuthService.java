package com.revature.services;

//Remember that Service classes are for business logic -
    //data formatting, input validation, etc
    //It makes sure everything looks good before going to the DB or back to the user

import com.revature.models.LoginDTO;
import com.revature.models.User;
import com.revature.repositories.UserDAO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service //1 of the 4 stereotype annotations - makes this Class a bean
public class AuthService {

    //The controllers call services, which call the DAOs (data access objects)

    //The Service needs the DAO. They're both beans, so let's CONSTRUCTOR INJECT
    private final UserDAO userDAO;

    @Autowired
    public AuthService(UserDAO userDAO) {
        this.userDAO = userDAO;
    }

    //Insert User - calls the UserDAO's save() method
    public User insertUser(User newUser){

        //TODO: input validation, etc

        //save() is used for inserts AND updates
            //if the ID doesn't exist, it inserts a new record
            //if the ID DOES exist, it updates it
        return userDAO.save(newUser);

        //TODO: maybe strip or obscure the password before sending it back

    }


}
