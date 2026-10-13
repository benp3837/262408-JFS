package com.revature.models;

public class Cat {

    private int catId;
    private String catColor;
    private String catName;

    //Owner is a DEPENDENCY of Cat
    //With Spring we can "wire beans together" to accomplish DEPENDENCY INJECTION
    private Owner owner;

    //boilerplate-----

    public Cat() {
    }

    public Cat(int catId, String catColor, String catName, Owner owner) {
        this.catId = catId;
        this.catColor = catColor;
        this.catName = catName;
        this.owner = owner;
    }

    public int getCatId() {
        return catId;
    }

    public void setCatId(int catId) {
        this.catId = catId;
    }

    public String getCatColor() {
        return catColor;
    }

    public void setCatColor(String catColor) {
        this.catColor = catColor;
    }

    public String getCatName() {
        return catName;
    }

    public void setCatName(String catName) {
        this.catName = catName;
    }

    public Owner getOwner() {
        return owner;
    }

    public void setOwner(Owner owner) {
        this.owner = owner;
    }

    @Override
    public String toString() {
        return "Cat{" +
                "catId=" + catId +
                ", catColor='" + catColor + '\'' +
                ", catName='" + catName + '\'' +
                ", owner=" + owner +
                '}';
    }
}
