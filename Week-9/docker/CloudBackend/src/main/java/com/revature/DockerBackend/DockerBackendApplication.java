package com.revature.DockerBackend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/* Without Docker, hosting a Spring Boot app on an EC2 needs:
Java installed
Maven installed
Your source code cloned, AND you have to build it there.

If you’re deploying a different app, or a new version,
or on a different server, you repeat all of that.

With Docker, EC2 just needs Docker.
It doesn’t know or care about anything else.
You docker pull and docker run and you’re done.
And you can do this infinite times (or til your EC2 runs out of disk space).

The main benefits of Docker are portability and scalability. */

@SpringBootApplication
@ComponentScan(basePackages = "com.revature")
@EntityScan(basePackages = "com.revature.models")
@EnableJpaRepositories(basePackages = "com.revature.daos")
public class DockerBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(DockerBackendApplication.class, args);
	}

}
