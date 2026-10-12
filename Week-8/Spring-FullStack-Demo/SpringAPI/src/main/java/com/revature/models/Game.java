package com.revature.models;

//TODO: No Spring Data annotations here yet. We'll do it together for practice

public class Game {

    private int gameId;
    private String gameTitle;

    //TODO: add a field for user (the user the game belongs to)


    //boilerplate ---------------------------

    public Game() {
    }

    public Game(int gameId, String gameTitle) {
        this.gameId = gameId;
        this.gameTitle = gameTitle;
    }

    public int getGameId() {
        return gameId;
    }

    public void setGameId(int gameId) {
        this.gameId = gameId;
    }

    public String getGameTitle() {
        return gameTitle;
    }

    public void setGameTitle(String gameTitle) {
        this.gameTitle = gameTitle;
    }

    @Override
    public String toString() {
        return "Game{" +
                "gameId=" + gameId +
                ", gameTitle='" + gameTitle + '\'' +
                '}';
    }
}
