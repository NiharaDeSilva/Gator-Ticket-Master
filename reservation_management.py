import sys
import time
from waitlist import Waitlist
from seat_list import SeatList
from reservation_list import ReservationList

'''
This program uses a Red Black Tree and a Binary Min Heap to implement the seat reservation and waiting list system for Gator Ticket Master.
Supported commands are Initialize, Available, Reserve, Cancel, ExitWaitList, UpdatePriority, AddSeats, PrintReservations, ReleaseSeats, Quit.
'''

seats = SeatList()
reservation = ReservationList()
waitlist = Waitlist()


# Keep Track of the total seats allocated for Users
seat_count=0

# Initialize a number of seats
def initialize(count):
    global seat_count
    if count > 0:
        for i in range(1, count + 1):
            seats.add_seats(i)
        print(count, "seats are made available for reservation")
        seat_count = count
        return seat_count
    else:
        print("Invalid input. Please provide a valid number of seats.")
        return -1

# Reserve a seat, pass the user ID and priority
def reserve(userID, userPriority):
    if not seats.is_empty_seats():
        seatID = seats.get_first_available_seat()
        reservation.make_reservation(userID, seatID)
        seats.assign_seat()
        print(f"User {userID} reserved seat {seatID}")
        return reservation
    else:
        timestamp = time.time()
        waitlist.add_to_waitlist(userID, userPriority, timestamp)     # create a record in waitlist, with user priority
        print(f"User {userID} is added to the waiting list")
        return waitlist


# Print the available seats and number of users in the waitlist
def available():
    print(f"Total Seats Available : {seats.get_seat_count()}, Waitlist :{waitlist.get_size()}")


# Cancel reservation if user has reserved a seat and user ID matches the seat ID
def cancel(seatID, userID):
    if (reservation.search_reservation(userID) is not None):
        result = reservation.search_reservation(userID)
        if result.key == seatID:
            if waitlist.is_empty():
                reservation.remove_reservation(userID)
                seats.add_seats(seatID)
                print(f"User {userID} canceled their reservation")
            else:
                reservation.remove_reservation(userID)
                new_userID = waitlist.sort_waitlist_by_priority()[0]
                reservation.make_reservation(new_userID[0], seatID)
                waitlist.drop_from_waitlist(new_userID[0])
                print(f"User {userID} canceled their reservation")
                print(f"User {new_userID[0]} reserved seat {seatID}")
        elif ((reservation.search_reservation(userID).value != None) and (reservation.search_reservation(userID).key != seatID)):
            print(f"User {userID} has no reservation for seat {seatID} to cancel")
    else:
        print(f"User {userID} has no reservation to cancel")



# Add seats to the available seat list
def add_seats(count):
    global seat_count
    if count > 0:
        total = seat_count + count
        for i in range(seat_count + 1, total + 1):
            seats.add_seats(i)
        seat_count = total
        print(f"Additional {count} Seats are made available for reservation")
        assign_seats_to_waitlist(count)
    else:
        print(f"Invalid input. Please provide a valid number of seats.")


# Print the reservations ordered by seat number
def print_reservations():
    reservation_list = reservation.get_all_reservations()
    for item in reservation_list:
        print(f"Seat {item.key}, User {item.value}")


'''
Release seats of users in the user ID range given, if seats have been reserved.
If users are in waitlist release from waitlist
'''
def release_seats(userID1, userID2):
    if userID1 > 0: #Check this
        reservations_released = False
        waitlist_released = False
        count = 0
        for userID in range(userID1, userID2):
            if reservation.search_reservation(userID) is not None:
                result = reservation.search_reservation(userID)
                seatID = result.key
                seats.add_seats(seatID)
                reservation.remove_reservation(userID)
                count += 1
                reservations_released = True
            elif waitlist.search(userID) is not None:
                waitlist.drop_from_waitlist(userID)
                waitlist_released = True
        if reservations_released:
            print(f"Reservations of the users in the range {userID1, userID2} have been released")
        elif waitlist_released:
            print(f"Waitlist of the users in the range {userID1, userID2} have been released")
        newReservations = assign_seats_to_waitlist(count)
        return newReservations
    else:
        print("Invalid input. Please provide a valid range of users.")
        return


# If the user wants to exit the waitlist
def exit_waitlist(userID):
    if waitlist.search(userID) is not None:
        waitlist.drop_from_waitlist(userID)
        print(f"User {userID} is removed from the waiting list")
    else:
        print(f"User {userID} is not in waitlist")



# Update the user priority if user is in waitlist
def update_priority(userID, userPriority):
    priority_updated = waitlist.modify_priority(userID, userPriority)
    if priority_updated:
        print(f"User {userID} priority has been updated to {userPriority}")
    else:
        print(f"User {userID} priority is not updated")



# Assign seats to users in waitlist if seats are available
def assign_seats_to_waitlist(count):
    while (count >= 0) and (not waitlist.is_empty()):
        sortedList = waitlist.sort_waitlist_by_priority()
        for index, (user, priority, timeStamp) in enumerate(sortedList, start=1):
            seatID = seats.get_first_available_seat()
            if seatID is not None:
                reservation.make_reservation(user, seatID)
                seats.assign_seat()
                waitlist.remove_from_waitlist()
                print(f"User {user} reserved seat {seatID}")
            count -= 1
    return reservation


def quit():
    print("Program Terminated!!")
    sys.exit(0)


