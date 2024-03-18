from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime
import os
import pytz
import json  # Import the json module

app = Flask(__name__)
app.secret_key = '95311'  # Replace this with a strong secret key

# JSON file to store student data
students_file = 'students.json'

# Load student data from JSON file, or create an empty dictionary if the file doesn't exist
def load_students():
    if os.path.exists('students.json'):
        with open('students.json', 'r') as file:
            students = json.load(file)
    else:
        students = {}
    return students

# Save student data to JSON file
def save_students(students):
    with open(students_file, 'w') as file:
        json.dump(students, file)

# Initialize students dictionary
students = load_students()

# List to store bathroom visit logs
bathroom_log = []

# Variable to track if the bathroom is occupied and when they entered
bathroom_occupied = None
bathroom_occupied_since = None

# Define the PST timezone
pst = pytz.timezone('America/Los_Angeles')

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

    # Load the student data
    students = load_students()

    if bathroom_occupied is not None:
        flash(f"Cannot go to the bathroom. It is currently occupied by {students.get(str(bathroom_occupied), 'Unknown')}.")
        return

    bathroom_occupied = student_id
    bathroom_occupied_since = datetime.datetime.now(pytz.utc).astimezone(pst)
    # Log the bathroom visit
    bathroom_log.append(f"{students.get(str(student_id), 'Unknown')} went to the bathroom at {bathroom_occupied_since.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    flash(f"{students.get(str(student_id), 'Unknown')} has left for the bathroom at {bathroom_occupied_since.strftime('%Y-%m-%d %H:%M:%S %Z')}.")
    return True

def coming_back_to_class(student_id):
    global bathroom_occupied, bathroom_occupied_since

    # Load the student data
    students = load_students()

    if bathroom_occupied != student_id:
        flash("Error: You did not have an active bathroom pass.")
        return False

    coming_back_time = datetime.datetime.now(pytz.utc).astimezone(pst)
    duration = coming_back_time - bathroom_occupied_since
    minutes, seconds = divmod(duration.seconds, 60)
    # Log the return from the bathroom
    bathroom_log.append(f"{students.get(str(student_id), 'Unknown')} came back from the bathroom at {coming_back_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    flash(f"{students.get(str(student_id), 'Unknown')} came back to class at {coming_back_time.strftime('%Y-%m-%d %H:%M:%S %Z')}.")
    flash(f"Duration in the bathroom: {minutes} minutes and {seconds} seconds.")
    bathroom_occupied = None
    bathroom_occupied_since = None
    return True

def view_bathroom_log():
    clear_screen()
    if not bathroom_log:
        flash("No bathroom visits have been logged yet.")
    else:
        for entry in bathroom_log:
            flash(entry)
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

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_id_input = request.form.get('student_id')
        if student_id_input.lower() == 'admin':
            return redirect(url_for('view_log'))

        students = load_students()  # Load the student data
        
        try:
            student_id = int(student_id_input)
        except ValueError:
            flash("Invalid student ID. Please enter a numeric ID.")
            return redirect(url_for('index'))

        # The JSON keys are stored as strings, so we need to convert the keys back to integers
        student_ids = {int(k): v for k, v in students.items()}

        # Check if the student_id exists in the loaded students data
        if student_id in student_ids:
            session['student_id'] = student_id
            return redirect(url_for('menu'))
        else:
            flash("Invalid student ID.")
            return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    student_id = session.get('student_id')
    if student_id is None:
        flash("Please log in with your student ID.")
        return redirect(url_for('index'))

    students = load_students()  # Load the student data here

    # Convert student_id to string because JSON keys are stored as strings
    student_name = students.get(str(student_id), "Unknown")

    if request.method == 'POST':
        if 'go_to_bathroom' in request.form:
            go_to_bathroom(student_id)  # Flash messages are set within this function
        elif 'coming_back' in request.form:
            coming_back_to_class(student_id)  # Flash messages are set within this function
        elif 'logout' in request.form:
            session.pop('student_id', None)
            flash("You have been logged out.")
            return redirect(url_for('index'))
    
    return render_template('menu.html', student_name=student_name)

@app.route('/view_log')
def view_log():
    return render_template('view_log.html', bathroom_log=bathroom_log)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        student_id_input = request.form.get('student_id')
        student_name = request.form.get('student_name')
        try:
            student_id = int(student_id_input)
        except ValueError:
            flash("Invalid student ID. Please enter a numeric ID.")
            return redirect(url_for('signup'))
        
        # Load the current students from the file
        students = load_students()
        
        # Convert student_id to string because JSON keys are stored as strings
        if str(student_id) in students:
            flash("A student with this ID already exists.")
            return redirect(url_for('signup'))
        else:
            students[str(student_id)] = student_name  # Use string version of the ID
            # Save the updated students dictionary to the file
            save_students(students)
            flash("Signup successful!")
            return redirect(url_for('index'))
        
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=False)