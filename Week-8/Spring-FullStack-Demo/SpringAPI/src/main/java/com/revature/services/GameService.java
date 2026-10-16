package com.revature.services;

import com.revature.jwt.JwtUtil;
import com.revature.models.Game;
import com.revature.models.User;
import com.revature.repositories.GameDAO;
import com.revature.repositories.UserDAO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class GameService {

    //Constructor inject GameDAO and UserDAO
    private final GameDAO gameDAO;
    private final UserDAO userDAO;
    private final JwtUtil jwtUtil;

    @Autowired
    public GameService(GameDAO gameDAO, UserDAO userDAO, JwtUtil jwtUtil) {
        this.gameDAO = gameDAO;
        this.userDAO = userDAO;
        this.jwtUtil = jwtUtil;
    }

    //TODO: get all games


    //Insert game (calls findById of userDAO to get the User object)
    public Game insertGame(Game game, String token){

        //The Auth header is "Bearer <token>", but we just need <token>
        String strippedToken = token.substring(7).trim(); // Remove "Bearer " and trim spaces

        //Get the user by id using id extracted from the JWT
        //TODO: Yes we should validate that the user exists
        User u = userDAO.findById(jwtUtil.extractUserId(strippedToken)).get();

        game.setUser(u);

        return gameDAO.save(game);

    }


}
