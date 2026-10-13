package com.revature.controllers;

import com.revature.daos.AuthorDAO;
import com.revature.daos.BookDAO;
import com.revature.models.Author;
import com.revature.models.Book;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.*;
import org.springframework.stereotype.Controller;

import java.util.List;
import java.util.NoSuchElementException;

@Controller
public class BookController {

    //Constructor inject and autowire the DAOs

    private final BookDAO bookDAO;
    private final AuthorDAO authorDAO;

    @Autowired
    public BookController(BookDAO bookDAO, AuthorDAO authorDAO) {
        this.bookDAO = bookDAO;
        this.authorDAO = authorDAO;
    }

    //A record in Java is a type of class we can use to quickly to model data.
    //It automatically generates boilerplate code like constructors, getters, equals(), hashCode(), and toString() methods.
    record BookInput(String name, int pageCount, int authorId) {}

    //GraphQL query and mutation mappings ------------
        //query - used to fetch data from the server (read-only stuff)
        //mutation - used to modify data on the server (create, update, delete)

    @QueryMapping
    public List<Book> getAllBooks() {
        return bookDAO.findAll();
    }

    @QueryMapping
    public Book bookById(@Argument int bookId) {
        return bookDAO.findById(bookId)
                .orElseThrow(() -> new NoSuchElementException("Book with ID " + bookId + " not found."));
    }

    @MutationMapping
    public Book createBook(@Argument BookInput bookInput) {
        Author a = authorDAO.findById(bookInput.authorId())
                .orElseThrow(() -> new NoSuchElementException("Author with ID " + bookInput.authorId() + " not found."));
        Book b = new Book(bookInput.name(), bookInput.pageCount(), a);
        return bookDAO.save(b);
    }

    /*This method is used to resolve the author field of a Book object when queried in GraphQL.

    "resolve"? when you query a Book and want to get the Author details,
    this method fetches the Author from the DB based on the Book's authorId.*/
    @SchemaMapping
    public Author author(Book book) {
        return authorDAO.findById(book.getAuthor().getAuthorId()).orElse(null);
    }
}