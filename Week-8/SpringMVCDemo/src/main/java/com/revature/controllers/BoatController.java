package com.revature.controllers;

//SpringMVC (Model View Controller) lets us take in HTTP Requests and send HTTP Responses
    //INTEGRAL part of full stack applications

//M - Model - the data being "model"ed in our application (Boat)
//V - View - the front end (or whatever is the requests)
//C - Controller - the layer that handles the HTTP requests

import com.revature.models.Boat;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller //1 of the 4 stereotype annotations (Makes a Class a Bean)
@RequestMapping("/boat") //Any requests to the API starting in /boat will go here
@ResponseBody //This turns all of our HTTP Response data into JSON for us.
public class BoatController {

    //Here's a super generic SpringMVC controller method
    @GetMapping // GET requests to /boat will trigger this method
    public String getGreeting(){
        return "Hello from the BoatController!";
    }

    //A typical "get all" style method - emulates getting all records from a DB database
    @GetMapping("/all") // GET requests to /boat/all will trigger this method
    public ResponseEntity<List<Boat>> getAllBoats(){

        //ResponeEntity<List<Boat>>
            //== this method returns an HTTP Response that has a JSON list of Boat objects

        //Hardcoded list of boats - imagine we got it from a DB
        List<Boat> boats = List.of(
                new Boat(1, "Sailboat"),
                new Boat(2, "Yacht"),
                new Boat(3, "Canoe"));

        //Look how easy it is to send back a response!
        return ResponseEntity.ok(boats); //200 OK response with the boats as JSON.

    }

    //A typical "get by id" style method -
    //here, we take user input to decide what object gets passed back
    @GetMapping("/byId/{id}") // GET requests to /boat/byId/{id} will trigger this method
    public ResponseEntity<Boat> getBoatById(@PathVariable int id){

        //User input validation (SHOULD BE in the service layer...)
        if(id < 1){
            throw new IllegalArgumentException("Invalid ID! Must be greater than 1");
        }

        //Hardcoded list of boats - imagine we got it from a DB
        List<Boat> boats = List.of(
                new Boat(1, "Sailboat"),
                new Boat(2, "Yacht"),
                new Boat(3, "Canoe"));

        //Find the boat with the matching id
        for(Boat boat : boats){
            if(boat.boatId == id){
                return ResponseEntity.ok(boat); //200 OK response with the boat as JSON.
            }
        }

        //If we get here, no boat was found with that id
        //We use build() if there's no body to be sent back
        return ResponseEntity.notFound().build(); //404 Not Found response
    }

    //A typical "create object" method - we send in a boat object through the Request Body
    @PostMapping //POST requests to /boat will trigger this method
    public ResponseEntity<Boat> createBoat(@RequestBody Boat boat){

        //TODO: user input validations

        //Assume the incoming boat got saved to the DB (we'll just make one here)
        Boat savedBoat = new Boat(500, boat.boatName);

        //201 CREATED with the boat in the response body
        return ResponseEntity.status(201).body(savedBoat);

    }

    /* Note about PUT, PATCH, DELETE

    -PUT will look very similar to POST (@PutMapping and @RequestBody)
    -PATCH will look the same^ but typically only contain the fields you wanna update
        -Some people still do a @RequestBody, other might use @PathVariable

    -DELETE looks similar to GET by id (@PathVariable indicating the record to delete)*/


    //Global Exception Handling -------------------

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<String> handleIllegalArg(Exception e){
        //Send back a 400 "Bad Request" with the Exception message
        return ResponseEntity.badRequest().body(e.getMessage());
    }

}
