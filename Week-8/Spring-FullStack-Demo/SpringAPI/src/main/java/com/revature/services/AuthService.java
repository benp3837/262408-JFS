package com.revature.services;

//Remember that Service classes are for business logic -
    //data formatting, input validation, etc
    //It makes sure everything looks good before going to the DB or back to the user

import com.revature.models.LoginDTO;
import com.revature.models.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service //1 of the 4 stereotype annotations - makes this Class a bean
public class AuthService {

    //Nothing here yet... Just a placeholder til we talk about DB ops

    //The controllers call services, which call the DAOs (data access objects)

}
