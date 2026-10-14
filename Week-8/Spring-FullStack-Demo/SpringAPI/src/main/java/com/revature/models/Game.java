package com.revature.models;

//Again, no @Component, it'll be a DB @Entity

import jakarta.persistence.*;

@Entity // Tells Spring to make this Class a DB table
@Table(name = "games") //Set the table name to "games"
public class Game {

    @Id //Tell Spring that this is the Primary Key
    @GeneratedValue(strategy = GenerationType.IDENTITY) //Make the PK auto-increment
    private int gameId;

    @Column(nullable = false) //Games must have a title
    private String gameTitle;

    //Add a field for user (the user the game belongs to)
    //THIS IS THE FK! Games will have a many-to-one relationship with Users.

    /*

     */
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "userId")
    private User user;


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
