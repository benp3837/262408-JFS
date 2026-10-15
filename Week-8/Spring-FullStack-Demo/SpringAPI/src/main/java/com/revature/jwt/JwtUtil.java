package com.revature.jwt;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;

//This Class is responsible for generating and validating JWTs

@Component
public class JwtUtil {

    // Every JWT will have a secret key that helps it be unique
    private final Key key = Keys.secretKeyFor(SignatureAlgorithm.HS256);
    private final long EXPIRATION = 1000 * 60 * 60 * 8; // 8 hours

    // Generates a signed JWT containing the username, role, and userId as claims
    public String generateToken(String username, String role, int userId) {
        return Jwts.builder()
                .setSubject(username) //who the user is
                .claim("role", "ROLE_" + role) //claims are just other pieces of info
                .claim("userId", userId)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION))
                .signWith(key) //the "signature", which identifies the JWT itself
                .compact();
    }

    //Extraction methods -----
        //These help us "extract" info from the JWTs

    // Extracts the username (subject) from a JWT
    public String extractUsername(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    // Extracts the role custom claim from a JWT
    public String extractRole(String token) {
        return (String) Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .get("role");
    }

    // Extracts the userId custom claim from a JWT
    public int extractUserId(String token) {
        return (int) Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .get("userId");
    }

    // Returns true if the token is valid and not expired — false if tampered with or expired
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder().setSigningKey(key).build().parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
