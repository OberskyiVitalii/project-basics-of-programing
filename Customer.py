class Customer:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.black_listed = False
        self.booking = []