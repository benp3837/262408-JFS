package com.revature.clients;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

//ben killed this to show circuit breaking

//Circuit breaker - a pattern where a fallback invokes if the main service is down


//TODO: then kill user service to show lack of circuit breaking (500)

@FeignClient(name = "ProductService", fallback = ProductClientFallback.class)
public interface ProductClient {
    @GetMapping("/products/{id}")
    Object getProductById(@PathVariable int id);
}