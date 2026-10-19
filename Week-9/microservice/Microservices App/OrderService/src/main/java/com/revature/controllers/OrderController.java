package com.revature.controllers;

import com.revature.clients.ProductClient;
import com.revature.clients.UserClient;
import com.revature.daos.OrderDAO;
import com.revature.models.Order;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private OrderDAO orderDAO;

    // Injected just like any Spring bean. Feign handles the HTTP magic underneath
    @Autowired
    private UserClient userClient;

    @Autowired
    private ProductClient productClient;

    @GetMapping
    public ResponseEntity<List<Order>> getAllOrders() {
        return ResponseEntity.ok(orderDAO.findAll());
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> createOrder(@RequestBody Order order) {
        orderDAO.save(order);

        // These look like method calls but they're HTTP requests to other services
        // If a service is down the fallback fires. no exception, no 500 status code
        Object user = userClient.getUserById(order.getUserId());
        Object product = productClient.getProductById(order.getProductId());

        // Crafty way to return multiple objects. Claude gave me this idea
        Map<String, Object> response = new HashMap<>();
        response.put("order", order);
        response.put("user", user);
        response.put("product", product);

        return ResponseEntity.status(201).body(response);
    }
}