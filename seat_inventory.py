from binary_min_heap import BinaryMinHeap
'''
Class to manage seats inheriting the Binary Min Heap
Supports initialization, check empty, adding seats, get first available seat and assign seat and get seat count functions 
'''

class SeatInventory(BinaryMinHeap):
    def __init__(self):
        super().__init__()

    def is_empty_seats(self):
        return self.is_empty()

    def add_seats(self, seat_number):
        return self.insert(seat_number)

    def get_first_available_seat(self):
        return self.get_min()

    def assign_seat(self):
        return self.delete_min()

    def get_seat_count(self):
        return self.get_size()
