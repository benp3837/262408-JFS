package com.revature.services;

import com.revature.daos.UserDAO;
import com.revature.models.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserDAO userDAO;

    public User register(User user) {
        user.setRole("user");
        return userDAO.save(user);
    }

    public Optional<User> login(String username, String password) {
        return userDAO.findByUsernameAndPassword(username, password);
    }

    public List<User> getAllUsers() {
        return userDAO.findAll();
    }
}