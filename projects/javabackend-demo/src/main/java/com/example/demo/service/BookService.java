package com.example.demo.service;

import com.example.demo.entity.Book;
import com.example.demo.mapper.BookMapper;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BookService {

    private final BookMapper bookMapper;

    public BookService(BookMapper bookMapper) {
        this.bookMapper = bookMapper;
    }

    public List<Book> list() {
        return bookMapper.findAll();
    }

    public Book get(Long id) {
        Book book = bookMapper.findById(id);
        if (book == null) {
            throw new IllegalArgumentException("book not found: " + id);
        }
        return book;
    }
}
