package com.revature.repositories;


import com.revature.models.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/* We extended JpaRepository, which takes 2 generics

-The Java Entity that we intend to perform CRUD operations on (User Class)
-The datatype of the PK (as a wrapper Class, so Integer)

With just that information, Spring Data will make a BUNCH of DAO methods for us
This is thanks to a very rich inheritance hierarchy above JpaRepository*/

@Repository //1 of the 4 stereotype annotations that makes a Class a bean
public interface UserDAO extends JpaRepository<User, Integer> {


    //This method will find a User by their username
    //This is called a PROPERTY EXPRESSION
    User findByUsername(String username);

    //TODO: To check for valid login, we'll need a Property Expression...

    /* HOW TO MAKE PROPERTY EXPRESSIONS

     The methods MUST be named like findByX, existsByX, findByXAndY
     "X" and "Y" MUST be exact names of fields in your entity

     Spring Data will do A LOT for us, if we follow its rules
     PropExs are very flexible, feel free to look into them! */


}
