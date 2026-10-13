package com.revature.models;

//This won't be a bean, it'll what's called a POJO (plain ol' java object)
public class Boat {

    public int boatId;
    public String boatName;

    //boilerplate------

    public Boat() {
    }

    public Boat(int boatId, String boatName) {
        this.boatId = boatId;
        this.boatName = boatName;
    }

    @Override
    public String toString() {
        return "Boat{" +
                "boatId=" + boatId +
                ", boatName='" + boatName + '\'' +
                '}';
    }


}
