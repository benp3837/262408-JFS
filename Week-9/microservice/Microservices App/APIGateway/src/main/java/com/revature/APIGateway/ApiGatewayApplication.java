package com.revature.APIGateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/* Why: The API gateway is a FRONT CONTROLLER!
It figures out where to send each request so we don't need to keep track of it.

Without it, clients would need to know five different ports to use this app.

The gateway is the single front door, providing one port and one URL

It also enables LOAD BALANCING: if you ran two instances of User Service,
the gateway would distribute traffic between them automatically
(Load balancing is more visible if we hosted this app on the cloud)

Check application.properties, no real source code in this Service, mostly configs*/

@SpringBootApplication
public class ApiGatewayApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiGatewayApplication.class, args);
	}

}
