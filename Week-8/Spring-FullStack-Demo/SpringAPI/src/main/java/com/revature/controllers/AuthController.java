package com.revature.controllers;

import com.revature.models.LoginDTO;
import com.revature.models.User;
import com.revature.services.AuthService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

//Make the Class a Bean and automatically send HTTP response data as JSON
@RestController
//All requests with /auth will get routed here
@RequestMapping("/auth")
//Allow CORS requests from React and Angular frontends
@CrossOrigin(origins = {"http://localhost:5173", "http://localhost:4200"}, allowedHeaders = "*")
public class AuthController {

    //Inject the UserService with Constructor Injection
    private final AuthService authService;

    @Autowired
    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    //Log in User (POST Requests to /auth will get routed here)
    //TODO: JWTs will get created upon successful login
    @PostMapping
    @CrossOrigin(origins = {"http://localhost:3000", "http://localhost:4200"}, allowedHeaders = "*")
    public ResponseEntity<?> login(@RequestBody LoginDTO loginDTO){

        System.out.println(loginDTO);

        //(hardcoded) Upon successful login, return a 200 OK and a success message
        if(loginDTO.getUsername().equals("user") && loginDTO.getPassword().equals("pass")){
            return ResponseEntity.ok().body(loginDTO);
        } else {
            //otherwise... send a 401 Unauthorized with a failure message
            return ResponseEntity.status(401).body("Invalid credentials");
        }

    }

    //Register User (POST Requests to /auth/register will get routed here)
    @PostMapping("/register")
    public ResponseEntity<User> registerUser(@RequestBody User newUser){

        //Send the newUser to the Service to get processed and persisted
        User createdUser = authService.insertUser(newUser);

        return ResponseEntity.status(201).body(createdUser);

        //No error handling here! Check the @ExceptionHandler at the bottom of this file

    }

    //Exception Handling---------------------------------------------

    /*Avoid error handling bloat in your controllers!
    Any Exceptions thrown from the Service layer will be caught here
    Our controller methods can now focus solely on success states */

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<String> handleIllegalArgument(IllegalArgumentException e){
        //Return a bad request (400) with the Exception message
        return ResponseEntity.badRequest().body(e.getMessage());
    }

}
