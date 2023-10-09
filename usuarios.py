class Usuario:
    def __init__(self, name, username, age, email, uid, password):
        self.name = name
        self.username = username
        self.age = age
        self.email = email
        self.uid = uid
        self.password = password

    def __str__(self):
        return f"Name: {self.name}, Username: {self.username} ,Age: {self.age}, Email: {self.email}, UID: {self.uid}, Password: {self.password}"
