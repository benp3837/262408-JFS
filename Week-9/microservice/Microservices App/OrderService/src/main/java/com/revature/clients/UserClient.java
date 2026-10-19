package com.revature.clients;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

/* Feign Client: Spring generates the HTTP implementation for us at runtime
 "UserService" = spring.application.name of UserService app in Eureka
 No hardcoded URL!! Eureka resolves the address dynamically. Very cool */
@FeignClient(name = "UserService", fallback = UserClientFallback.class)
public interface UserClient {
    @GetMapping("/users/{id}")
    Object getUserById(@PathVariable int id);
}