package com.revature.services;

import com.revature.repositories.GameDAO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class GameService {

    //Constructor inject GameDAO
    private final GameDAO gameDAO;

    @Autowired
    public GameService(GameDAO gameDAO) {
        this.gameDAO = gameDAO;
    }
}
