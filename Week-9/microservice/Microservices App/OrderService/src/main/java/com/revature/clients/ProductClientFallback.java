package com.revature.clients;

import org.springframework.stereotype.Component;

@Component
public class ProductClientFallback implements ProductClient {
    @Override
    public Object getProductById(int id) {
        return "Product service is currently unavailable — using fallback";
    }
}