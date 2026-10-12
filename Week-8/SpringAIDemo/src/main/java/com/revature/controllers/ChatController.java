package com.revature.controllers;

//This is just a typical SpringMVC Controller, but it has LLM chat capabilities!

//Make sure to install Ollama and pull llama3.2:3b (or whatever model you want)
//Don't forget to configure the AI client in application.properties

//LINK TO THE SETUP GUIDE HERE:
//https://docs.google.com/document/d/1-qTezE8u9i54AKsts14TITfgQ1IDIfRh5aG3hJW3FxQ/edit?usp=sharing

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/ai")
public class ChatController {

    private final ChatClient chatClient;

    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    //Generic chat endpoint that answers questions with a personality we define
    @GetMapping("/ask")
    public String ask(@RequestParam String question) {
        return chatClient.prompt()
                .system("You are a helpful assistant that speaks like a pirate")
                .user(question)
                .call()
                .content();
    }

    //Using a Prompt Template to make the {response} more {dynamic} and {personalized}
    @GetMapping("/explain")
    public String explain(@RequestParam String concept, @RequestParam String level) {
        return chatClient.prompt()
                .system("You are a snarky {concept} expert.")
                .user(u -> u.text("Explain {concept} to someone at a {level} level")
                        .param("concept", concept)
                        .param("level", level))
                .call()
                .content();
    }

}
