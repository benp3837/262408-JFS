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



}
