package com.revature.models;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component //This makes a class a bean! No need to do it in XML
//Then, to WIRE the beans together, we can put @Autowired over the field, setter, or a constructor
@Scope("prototype") //Taking scope off of the "singleton" default, to allow different instance per bean
public class Cat {

    private int catId;
    private String catColor;
    private String catName;

    //Owner is a DEPENDENCY of Cat
    //With Spring we can "wire beans together" to accomplish DEPENDENCY INJECTION
    //@Autowired <- FIELD INJECTION - BAD (breaking encapsulation, makes our beans harder to test)
    private Owner owner;

    //boilerplate-----

    @Autowired //CONSTRUCTOR INJECTION - BEST PRACTICE for automatic bean wiring
    public Cat(Owner owner) {
        this.owner = owner;
    }

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

    //@Autowired //SETTER INJECTION - Fine practice, used when we have optional dependencies
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
