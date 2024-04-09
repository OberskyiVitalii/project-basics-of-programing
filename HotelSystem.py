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
            print('5. Cancel booking')
            print('6. Add to blacklist')
            print('7. Remove from blacklist')
            print('0. Exit\n')

            action = input('Choose your action: ').strip()

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
        name = input('\nEnter hotel name: ').strip()
        for h in self.hotels:
            if name == h.name:
                print(f'Error: Hotel "{name}" already exists!')
                return
        hotel = Hotel.Hotel(name)
        self.hotels.append(hotel)
        print(f'Hotel "{name}" successfully added!')

    def add_room(self):
        hotel_name = input('\nEnter hotel name: ').strip()
        for hotel in self.hotels:
            if hotel_name == hotel.name:
                number = input('Enter room number: ').strip()
                for room in hotel.rooms:
                    if number == room.number:
                        print(f'Error: Room with number {number} already exists!')
                        return
                type = input('Enter room type: ').strip()
                beds = int(input('Enter count of beds: ')).strip()
                amenities = input('Enter amenities (comma-separated): ').split(',').strip()
                max_guests = int(input('Enter maximum number of guests: ')).strip()
                price = float(input('Enter price per hour: ')).strip()
                new_room = Room.Room(number, type, beds, amenities, max_guests, price)
                hotel.add_room(new_room)
                print(f'Room {number} successfully added to {hotel_name} hotel!')
                return
        print(f'Error: Hotel "{hotel_name}" does not exist!')

    def create_customer(self):
        name = input('\nEnter customer name: ').strip()
        email = input('Enter customer email: ').strip()
        phone = input('Enter cutomer number phone: ').strip()

        for customer in self.customers:
            if customer.email == email:
                print(f'Email {email} already bussied!')
            if customer.phone == phone:
                print(f'Error: {phone} already bussied!')

        customer = Customer.Customer(name, email, phone)
        self.customers.append(customer)
        print(f'Customer {name} successfully added!')

    def book_room(self):
        customer_phone = input('\nEnter customer phone number: ').strip()
        customer = self.find_customer(customer_phone)

        if not customer:
            print(f'Error: Customer with {customer_phone} phone number not found!')
            return

        if customer.black_listed:
            print(f'Error: Customer {customer.name} is blacklisted!')
            return

        self.get_hotels()

        hotel_name = input('Enter hotel name: ').strip()
        hotel = self.find_hotel(hotel_name)

        if not any(room.avaible for hotel in self.hotels for room in hotel.rooms):
            print(f'Error: In hotel {hotel_name} has no available rooms!')
            return
        
        if not hotel:
            print(f'Error: Hotel {hotel_name} does not exist!')
            return

        self.get_avaible_room()

        room_number = input('Enter room number: ').strip()
        room = self.find_room(hotel, room_number)
        
        if not room:
            print(f'Error: Room {room_number} does not exist in {hotel_name} hotel!')
            return

        if not room.avaible:
            print(f'Error: Room {room_number} is already booked!')
            return

        check_in = input('Enter check-in date (YYYY.MM.DD HH:MM): ').strip()
        check_out = input('Enter check-out date (YYYY.MM.DD HH:MM): ').strip()
        guests = int(input('Enter count of guests: ')).strip()

        booking = Booking.Booking(room, customer, check_in, check_out, guests)
        
        if self.validate_date(booking) and self.validate_guests(room, guests):
            room.avaible = False
            print(f'Room {room_number} successfully booked by {customer.name}. From {check_in} to {check_out}.')
            customer.booking.append(booking)
            total_price = booking.calculate_price()
            print(f'Total price: {total_price}')
            return booking


    def cancel_booking(self):
        customer_phone = input('\nEnter customer phone number: ').strip()
        customer = self.find_customer(customer_phone)

        if not customer:
            print(f'Error: Customer with {customer_phone} phone number not found!')
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

        choice = input("Enter the number of the booking you want to cancel: ").strip()

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
        customer_phone = input('\nEnter customer phone number to add to black list: ').strip()
        customer = self.find_customer(customer_phone)
        
        if not customer:
            print(f'Error: Customer with {customer_phone} phone number not found!')

        if customer.booking:
            print('Clearing active bookings for customer...')
            customer.booking = []

        customer.black_listed = True
        print(f'Customer {customer.name} has been added to the blacklist.')

    def remove_from_blacklist(self):
        customer_phone = input('\nEnter customer phone number to remove from black list: ').strip()
        customer = self.find_customer(customer_phone)

        if not customer:
            print(f'Error: Customer with {customer_phone} phone number not found!')
            return

            
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
                    amenities_str = ', '.join(room.amenities)
                    print(f'Room number: {room.number}. Name: {room.type}. Beds: {room.beds}. Amenities: {amenities_str}. Max guests: {room.max_guests}')

    def get_all_customers(self):
        for customer in self.customers:
            print(f'{customer.name}. Email: {customer.email}. Phone: {customer.phone}. Banned: {'Banned' if customer.black_listed else 'Not banned'}. Bookings: {len(customer.booking)}')

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

    def find_customer(self, phone):
        for customer in self.customers:
            if customer.phone == phone:
                return customer
        return None

