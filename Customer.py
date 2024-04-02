class Customer:
    def __init__(self, name, nick_name, email, phone):
        self.name = name
        self.nick_name = nick_name
        self.email = email
        self.phone = phone
        self.black_listed = False
        self.booking = []