package com.revature.clients;

import org.springframework.stereotype.Component;

@Component
public class UserClientFallback implements UserClient {

    @Override
    public Object getUserById(int id){
        return "User service is down! Try again later";
    }

}
