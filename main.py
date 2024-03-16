import datetime

# Placeholder for student database
students = {
    1234: 'John Doe'
}

# Placeholder for active bathroom passes
active_passes = {}

def show_menu():
    print("\n1. Go to Bathroom")
    print("2. Coming Back to Class")
    print("3. Exit")
    return input("Choose an option: ")

def go_to_bathroom(student_id):
    if student_id in active_passes:
        print("Error: Student is already out.")
    else:
        active_passes[student_id] = datetime.datetime.now()
        formatted_time = active_passes[student_id].strftime('%Y-%m-%d %H:%M:%S')
        print(f"{students[student_id]} has left for the bathroom at {formatted_time}.")

def coming_back_to_class(student_id):
    if student_id not in active_passes:
        print("Error: No active bathroom pass for this student.")
    else:
        check_out_time = active_passes.pop(student_id)
        check_in_time = datetime.datetime.now()
        elapsed = check_in_time - check_out_time
        elapsed_seconds = elapsed.total_seconds()
        elapsed_formatted = str(datetime.timedelta(seconds=round(elapsed_seconds)))
        print(f"{students[student_id]} is coming back to class.")
        print(f"Time spent in bathroom: {elapsed_formatted}")

def main():
    while True:
        student_id = input("\nEnter your student ID: ")
        try:
            student_id = int(student_id)
        except ValueError:
            print("Invalid student ID. Please enter a numeric ID.")
            continue

        if student_id not in students:
            print("Invalid student ID")
            continue

        option = show_menu()

        if option == '1':
            go_to_bathroom(student_id)
        elif option == '2':
            coming_back_to_class(student_id)
        elif option == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()