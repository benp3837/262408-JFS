package com.revature.CloudBackend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@ComponentScan(basePackages = "com.revature")
@EntityScan(basePackages = "com.revature.models")
@EnableJpaRepositories(basePackages = "com.revature.daos")
public class CloudBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(CloudBackendApplication.class, args);
	}

}
