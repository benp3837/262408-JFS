package com.revature.controllers;

//SpringMVC (Model View Controller) lets us take in HTTP Requests and send HTTP Responses
    //INTEGRAL part of full stack applications

//M - Model - the data being "model"ed in our application (Boat)
//V - View - the front end (or whatever is the requests)
//C - Controller - the layer that handles the HTTP requests

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@RequestMapping("/boat")
@ResponseBody
public class BoatController {

    //Here's a super generic SpringMVC controller method
    @GetMapping
    public String getGreeting(){
        return "Hello from the BoatController!";
    }

}
