package com.revature.models;

import org.springframework.context.annotation.Configuration;

@Configuration
public class BeanConfigClassExample {

    //NOTE: THIS CLASS ACCOMPLISHES THE SAME THING AS OUR applicationContext.xml
    //(It registers and wires beans)
    //This is just the class-based way to do it!

//    @Bean
//    public ___ _____(){
//        return new ___();
//    }
//
//    @Bean
//    public ___ ___(){
//        return new ____();
//    }

    //Then we'd make an ApplicationContext in main() like this:

    //ApplicationContext ac = new AnnotationConfigApplicationContext(Classname.class);

}
