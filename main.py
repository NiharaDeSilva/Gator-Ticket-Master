import sys
import reservation_management
import binary_heap


seats = binary_heap.BinaryHeap()
reservation = reservation_management.RedBlackTree()
waitlist = binary_heap.BinaryHeap()

seat_count=0
def initialize(count):
    if count > 0:
        for i in range(1, count+1):
            seats.insert(i)
        print(count, "Seats are made available for reservation")
        global seat_count
        seat_count = count
    else:
        print("Invalid input. Please provide a valid number of seats.")


def reserve(userID, userPriority):
    if not seats.is_empty():
        seatID = seats.get_min()
        reservation.insert(userID, seatID)
        seats.delete_min()
        print(f"User {userID} reserved seat {seatID[0]}")
    else:
        waitlist.insert(userID, userPriority)     # create a record in waitlist, with user priority
        print(f"User {userID} is added to the waiting list")


def available():
    print (f"Total Seats Available : {seats.get_size()} Waitlist :{waitlist.get_size()}" )

def cancel(seatID, userID):
    userReservation = reservation.search(userID)
    if (userReservation.value != None) and (userReservation.key[0] == seatID):
        if waitlist.is_empty():
            reservation.delete(userID)
            seats.insert(seatID)
            print(f"User {userID} canceled their reservation")
        else:
            reservation.delete(userID)
            new_userID = sortWaitlitsbyPriority()[0]
            reservation.insert(new_userID[0], seatID)
            waitlist.delete(new_userID[0])
            print(f"User {userID} canceled their reservation")
            print(f"User {new_userID[0]} reserved seat {seatID}")
    elif ((userReservation.value != None) and (userReservation.key[0] != seatID)):
        print(f"User {userID} has no reservation for seat {seatID} to cancel")
    else:
        print(f"User {userID} has no reservation to cancel")

# If the user wants to exit the waitlist, given that he was never assigned a seat
def exitWaitList(userID):
    if waitlist.search(userID) != -1:
        waitlist.delete(userID)
        print(f"User {userID} is removed from the waiting list")
    else:
        print(f"User {userID} is not in waitlist")

# Modify the user priority only if he is in the waitlist heap. Update the heap with this modification
def updatePriority(userID, userPriority):
    if waitlist.search(userID) != -1:
        waitlist.update(userID, userPriority)
        print(f"User {userID} priority has been updated to {userPriority}")
    else:
        #If the user is not in the waiting list
        print(f"User {userID} priority is not updated")


def sortWaitlitsbyPriority():
    list = waitlist.get_items()
    sortedList = sorted(list, key=lambda x: x[1], reverse=True)
    return sortedList


#Add seats to the available seat list. The new seat numbers should follow the previously available range.
def addSeats(count):
    if count > 0:
        global seat_count
        total = seat_count + count
        for i in range(seat_count+1, total+1):
            seats.insert(i)
        seat_count = total
        print(f"Additional {count} Seats are made available for reservation")
        if not waitlist.is_empty():
            sortedList = sortWaitlitsbyPriority()
            for index, (user, priority) in enumerate(sortedList, start=1):
                seatID = seats.get_min()
                reservation.insert(user, seatID[0])
                seats.delete_min()
                waitlist.delete(user)
                print(f"User {user} reserved seat {seatID[0]}")

                if index == count:
                    break
    else:
        print(f"Invalid input. Please provide a valid number of seats.")

def getAllReservations():
    reservation_list = []
    reservation._inorder_traversal(reservation.root, reservation_list)
    reservation_list.sort(key=lambda x: x.key)
    return reservation_list

def printReservations():
    reservation_list = getAllReservations()
    for reservation in reservation_list:
        print(f"Seat {reservation.key[0]}, User {reservation.value}")

#
def releaseSeats(userID1, userID2):
    if userID1 > 0:
        for userID in range(userID1, userID2):
            #get seatId of UserID assign to seatID
            re = reservation.search(userID)
            if re is not None:
                seatID = re.key
                seats.insert(seatID[0])
                print(userID)
                reservation.delete(userID)
        print(f"Reservations/waitlist of the users in the range {userID1, userID2} have been released")
        #seats reserved users
        list = sortWaitlitsbyPriority()
        if not waitlist.is_empty():
            for user in enumerate(list):
                seatID = seats.get_min()
                reservation.insert(user[0], seatID)
                seats.delete_min()
                print(f"User {user[0]} reserved seat {seatID}")
    else:
        print("Invalid input. Please provide a valid range of users.")



def quit():
    print("Program Terminated")
    sys.exit(0)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    initialize(4)
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
    available()
    printReservations()
    quit()
