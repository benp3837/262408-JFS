package com.revature.HelloSpring;

import com.revature.models.Cat;
import com.revature.models.Owner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

@SpringBootApplication
public class HelloSpringApplication {

	public static void main(String[] args) {
		SpringApplication.run(HelloSpringApplication.class, args);


		//Before we can see the Beans in action, we need to create our ApplicationContext object
		//ApplicationContext is the "Spring Container" that we'll use
			//A Spring Container manages and injects beans
		ApplicationContext ac =
				new ClassPathXmlApplicationContext("applicationContext.xml");

		//First, lets just view all the beans in the Spring Container
		String[] beanNames = ac.getBeanDefinitionNames();

		//owner, cat
		for(String beanName : beanNames){
			System.out.println(beanName);
		}

		//Now, let's instantiate some Owners and Cats to see DEPENDENCY INJECTION at work

		Owner owner = ac.getBean(Owner.class);
		System.out.println(owner); //nothing crazy, but we do see the default value

		Cat cat = ac.getBean(Cat.class);
		System.out.println(cat);

		//FASCINATING^ We see that an Owner was instantiated for us
		//Thank you: Dependency Injection, Spring Beans, & Spring Container



	}

}
