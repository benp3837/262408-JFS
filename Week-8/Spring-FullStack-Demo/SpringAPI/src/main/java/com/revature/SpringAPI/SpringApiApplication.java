package com.revature.SpringAPI;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@ComponentScan("com.revature") //our bean annotations won't work without this!
@EntityScan("com.revature.models") //Spring Data will look in our models package for DB annotations
@EnableJpaRepositories("com.revature.DAOs") //Lets our DAO class (which extends JPA) become a bean
public class SpringApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringApiApplication.class, args);
	}

}
