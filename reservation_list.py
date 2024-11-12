from red_black_tree import RedBlackTree
'''
Class to manage seats, extending the Binary Min Heap class
'''

class ReservationList(RedBlackTree):
    def __init__(self):
        super().__init__()

    def search_reservation(self, userID):
        return self.search(userID)

    def make_reservation(self, userID, seatID):
        return self.insert(userID, seatID)

    def remove_reservation(self, userID):
        return self.delete(userID)


    def getAllReservations(self):
        reservation_list = []
        self.inorder_traversal(self.root, reservation_list)
        sorted_list = sorted(reservation_list, key=lambda x: x.key)
        return sorted_list
