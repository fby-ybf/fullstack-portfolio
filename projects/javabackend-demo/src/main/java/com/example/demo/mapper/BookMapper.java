package com.example.demo.mapper;

import com.example.demo.entity.Book;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface BookMapper {

    @Select("SELECT id, title, author FROM book WHERE id = #{id}")
    Book findById(@Param("id") Long id);

    @Select("SELECT id, title, author FROM book ORDER BY id")
    List<Book> findAll();
}
