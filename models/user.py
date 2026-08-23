class User:
    def __init__(self, user_id, passport, username, email, password):
        self.user_id = user_id
        self.passport = passport
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return f"{self.username} ({self.email})"
