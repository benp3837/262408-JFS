package com.revature.controllers;

import com.revature.jwt.JwtUtil;
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
    //Inject the JwtUtil so we can make JWTs after login
    private final JwtUtil jwtUtil;

    @Autowired
    public AuthController(AuthService authService, JwtUtil jwtUtil) {
        this.authService = authService;
        this.jwtUtil = jwtUtil;
    }

    //Log in User (POST Requests to /auth will get routed here)
    //TODO: JWTs will get created upon successful login
    @PostMapping
    @CrossOrigin(origins = {"http://localhost:3000", "http://localhost:4200"}, allowedHeaders = "*")
    public ResponseEntity<String> login(@RequestBody LoginDTO loginDTO) {

        if(loginDTO.getUsername().equals("user")){
            String token = jwtUtil.generateToken(loginDTO.getUsername(), "user", 1);

            return ResponseEntity.ok().body(token);
        } else {
            return null;
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
