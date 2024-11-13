from red_black_tree import RedBlackTree
'''
Class to manage seats, extending the Binary Min Heap class
Supports initialization, search reservation, make reservation, remove reservation, get all reservations functions
'''

class ReservationList(RedBlackTree):
    def __init__(self):
        super().__init__()

    def search_reservation(self, userID):
        return self.search(userID)

    def make_reservation(self, userID, seatID):
        return self.insert((userID, seatID))

    def remove_reservation(self, userID):
        return self.delete(userID)

    def get_all_reservations(self):
        reservation_list = []
        self.inorder_traversal(self.root, reservation_list)
        sorted_list = sorted(reservation_list, key=lambda x: x.value)
        return sorted_list
