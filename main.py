import os
import datetime

# Database of 10 students
students = {
    101: 'Alice Smith',
    102: 'Bob Johnson',
    103: 'Charlie Brown',
    104: 'David Lee',
    105: 'Eva Green',
    106: 'Fiona Gallagher',
    107: 'George White',
    108: 'Hannah Young',
    109: 'Ian Black',
    110: 'Jane King'
}

# List to store bathroom visit logs
bathroom_log = []

# Variable to track if the bathroom is occupied and when they entered
bathroom_occupied = None
bathroom_occupied_since = None

def clear_screen():
    # Clear the screen. Use 'cls' if on Windows.
    os.system('clear')

def show_menu(student_name):
    clear_screen()  # Clear the screen before showing the menu
    print(f'Welcome, {student_name}.')
    print("\n1. Go to Bathroom")
    print("2. Coming Back to Class")
    print("3. Exit")
    return input("Choose an option: ")

def go_to_bathroom(student_id):
    global bathroom_occupied, bathroom_occupied_since

    if bathroom_occupied is not None:
        print(f"Cannot go to the bathroom. It is currently occupied by {students[bathroom_occupied]}.")
        return

    bathroom_occupied = student_id
    bathroom_occupied_since = datetime.datetime.now()
    # Log the bathroom visit
    bathroom_log.append(f"{students[student_id]} went to the bathroom at {bathroom_occupied_since.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{students[student_id]} has left for the bathroom at {bathroom_occupied_since.strftime('%Y-%m-%d %H:%M:%S')}.")

def coming_back_to_class(student_id):
    global bathroom_occupied, bathroom_occupied_since

    if bathroom_occupied != student_id:
        print("Error: You did not have an active bathroom pass.")
        return

    coming_back_time = datetime.datetime.now()
    duration = coming_back_time - bathroom_occupied_since
    minutes, seconds = divmod(duration.seconds, 60)
    # Log the return from the bathroom
    bathroom_log.append(f"{students[student_id]} came back from the bathroom at {coming_back_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{students[student_id]} is coming back to class at {coming_back_time.strftime('%Y-%m-%d %H:%M:%S')}.")
    print(f"Duration in the bathroom: {minutes} minutes and {seconds} seconds.")
    bathroom_occupied = None
    bathroom_occupied_since = None

def view_bathroom_log():
    clear_screen()
    if not bathroom_log:
        print("No bathroom visits have been logged yet.")
    else:
        for entry in bathroom_log:
            print(entry)
    input("Press Enter to continue...")  # Wait for user to acknowledge

def main():
    clear_screen()
    while True:
        student_id_input = input("Enter your student ID or type 'admin' to view the log: ")
        
        # Check for admin access
        if student_id_input.lower() == 'admin':
            view_bathroom_log()
            clear_screen()
            continue

        try:
            student_id = int(student_id_input)
        except ValueError:
            print("Invalid student ID. Please enter a numeric ID or type 'admin'.")
            input("Press Enter to continue...")  # Wait for user to acknowledge
            clear_screen()
            continue

        if student_id not in students:
            print("Invalid student ID.")
            input("Press Enter to continue...")  # Wait for user to acknowledge
            clear_screen()
            continue

        # Store the student's name for reuse in the menu display
        student_name = students[student_id]

        # Start of the new inner loop
        while True:
            option = show_menu(student_name)

            if option == '1':
                go_to_bathroom(student_id)
                input("Press Enter to continue...")  # Wait for user to acknowledge
            elif option == '2':
                coming_back_to_class(student_id)
                input("Press Enter to continue...")  # Wait for user to acknowledge
            elif option == '3':
                print('Going back to the main menu...')
                clear_screen()
                break  # Break to allow entering another ID
            else:
                print("Invalid option. Please try again.")
                input("Press Enter to try again...")  # Wait for user to acknowledge
                clear_screen()

if __name__ =="__main__":
    main()