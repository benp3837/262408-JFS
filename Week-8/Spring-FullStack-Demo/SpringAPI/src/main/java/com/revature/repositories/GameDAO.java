package com.revature.repositories;

import com.revature.models.Game;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository // make this class a bean
public interface GameDAO extends JpaRepository<Game, Integer> {



}
