package com.revature.aspects;

//This Class is an @Aspect - it will handle and generate ALL logging logic in one place

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
@Aspect
public class LoggingAspect {

    //A Logger object that will ONLY exist here (not in ever class we're logging)
    private static Logger logger = LoggerFactory.getLogger(LoggingAspect.class);

    //In an Aspect, methods are called ADVICES.
    //Each advice will be responsible for logging certain parts of the app

    //This advice will log EVERY method call in the service layer
    @Before("within(com.revature.services.*)")
    public void logServiceMethods(JoinPoint jp){
        //getTarget() returns the object(class)
        //getSignature() returns the method signature
        logger.info(jp.getTarget() + " is calling: " + jp.getSignature().getName());
    }

    /*This Advice will run AFTER successfully returning a value

     //TODO: more notes

     "After the execution of any method in any class that has any args inside the service layer, generate a log"
     */
    @AfterReturning(pointcut="execution(* com.revature.services.*.*(..))", returning="result")
    public void logSuccessfulServiceMethods(JoinPoint jp, Object result){
        //TODO: write the log
    }




}
