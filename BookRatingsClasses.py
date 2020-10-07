# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        
    def print_book(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")


class ReadShelf:
    books = []
    
    def add_book(self, book, review, rating):
        shelved_book = {"book": book, 
                        "review": review,
                        "rating": rating}
        self.books.append(shelved_book)

        
        
class User:
    read_shelf = ReadShelf()
    
    def __init__(self, username, name):
        self.username = username
        self.name = name

    def show_read_books(self):
        print(f"{self.name} has read the following books:")
        for book in self.read_shelf.books:
            print()
            book["book"].print_book()
            print("Review: " + book["review"])
            print("Rating: " + "*"*book["rating"])
            

        

user = User("mitchjohnson12", "Mitch Johnson")
book1 = Book("The Way of Kings", "Brandon Sanderson")
book2 = Book("Brain Rules", "John Medina")
user.read_shelf.add_book(book1, "Dope book", 5)
user.read_shelf.add_book(book2, "Good book", 4)
user.show_read_books()

