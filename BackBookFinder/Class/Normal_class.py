from Class.User_class import User_class

class Normal_class(User_class):
    def __init__(self, email, password, name, grade, domaine):
        super().__init__(email, password, name)
        self.grade = grade
        self.domaine = domaine
        self.is_admin = False  # Normal users are not admins by default

    def get_grade(self):
        return self.grade
    
    def get_domaine(self):
        return self.domaine
    
    def set_grade(self, new_grade):
        self.grade = new_grade

    def set_domaine(self, new_domaine):
        self.domaine = new_domaine

    def get_is_admin(self):
        return self.is_admin

    def set_is_admin(self, status):
        raise PermissionError("Normal users cannot change admin status.")
    
    def search_books(self, books):
        """
        Search for books based on the user's grade and domaine.
        Returns a list of books that match the user's criteria.
        """
        return [book for book in books if book.level == self.grade and book.domaine == self.domaine]
