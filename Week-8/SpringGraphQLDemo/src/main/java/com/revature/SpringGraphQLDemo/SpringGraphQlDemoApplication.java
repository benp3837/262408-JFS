package com.revature.SpringGraphQLDemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@ComponentScan("com.revature")
@EntityScan("com.revature.models")
@EnableJpaRepositories("com.revature.daos")
public class SpringGraphQlDemoApplication {

	/* GraphQL adopts a completely different request structure from RESTful APIs

	-The goal is to allow the client to request exactly what data they want,
	and the server will return only that data.

	-This is different from RESTful APIs,
	where the server defines the exact structure of the response.
		-RESTful APIs are prone to OVERSHARING. GraphQL avoids that entirely.

	And remember, your projects are RESTful APIs, not GraphQL APIs.
	This stuff is good to know since you may see it.
	But don't try to emulate this in your projects
	 */


	public static void main(String[] args) {
		SpringApplication.run(SpringGraphQlDemoApplication.class, args);
	}

}
