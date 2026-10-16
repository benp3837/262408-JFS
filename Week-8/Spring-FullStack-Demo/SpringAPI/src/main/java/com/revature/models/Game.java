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

    /* Every Game has a User it belongs to

    fetch - defines whether the dependency gets loaded on app start or when needed
        EAGER - load the dependency on app start
        LAZY - load the dependency when needed (in my experience can cause problems)

    @JoinColumn - define the column in the PK table that this FK references
        name - the name of the column in the FK table (games)
        referencedColumnName - the name of the column in the PK table
            it should also be the name of the field in the PK class (just for ease) */
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "userId")
    private User user;


    //boilerplate ---------------------------

    public Game() {
    }

    public Game(int gameId, String gameTitle, User user) {
        this.gameId = gameId;
        this.gameTitle = gameTitle;
        this.user = user;
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

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public String toString() {
        return "Game{" +
                "gameId=" + gameId +
                ", gameTitle='" + gameTitle + '\'' +
                '}';
    }
}
