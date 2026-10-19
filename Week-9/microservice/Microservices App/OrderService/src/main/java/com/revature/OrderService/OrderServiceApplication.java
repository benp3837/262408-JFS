package com.revature.OrderService;

import feign.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.persistence.autoconfigure.EntityScan;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/* Why: This is the most interesting one imo.

It manages its own data, AND orchestrates calls to other services.
It has our examples of Feign, load balancing, and circuit breaking.

It demonstrates the core MSA challenge: how do services talk to each other reliably?
"Reliably" including graceful failure instead of 500s */
@SpringBootApplication
@ComponentScan("com.revature")
@EntityScan("com.revature.models")
@EnableJpaRepositories("com.revature.daos")
@EnableFeignClients(basePackages = "com.revature.clients") // Activates Feign Client scanning
public class OrderServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(OrderServiceApplication.class, args);
	}

}
