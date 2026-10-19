package com.revature.EurekaServer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

/*Why: Every microservice needs a way to find other services without hardcoding URLs.

EUREKA IS THE PHONE BOOK. Services register themselves here,
and look up other services by name.

Registration happens automatically
(when a service with the Eureka dependency + application.properties value runs) */
@SpringBootApplication
@EnableEurekaServer // This is all it takes to turn a Spring Boot app into a discovery server
public class EurekaServerApplication {
	public static void main(String[] args) {
		SpringApplication.run(EurekaServerApplication.class, args);
	}
}