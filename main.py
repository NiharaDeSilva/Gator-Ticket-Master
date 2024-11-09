import sys
import reservation_management
import binary_heap


seats = binary_heap.BinaryHeap()
reservation = reservation_management.RedBlackTree()
waitlist = binary_heap.BinaryHeap()

seat_count=0
def initialize(count):
    for i in range(1, count+1):
        seats.insert(i)
    print(count, "Seats are made available for reservation")
    global seat_count
    seat_count = count



def reserve(userID, userPriority):
    if not seats.is_empty():
        seatID = seats.get_min()
        reservation.insert(userID, seatID)
        seats.delete_min()
    # else:
        # create a record in waitlist, with user priority
    print("User ", userID, "reserved seat", seatID)

def available():
    print ("Total Seats Available :", seats.get_size(), " Waitlist" )

def cancel(seatID, userID):
    # if not waitlist.is_empty():
    reservation.delete(userID)
    seats.insert(seatID)
        # new_userID = waitlist.get_min()
        # reservation.insert(new_userID, seatID)
    # else:
    #     reservation.delete(userID)
    print("User ", userID, "canceled their reservation")


# If the user wants to exit the waitlist, given that he was never assigned a seat
# def exitWaitList():
#
#


#Modify the user priority only if he is in the waitlist heap. Update the heap with this modification
# def updatePriority(userID, userPriority):
#
#
#

#Add seats to the available seat list. The new seat numbers should follow the previously available range.
def addSeats(count):
    global seat_count
    total = seat_count + count+1
    for i in range(seat_count, total):
        seats.insert(i)
    seat_count = total


def getAllReservations():
    reservation_list = []
    reservation._inorder_traversal(reservation.root, reservation_list)
    reservation_list.sort(key=lambda x: x.key)
    return reservation_list

def printReservations():
    reservation_list = getAllReservations()
    for reservation in reservation_list:
        print(f"Seat {reservation.key}, User {reservation.value}")

#
def releaseSeats(userID1, userID2):
    #seats reservaed users
    for userID in range(userID1, userID2):
        reservation.delete(userID)
    #Users in the waitlist



def quit():
    print("Program Terminated")
    sys.exit(0)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initialize(10)
    available()
    reserve(8, 1)
    reserve(4, 3)
    reserve(5, 2)
    available()
    cancel(2, 4)
    reserve(1, 1)
    available()
    # getAllReservations()
    printReservations()
    reserve(3, 1)
    reserve(2, 2)
    reserve(6, 3)
    available()
    cancel(1, 1)
    cancel(3, 5)
    available()
    reserve(11, 1)
    reserve(9, 2)
    addSeats(2)
    reserve(7, 2)
    cancel(1, 8)
    available()
    releaseSeats(8, 10)
    printReservations()
    quit()
