class Book_class:
    def __init__(self, isbn, title, author, year, grade, domaine, directory):
        self.isbn = isbn        
        self.title = title
        self.author = author
        self.year = year
        self.grade = grade
        self.domaine = domaine
        self.directory = directory

    def get_isbn(self):
        return self.isbn

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_year(self):
        return self.year

    def get_grade(self):
        return self.grade

    def get_domaine(self):
        return self.domaine

    def get_directory(self):
        return self.directory
    
    def __str__(self):
        return f"{self.title} by {self.author}, {self.year} (ISBN: {self.isbn})"

    def __repr__(self):
        return f"Book_class({self.title!r}, {self.author!r}, {self.year!r}, {self.isbn!r})"
    
    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "grade": self.grade,
            "domaine": self.domaine,
            "directory": self.directory
        }