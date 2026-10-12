package com.revature.controllers;

import com.revature.models.Game;
import com.revature.models.LoginDTO;
import com.revature.services.AuthService;
import com.revature.services.GameService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

//Check AuthController for better commenting
@RestController
@RequestMapping("/games")
@CrossOrigin(origins = {"http://localhost:5173", "http://localhost:4200"}, allowedHeaders = "*")
public class GameController {

    //Inject the GameService with Constructor Injection
    //TODO: more on this later, just wanted to show this pattern early
    private final GameService gameService;

    @Autowired
    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    //Get a list of games from the DB (GET Requests to /games will get routed here)
    @GetMapping
    public ResponseEntity<?> getAllGames() {

        //TODO: Call to GameService would be here, hardcoding for now
        List<Game> games = new ArrayList<Game>();

        games.add(new Game(1, "Hollow Knight"));
        games.add(new Game(2, "Halo 3"));
        games.add(new Game(3, "Duck Game"));

        //ok() is a shorthand way to say status(200) btw
        return ResponseEntity.ok().body(games);

    }


    //TODO: other stuff related to games

}
