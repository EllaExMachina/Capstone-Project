#gets list of months for due date
months = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}

# ====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''
user_details = {}

# Load usernames and passwords
with open("user.txt", "r") as userfile:
    for line in userfile:
        username, password = line.split(",")  # this creates split list of object details that can be called
        user_details[username.strip()] = password.strip()

while True:  # until successful login
    input_username = input("Please enter your username: ")
    input_password = input("Please enter your password: ")
    if input_username in user_details:  # won't allow non registered user to log in
        if input_password == user_details[input_username]:
            # Logged in
            print("Logged in")
            username = input_username
            break
        else:
            print(f"Incorrect password, please try again")
    else:
        print("Username not recognised, please register")

#define register user function
def reg_user():
    new_username = input("Please enter a new username: ")
    with open("user.txt", "r") as userfile:
        for line in userfile:
            logindetails = line.split(",")
            if new_username == logindetails[0]:
                print("Already registered")
                return
    new_password = input("Please enter a new password: ")
    new_password_confirmation = input("Please confirm your new password: ")
    if new_password == new_password_confirmation:
        user_details[new_username] = new_password
        user = open('user.txt', 'a')
        user.write(f"{new_username},{new_password}")
        user.close()
        print("Thank you, new password and username added to user.txt file")

    else:
        print("Passwords do not match, start again")


#defines check date function
def check_date_format(date_str):
    date_parts = date_str.split(" ")
    if len(date_parts) != 3:
        return False
    if not date_parts[0].isnumeric():
        return False
    if date_parts[1].lower() not in months:
        return False
    if not date_parts[2].isnumeric():
        return False

    return True

#define add task function
def add_task():
    task_username = input("Please enter the username of the person assigned to this task: ")
    if task_username.strip().lower() not in user_details:
        print("Please enter a registered user")
        return
    task_title = input("Please enter the title of this task: ")
    task_description = input("Please enter a description of this task: ")
    task_due_date = input("Please enter a due date for this task (DD Mmm YYYY, e.g. 21 Feb 2022): ")
    if not check_date_format(task_due_date):
        print("Invalid date format")
        return
    current_date = input("Please enter today's date (DD Mmm YYYY, e.g. 21 Feb 2022): ")
    if not check_date_format(current_date):
        print("Invalid date format")
        return
    task_complete = "No"
    with open('tasks.txt', 'a') as task_list:
        task_list.write(
            f"{task_username}, {task_title}, {task_description}, {task_due_date}, {current_date}, {task_complete}\n")
    print("New task registered\n")

#defines view all function
def view_all():
    with open("tasks.txt", "r") as task_list:
        for line in task_list:
            # performs this operation for all tasks in list by looping through them
            task = line.split(", ")
            # prints all components of the task
            print("__________")
            print(f"\n task:                   {task[1]}")
            print(f" task username:          {task[0]}")
            print(f" task date assigned:     {task[3]}")
            print(f" task date due:          {task[4]}")
            print(f" task completion status: {task[5]}")
            print(f" {task[2]}\n")

#defines edit task function
def edit_task(line_number, changes):
    new_task_lines = []
    current_line = 0
    # Read and edit the old lines
    with open("tasks.txt", "r") as old_task_lines:
        for old_line in old_task_lines:
            if current_line != line_number:
                new_task_lines.append(old_line.strip("\n"))
            else:
                task = old_line.strip("\n").split(", ")
                for field_number, value in changes.items():
                    if field_number != -1:
                        if task[-1] == "Yes":
                            print("Please edit a task that has not been completed")
                            return
                    task[field_number] = value
                new_line = ", ".join(task)
                new_task_lines.append(new_line)
            current_line += 1

    # Write the new file
    with open("tasks.txt", "w") as taskfile:
        for line in new_task_lines:
            taskfile.write(line + "\n")

    print("Task list updated")

#define view my tasks function
def view_my_tasks():
    with open("tasks.txt", "r") as task_list:
        count = 1  # Task numbers start at 1
        line_number = 0  # Line numbers start at 0
        line_numbers = {}  # To keep track of what line each user task is on
        print("Here are your assigned tasks:\n")
        for line in task_list:
            task = line.strip("\n").split(", ")
            line_numbers[count] = line_number

            if username == task[0]:
                print("__________\n")
                print(f" task number:            {count}")
                print(f" task:                   {task[1]}")
                print(f" task username:          {task[0]}")
                print(f" task date assigned:     {task[3]}")
                print(f" task date due:          {task[4]}")
                print(f" task completion status: {task[5]}")
                print(f" {task[2]}")

                count = count + 1
            line_number = line_number + 1
        print("__________\n")

        task_selection = int(input("Please select a task number or enter -1 to return to the main menu: "))
        if task_selection == -1:
            return
        if task_selection not in line_numbers:
            print("Please select a valid task")
            return
        user_selection = input("Please enter 'e' to edit task or 'm' to mark as complete: ").lower()

        changes = {}  # {field number: new value, }
        if user_selection == 'm':
            changes[-1] = "Yes"
        elif user_selection == 'e':
            edit_selection = input("please enter 'd' for edit due date or 'u' for edit username: ")
            if edit_selection == 'd':
                new_due_date = input("Please enter a new due date (DD Mmm YYYY): ")
                if not check_date_format(new_due_date):
                    print("Please enter a valid due date, e.g. 29 Oct 2022")
                    return
                changes[4] = new_due_date
            elif edit_selection == 'u':
                new_username = input("Please enter a new username: ")
                while new_username not in user_details:
                    new_username = input(f"Please enter a registered user from {user_details.keys()}: ")
                changes[0] = new_username
            else:
                print("Please select one of the above options")
                return

        edit_task(line_numbers[task_selection], changes)
        return


def is_date_before(date_a, date_b):
    # is date a before date b
    date_a_parts = date_a.split(" ")
    date_b_parts = date_b.split(" ")
    if int(date_a_parts[2]) < int(date_b_parts[2]):
        # Date a year before date b year, so must be before
        return True
    elif int(date_a_parts[2]) > int(date_b_parts[2]):
        # Date a year after date b year, so not before
        return False
    # Otherwise the same year

    if months[date_a_parts[1].lower()] < months[date_b_parts[1].lower()]:
        # Date a month before date b month
        return True
    elif months[date_a_parts[1].lower()] > months[date_b_parts[1].lower()]:
        # Date a month after date b month
        return False

    # Must be same year and same month
    if int(date_a_parts[0]) < int(date_b_parts[0]):
        return True
    else:
        return False

#define generate report function
def generate_reports():
    current_date = input("Please enter today's date (DD Mmm YYYY, e.g. 21 Feb 2022): ")
    if not check_date_format(current_date):
        print("Invalid date format")
        return

    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    uncompleted_overdue = 0

    user_stats = {}
    with open("user.txt", "r") as userfile:
        for line in userfile:
            username = line.split(",")[0]
            user_stats[username] = [0, 0, 0, 0]  # total, completed, uncompleted, overdue

    with open("tasks.txt", "r") as task_list:
        for line in task_list:
            task = line.strip("\n").split(", ")
            task_username = task[0]
            total_tasks = total_tasks + 1
            user_stats[task_username][0] += 1
            if task[5] == "Yes":
                completed_tasks = completed_tasks + 1
                user_stats[task_username][1] += 1
            else:  # Uncompleted
                uncompleted_tasks = uncompleted_tasks + 1
                user_stats[task_username][2] += 1
                task_due_date = task[4]
                if is_date_before(task_due_date, current_date):
                    # Due date before current date, overdue
                    uncompleted_overdue = uncompleted_overdue + 1
                    user_stats[task_username][3] += 1

    if total_tasks != 0:
        percent_complete = 100 * completed_tasks / total_tasks
        percent_incomplete = 100 * uncompleted_tasks / total_tasks
        percent_overdue = 100 * uncompleted_overdue / total_tasks
    else:  # cannot divide by zero
        percent_complete = percent_incomplete = percent_overdue = 0

    with open("task_overview.txt", "w") as task_overview:
        task_overview.write("-------------")
        task_overview.write("\nTask Overview")
        task_overview.write("\n-------------")
        task_overview.write(f"\nTotal tasks:       {total_tasks}")
        task_overview.write(f"\nCompleted tasks:   {completed_tasks} ({int(percent_complete)}%)")
        task_overview.write(f"\nUncompleted tasks: {uncompleted_tasks} ({int(percent_incomplete)}%)")
        task_overview.write(f"\nOverdue tasks:     {uncompleted_overdue} ({int(percent_overdue)}%)")

    with open("user_overview.txt", "w") as user_overview:
        user_overview.write("-------------")
        user_overview.write("\nUser Overview")
        user_overview.write("\n-------------")
        user_overview.write(f"\nTotal users:  {len(user_stats)}")
        for username, data in user_stats.items():
            if total_tasks != 0:
                percent_of_total = 100 * data[0] / total_tasks
            else:
                percent_of_total = 0

            if completed_tasks != 0:
                percent_of_complete = 100 * data[1] / completed_tasks
            else:
                percent_of_complete = 0

            if uncompleted_tasks != 0:
                percent_of_uncompleted = 100 * data[2] / uncompleted_tasks
            else:
                percent_of_uncompleted = 0

            if uncompleted_overdue != 0:
                percent_of_overdue = 100 * data[3] / uncompleted_overdue
            else:
                percent_of_overdue = 0

            user_overview.write("\n-------------")
            user_overview.write(f"\nUsername:          {username}")
            user_overview.write(f"\nUser tasks:        {data[0]} ({int(percent_of_total)}% of total tasks)")
            user_overview.write(f"\nCompleted tasks:   {data[1]} ({int(percent_of_complete)}% of completed tasks)")
            user_overview.write(f"\nUncompleted tasks: {data[2]} ({int(percent_of_uncompleted)}% of uncompleted tasks)")
            user_overview.write(f"\nOverdue tasks:     {data[3]} ({int(percent_of_overdue)}% of overdue tasks)")
            if data[0] != 0:
                user_overview.write(
                    f"\nUser's tasks are {int(100 * data[1] / data[0])}% complete, {int(100 * data[2] / data[0])}% uncompleted, and {int(100 * data[3] / data[0])}% overdue")

#define statistics function
def statistics():
    generate_reports()
    selection = ""
    while selection not in ["t", "u"]:
        selection = input("Please enter 't' for task statistics or 'u' for user statistics: ")
    if selection == "t":
        filename = "task_overview.txt"
    else:
        filename = "user_overview.txt"

    with open(filename, "r") as stats_file:
        for line in stats_file:
            print(line.strip("\n"))

#menu for all
menu = {"r": "Registering a user",
        "a": "Adding a task",
        "vm": "View my tasks",
        "va": "View all tasks",
        "e": "Exit"}
#appended menu for admin
if username == "admin":
    menu["gr"] = "Generate reports"
    menu["st"] = "View statistics"

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    # creates separate menu for admin with more choices
    print("------------------------------------------")
    print("Select one of the following Options below:")
    for menu_option, description in menu.items():
        print(f"{menu_option} - {description}")

    menu_choice = input(": ")
    if menu_choice not in menu:
        print("Please select a command from the menu")
        continue

    if menu_choice == 'r':
        reg_user()
    # adding a task
    elif menu_choice == 'a':
        add_task()
        # viewing all tasks
    elif menu_choice == 'va':
        view_all()
        # viewing 'my tasks'
    elif menu_choice == 'vm':
        # create empty task list to populate later
        view_my_tasks()
        # for choice 'statistics' (admin only allowed)
    elif menu_choice == 'st':
        statistics()
        # for choice 'generate report'
    elif menu_choice == 'gr':
        generate_reports()
        # for choice 'exit'
    elif menu_choice == 'e':
        print("Goodbye")
        break
    else:
        print("Unexpected input")