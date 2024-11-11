import sys
import reservation_management
import binary_heap
from priority_queue import BinaryMinHeap, Waitlist
import time

seats = BinaryMinHeap()
reservation = reservation_management.RedBlackTree()
waitlist = Waitlist()

seat_count=0
def Initialize(count):
    global seat_count
    if count > 0:
        for i in range(1, count + 1):
            seats.insert(i)
        print(count, "seats are made available for reservation")
        seat_count = count
        return seat_count
    else:
        print("Invalid input. Please provide a valid number of seats.")
        return -1  # Indicate an invalid input

def Reserve(userID, userPriority):
    if not seats.is_empty():
        seatID = seats.get_min()
        reservation.insert(userID, seatID)
        seats.delete_min()
        print(f"User {userID} reserved seat {seatID}")
        return reservation
    else:
        timestamp = time.time()
        waitlist.add_to_waitlist(userID, userPriority, timestamp)     # create a record in waitlist, with user priority
        print(f"User {userID} is added to the waiting list")
        return waitlist

def Available():
    print(f"Total Seats Available : {seats.get_size()}, Waitlist :{waitlist.get_size()}")

def Cancel(seatID, userID):
    # userReservation = reservation.search(userID)
    if (reservation.search(userID) is not None):
        result = reservation.search(userID)
        if (isinstance(result.key, tuple) and result.key[0] == seatID) or (result.key == seatID):
            if waitlist.is_empty():
                reservation.delete(userID)
                seats.insert(seatID)
                print(f"User {userID} canceled their reservation")
            else:
                reservation.delete(userID)
                new_userID = sortWaitlistbyPriority()[0]
                reservation.insert(new_userID[0], seatID)
                waitlist.delete(new_userID[0])
                print(f"User {userID} canceled their reservation")
                print(f"User {new_userID[0]} reserved seat {seatID}")
        elif ((reservation.search(userID).value != None) and (reservation.search(userID).key != seatID)):
            print(f"User {userID} has no reservation for seat {seatID} to cancel")
    else:
        print(f"User {userID} has no reservation to cancel")

# If the user wants to exit the waitlist, given that he was never assigned a seat
def ExitWaitlist(userID):
    if waitlist.search(userID) is not None:
        waitlist.delete(userID)
        print(f"User {userID} is removed from the waiting list")
    else:
        print(f"User {userID} is not in waitlist")

# Modify the user priority only if he is in the waitlist heap. Update the heap with this modification
def UpdatePriority(userID, userPriority):
    return waitlist.update_priority(userID, userPriority)
    # if waitlist.search(userID) != -1:
    #     waitlist.update(userID, userPriority)
    #     print(f"User {userID} priority has been updated to {userPriority}")
    # else:
    #     #If the user is not in the waiting list
    #     print(f"User {userID} priority is not updated")


def sortWaitlistbyPriority():
    list = waitlist.get_waitlist()
    sortedList = sorted(list, key=lambda x: (-x[1], x[2]))
    return sortedList


#Add seats to the available seat list. The new seat numbers should follow the previously available range.
def AddSeats(count):
    global seat_count
    if count > 0:
        total = seat_count + count
        for i in range(seat_count + 1, total + 1):
            seats.insert(i)
        seat_count = total
        print(f"Additional {count} Seats are made available for reservation")
        assignSeatsToWaitlist(count)
    else:
        print(f"Invalid input. Please provide a valid number of seats.")

def getAllReservations():
    reservation_list = []
    reservation._inorder_traversal(reservation.root, reservation_list)
    sorted_list = sorted(reservation_list, key=lambda x: x.key)
    return sorted_list

def PrintReservations():
    reservation_list = getAllReservations()
    for reservation in reservation_list:
        if isinstance(reservation.key, tuple):
            # If it's a tuple, access the first element
            print(f"Seat {reservation.key[0]}, User {reservation.value}")
        else:
            # If it's an integer, print it directly
            print(f"Seat {reservation.key}, User {reservation.value}")
#
def ReleaseSeats(userID1, userID2):
    if userID1 > 0: #Check this
        count = 0
        for userID in range(userID1, userID2):
            if reservation.search(userID) is not None:
                result = reservation.search(userID)
                if isinstance(result.key, tuple):
                    seatID = result.key[0]  # Access the first element if it's a tuple
                else:
                    seatID = result.key
                seats.insert(seatID)
                reservation.delete(userID)
                count += 1
            elif waitlist.search(userID) is not None:
                waitlist.delete(userID)
        print(f"Reservations/Waitlist of the users in the range {userID1, userID2} have been released")
        newReservations = assignSeatsToWaitlist(count)
        #if user id in waitlist , those should also be removed
        return newReservations
    else:
        print("Invalid input. Please provide a valid range of users.")
        return

def assignSeatsToWaitlist(count):
    while (count >= 0) and (not waitlist.is_empty()):
        sortedList = sortWaitlistbyPriority()
        for index, (user, priority, timeStamp) in enumerate(sortedList, start=1):
            seatID = seats.get_min()
            if seatID is not None:
                reservation.insert(user, seatID)
                seats.delete_min()
                waitlist.remove_from_waitlist()
                print(f"User {user} reserved seat {seatID}")
            count -= 1
    return reservation

def deleteFromWaitlist(userID):
    return waitlist.delete(userID)


def Quit():
    print("Program Terminated!!")
    sys.exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Initialize(3)
    Reserve(6, 2)
    Reserve(1, 1)
    Reserve(9, 3)
    Reserve(2, 2)
    Reserve(5, 1)
    Reserve(4, 3)
    Reserve(3, 2)
    Available()
    ExitWaitlist(9)
    UpdatePriority(6, 3)
    UpdatePriority(3, 3)
    AddSeats(3)
    Available()
    Cancel(3, 9)
    Reserve(9, 3)
    Reserve(12, 2)
    Reserve(18, 1)
    Reserve(17, 3)
    ReleaseSeats(6, 11)
    UpdatePriority(18, 3)
    AddSeats(2)
    PrintReservations()
    Quit()
