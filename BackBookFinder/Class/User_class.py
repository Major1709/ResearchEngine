class User_class:
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        self.is_logged_in = False
        self.is_admin = False

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password
    
    def get_name(self):
        return self.name
    
    def get_is_logged_in(self):
        return self.is_logged_in
    
    def get_is_admin(self):
        return self.is_admin

    def set_email(self, new_email):
        self.email = new_email

    def set_password(self, new_password):
        self.password = new_password
    
    def set_name(self, new_name):
        self.name = new_name
    
    def set_is_logged_in(self, status):
        self.is_logged_in = status

    def set_is_admin(self, status):
        self.is_admin = status