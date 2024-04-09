from datetime import datetime

class Booking:
    def __init__(self, room, customer, check_in, check_out, guests):
        self.room = room
        self.customer = customer
        self.check_in = datetime.strptime(check_in, '%Y.%m.%d %H:%M')
        self.check_out = datetime.strptime(check_out, '%Y.%m.%d %H:%M')
        self.guests = guests

    def calculate_price(self):
        hours = (self.check_out - self.check_in).total_seconds() / 3600
        total_price = self.room.price * hours
        return total_price