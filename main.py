import os
import io
import sys
from contextlib import redirect_stdout
from reservation_management import (
    initialize, available, reserve, cancel, printReservations,
    addSeats, releaseSeats, exitWaitlist, updatePriority, quit)

'''
This program uses a Red Black Tree and a Binary Min Heap to implement the seat reservation and waiting list system for Gator Ticket Master.
This script automates the execution of commands for the program.
'''

'''
Takes one command and run the respective operation Reservation_management.py. 
Supported commands are Initialize, Available, Reserve, Cancel, ExitWaitList, UpdatePriority, AddSeats, PrintReservations, ReleaseSeats, Quit.
The output generated is saved under <input_file_base>_output_file.txt 
'''
def run_commands_from_file(file_name):
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_output_file.txt"

    with open(file_name, 'r') as file, open(output_file, 'w') as out:
        for line in file:
            line = line.strip()
            if not line:
                continue

            command = line.split('(')[0]
            args_str = line[len(command) + 1:-1].strip()

            if args_str:
                args = [int(arg) if arg.isdigit() else arg for arg in args_str.split(', ')]
            else:
                args = []

            with io.StringIO() as buf, redirect_stdout(buf):
                try:
                    if command == 'Quit':
                        quit()
                    elif command == 'Initialize':
                        initialize(*args)
                    elif command == 'Available':
                        available()
                    elif command == 'Reserve':
                        reserve(*args)
                    elif command == 'Cancel':
                        cancel(*args)
                    elif command == 'ExitWaitlist':
                        exitWaitlist(*args)
                    elif command == 'UpdatePriority':
                        updatePriority(*args)
                    elif command == 'PrintReservations':
                        printReservations()
                    elif command == 'AddSeats':
                        addSeats(*args)
                    elif command == 'ReleaseSeats':
                        releaseSeats(*args)
                    else:
                        print(f"Unknown command: {command}")
                except SystemExit:
                    output = buf.getvalue()
                    out.write(output)
                    return

                output = buf.getvalue()
                out.write(output)

        print(f"Output written to {output_file}")

'''
This is the main method of the program. 
It expects the input file containing commands to be processed.
it reads the input file name and calls `run_commands_from_file` to execute the commands.
'''

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
    else:
        input_file = sys.argv[1]
        run_commands_from_file(input_file)
