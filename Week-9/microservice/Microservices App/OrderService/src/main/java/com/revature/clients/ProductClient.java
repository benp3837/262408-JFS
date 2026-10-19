package com.revature.clients;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

//TODO: ben - kill this to show circuit breaking
//TODO: then kill user service to show lack of circuit breaking (500)

@FeignClient(name = "ProductService", fallback = ProductClientFallback.class)
public interface ProductClient {
    @GetMapping("/products/{id}")
    Object getProductById(@PathVariable int id);
}