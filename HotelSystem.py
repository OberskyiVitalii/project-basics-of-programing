import Hotel
import Room
import Customer
import Booking

from datetime import datetime

class HotelSystem:
    def __init__(self):
        self.hotels = []
        self.customers = []
        self.main_menu()

    def main_menu(self):
        while True:
            print('\nHotel system')
            print('1. Create new hotel')
            print('2. Add room to hotel')
            print('3. Create customer')
            print('4. Book room')
            print('5. Cancle booking')
            print('6. Add to blacklist')
            print('7. Remove from blacklist')
            print('0. Exit\n')

            action = input('Choose your action: ')

            if action == '1':
                self.get_hotels()
                self.create_hotel()
            elif action == '2':
                self.get_hotels()
                self.add_room()
            elif action == '3':
                self.get_all_customers()
                self.create_customer()
            elif action == '4':
                self.get_all_customers()
                self.book_room()
            elif action == '5':
                self.cancel_booking()
            elif action == '6':
                self.get_all_customers()
                self.add_to_blacklist()
            elif action == '7':
                self.get_all_customers()
                self.remove_from_blacklist()
            elif action == '0':
                print('Exiting...')
                break
            else:
                print('Error: Incorrect action was entered!')

    def create_hotel(self):
        name = input('\nEnter hotel name: ')
        for h in self.hotels:
            if name == h.name:
                print(f'Error: Hotel "{name}" already exists!')
                return
        hotel = Hotel.Hotel(name)
        self.hotels.append(hotel)
        print(f'Hotel "{name}" successfully added!')

    def add_room(self):
        hotel_name = input('\nEnter hotel name: ')
        for hotel in self.hotels:
            if hotel_name == hotel.name:
                number = input('Enter room number: ')
                for room in hotel.rooms:
                    if number == room.number:
                        print(f'Error: Room with number {number} already exists!')
                        return
                type = input('Enter room type: ')
                beds = int(input('Enter count of beds: '))
                amenities = input('Enter amenities (comma-separated): ').split(',')
                max_guests = int(input('Enter maximum number of guests: '))
                price = float(input('Enter price per night: '))
                new_room = Room.Room(number, type, beds, amenities, max_guests, price)
                hotel.add_room(new_room)
                print(f'Room {number} successfully added to {hotel_name} hotel!')
                return
        print(f'Error: Hotel "{hotel_name}" does not exist!')

    def create_customer(self):
        name = input('\nEnter customer name: ')
        nick_name = input('Enter nick name: ')
        for customer in self.customers:
            if customer.nick_name == nick_name:
                print(f'Error: {nick_name} already bussied!')
        email = input('Enter customer email: ')
        phone = input('Enter cutomer number phone: ')
        customer = Customer.Customer(name, nick_name, email, phone)
        self.customers.append(customer)
        print(f'Customer {name} successfully added!')

    def book_room(self):
        customer_nick_name = input('\nEnter customer nick name: ')
        customer = self.find_customer(customer_nick_name)

        if not customer:
            print(f'Error: Customer {customer.name} does not exist!')
            return

        if customer.black_listed:
            print(f'Error: Customer {customer.name} is blacklisted!')
            return

        self.get_hotels()

        hotel_name = input('Enter hotel name: ')
        hotel = self.find_hotel(hotel_name)
        
        if not hotel:
            print(f'Error: Hotel {hotel_name} does not exist!')
            return

        self.get_avaible_room()

        room_number = input('Enter room number: ')
        room = self.find_room(hotel, room_number)
        
        if not room:
            print(f'Error: Room {room_number} does not exist in {hotel_name} hotel!')
            return

        if not room.avaible:
            print(f'Error: Room {room_number} is already booked!')
            return

        check_in = input('Enter check-in date (YYYY.MM.DD HH:MM): ')
        check_out = input('Enter check-out date (YYYY.MM.DD HH:MM): ')
        guests = int(input('Enter count of guests: '))

        booking = Booking.Booking(room, customer, check_in, check_out, guests)
        
        if self.validate_date(booking) and self.validate_guests(room, guests):
            room.avaible = False
            print(f'Room {room_number} successfully booked by {customer.name}. From {check_in} to {check_out}.')
            customer.booking.append(booking)
            return booking


    def cancel_booking(self):
        customer_nick_name = input('\nEnter customer nick name: ')
        customer = self.find_customer(customer_nick_name)

        if not customer:
            print(f'Error: Customer {customer_nick_name} does not exist!')
            return

        if not customer.booking:
            print(f'Error: Customer {customer.name} does not have any bookings!')
            return

        if customer.black_listed:
            print(f'Error: Customer {customer.name} is blacklisted!')
            return

        print(f'Bookings for {customer.name}:')
        for i, booking in enumerate(customer.booking):
            print(f"{i + 1}. Room: {booking.room.number}, Check-in: {booking.check_in}, Check-out: {booking.check_out}, Guests: {booking.guests}")

        choice = input("Enter the number of the booking you want to cancel: ")

        if not choice.isdigit():
            print("Error: Invalid choice! Please enter a valid number.")
            return

        choice = int(choice)
        if choice < 1 or choice > len(customer.booking):
            print("Error: Invalid choice! Please enter a valid number.")
            return

        booking_to_cancel = customer.booking.pop(choice - 1)
        print(f'Booking {customer.name}: {booking_to_cancel.room.number} - {booking_to_cancel.room.type}. From {booking_to_cancel.check_in} to {booking_to_cancel.check_out}. Guests: {booking_to_cancel.guests}')

        booking_to_cancel.room.avaible = True

        print(f'Booking successfully canceled!')

    def add_to_blacklist(self):
        customer_nick_name = input('\nEnter customer nick name to add to black list: ')
        customer = self.find_customer(customer_nick_name)
        
        if not customer:
            print(f'Error: Customer with nick name {customer_nick_name} not found.')

        if customer.booking:
            print('Clearing active bookings for customer...')
            customer.booking = []

        customer.black_listed = True
        print(f'Customer {customer.name} has been added to the blacklist.')

    def remove_from_blacklist(self):
        customer_nick_name = input('\nEnter customer nick name to remove from black list: ')
        customer = self.find_customer(customer_nick_name)

        if not customer:
            print(f'Error: Customer with nick name {customer_nick_name} not found.')
            
        customer.black_listed = False
        print(f'Customer {customer.name} has been removed from the blacklist.')


    def get_hotels(self):
        print("\nList of Hotels:")
        for hotel in self.hotels:
            available_rooms = sum(1 for room in hotel.rooms if room.avaible)
            print(f'Hotel "{hotel.name}": Total rooms - {len(hotel.rooms)}, Available rooms - {available_rooms}')

    def get_avaible_room(self):
        print('\nAvaible rooms: ')
        for hotel in self.hotels:
            for room in hotel.rooms:
                if room.avaible:
                    print(f'Name: {room.number}. Nick name: {room.type}. Beds: {room.beds}. Amenities: {room.amenities.__str__()}')

    def get_all_customers(self):
        for customer in self.customers:
            print(f'{customer.name} - {customer.nick_name}. Email: {customer.email}. Phone: {customer.phone}. Banned {'Banned' if customer.black_listed else 'Not banned'}. Bookings: {len(customer.booking)}')

    def validate_date(self, booking):
        now = datetime.now()
        check_in_datetime = datetime.strptime(booking.check_in.strftime('%Y.%m.%d %H:%M'), '%Y.%m.%d %H:%M')
        
        if check_in_datetime < now:
            print('Error: Check-in date cannot be in the past!')
            return False

        if check_in_datetime > datetime.strptime(booking.check_out.strftime('%Y.%m.%d %H:%M'), '%Y.%m.%d %H:%M'):
            print('Error: Check-in date must be before check-out date!')
            return False
        
        for previous_booking in booking.customer.booking:
            previous_booking_end = datetime.strptime(previous_booking.check_out.strftime('%Y.%m.%d %H:%M'), '%Y.%m.%d %H:%M')
            if check_in_datetime < previous_booking_end:
                print("Error: New booking must start after the end of the previous booking!")
                return False
        
        return True

    def validate_guests(self, room, guests):
        if guests > room.max_guests:
            print(f'Error: The number of guests cannot exceed the maximum capacity of {room.max_guests}.')
            return False
        return True

    def find_hotel(self, name):
        for hotel in self.hotels:
            if hotel.name == name:
                return hotel
        return None
    
    def find_room(self, hotel, number):
        for room in hotel.rooms:
            if room.number == number:
                return room
        return None

    def find_customer(self, nick_name):
        for customer in self.customers:
            if customer.nick_name == nick_name:
                return customer
        return None

