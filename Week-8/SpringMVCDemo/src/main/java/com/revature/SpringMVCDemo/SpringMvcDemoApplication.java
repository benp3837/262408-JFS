package com.revature.SpringMVCDemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan("com.revature") //SKIP THE XML!!! Tell Spring the beans live in com.revature
public class SpringMvcDemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringMvcDemoApplication.class, args);
	}

}
