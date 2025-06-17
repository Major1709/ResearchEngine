import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Class.Book_class import Book_class


def list_books():
    with open("/home/toma/Documents/projet pres/data.json", "r", encoding="utf-8") as f:
        books = json.load(f)

    Books = []
    for i, book in enumerate(books, start=1):
        bk = Book_class(
            isbn=book['isbn'],
            title=book['title'],
            author=book['author'],
            year=book['year'],
            grade=book['grade'],  # Utilise .get au cas où certains champs manquent
            domaine=book['domaine'],
            directory=book['directory']
        )
        Books.append(bk)
    return Books


def filtre_books(query, books):
    results = []
    for q in query:
        for book in books:
            if (q == book.get_isbn()):
                results.append(book)
    return results
