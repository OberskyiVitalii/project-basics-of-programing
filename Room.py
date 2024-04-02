class Room:
    def __init__(self, number, type, beds, amenities, max_guests, price):
        self.number = number
        self.type = type
        self.beds = beds
        self.amenities = amenities
        self.max_guests = max_guests
        self.price = price
        self.avaible = True

