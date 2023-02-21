# import libraries
from datetime import date
from datetime import *
from datetime import datetime
from datetime import date, datetime


# this is a program for a small business that can help it to manage tasks assigned to each member of the team.
# for this part the following resource was very helpful https://stackoverflow.com/questions/73121319/login-from-txt-file-in-python
details = []
with open("user.txt", "r") as f:
    for line in f.readlines():
        user, pwd = line.split(sep=', ')
        details.append((user.strip(), pwd.strip()))

# the user should be prompted to enter a username and password.
login = input('Please enter your login: \n')
password = input('Please enter you password: \n')


# CREATING FUNCTIONS
def reg_user():
        # only the user with the username ‘admin’ is allowed to register users.
        if login == 'admin':
            new_user = input('Please provide a new username:\n') 

            while new_user in str(details):
                print('This user already exists.')
                new_user = input('Please provide a new username:\n') 
                                
            new_pass = input('Please provide a new password:\n')
            confirm_pass = input('Please confirm your password:\n')
            
            while new_pass != confirm_pass:
                print('Passwords do NOT match.')
                new_pass = input('Please provide a new password:\n')
                confirm_pass = input('Please confirm your password:\n')
            
            if new_pass == confirm_pass and new_user not in details:
                file = open('user.txt', 'a')
                file.write(new_user)
                file.write(', ')
                file.write(new_pass)
                file.write('\n')
                file.close()
        else:
            print('Sorry. You don\'t have the permission to add new users.\n')
        return '\033[92m' + 'New user added.' + '\033[00m'
                        
                    

def view_mine(): 
    tasks_read = open('tasks.txt', 'r')
    data = tasks_read.readlines()
    for pos, line in enumerate(data, 1):
        if login in line:
            split_data = line.split(', ')
            
            output = f'─────────────────[{pos}]─────────────────\n'
            output += f'Assigned to:\t\t{split_data[0]}\n'
            output += f'Task:\t\t\t{split_data[1]}\n'
            output += f'Date assigned:\t\t{split_data[4]}\n'
            output += f'Due date:\t\t{split_data[3]}\n'
            output += f'Taks Complete?:\t\t{split_data[5]}\n'
            output += f'Task description:\t{split_data[2]}\n'
            output += '\n'
            output += f'──────────────────────────────────'

            print(output)

    while True: # it's a simple condition to avoid bugs
        task_selected = int(input("Please enter the task number that you wish to select or -1 - to return to the main menu \n")) -1

        if task_selected > len(data) or task_selected < -2 or task_selected == -1:
            print('You have selcted an invalid option, try again.')
            continue
        edit_data = data[task_selected]
        break
    
             # we got to the user data, that we want to be able to change
    if task_selected == -2:  # If they select '-1', they return to the outer while loop main menu.
        return(menu)   

    while True:
        output2 = '\033[94m'+'─────────────SELECT AN OPTION───────────────────\n'
        output2 += '1 - Edit the task \n'
        output2 += '2 - Mark as completed \n'
        output2 +='────────────────────────────────\n'+ '\033[00m'

        choice = int(input(output2))
        break

    split_data = edit_data.split(', ')
    if choice == 1 and split_data[-1] == 'No\n':
        output3 = '\033[94m'+'─────────────SELECT AN OPTION───────────────────\n'
        output3 += '3 - Edit due date \n'
        output3 += '4 - Reassign the task  \n'
        output3 +='────────────────────────────────\n'+ '\033[00m'
        next_choice = int(input(output3))

        if next_choice == 3:
            split_data = edit_data.split(', ')
            split_data[3] = input('Type new deadline, e.g. dd-mm-yyyy:\n')
            due_data = ', '.join(split_data)
            data[task_selected] = due_data # overwriting

            dat_format = split_data[3].split('-')
            num_date = [int(x) for x in dat_format]
            due_data = date(num_date[2], num_date[1], num_date[0]).strftime('%d %b %Y') 

            file = open('tasks.txt', 'w')
            for line in data:   #IT TAKES ALL orginal data and rewrites it here
                file.write(line)
            file.close()

            return '\033[92m' +'The deadline has been changed successfully.' +'\033[00m'
                            
        elif next_choice == 4:
            split_data[0] = input('Enter a name of a peron who you want to allocate to the task:\n')
            assign_data = ', '.join(split_data)
            data[task_selected] = assign_data # overwriting
            file_read = open('tasks.txt', 'w')
            for line in data:   #IT TAKES ALL orginal data and rewrites it here
                file_read.write(line)
            file_read.close()

            return '\033[92m' +'The task has been successfully re-assigned' + '\033[00m'
            
        else:
            print('You have selcted an invalid option, try again. Type 3 or 4, please.')
            next_choice = int(input(output2))
            

    elif choice == 2 and split_data[-1] == 'No\n':
        split_data = edit_data.split(', ')
        split_data[-1] = 'Yes\n'   # it refers to the last element which is NO
        new_data = ', '.join(split_data)  # now we need to replace the data that we originally had
        data[task_selected] = new_data # overwriting

    elif choice == 1 and split_data[-1] == 'Yes\n':
        print('You cannot makes changes to a completed task.')
        return(menu) 

    else:
        print('You have selcted an invalid option, try again. Type 1 or 2, please.')
        choice = int(input(output2))

            
    tasks_read.close()

    myfile = open('tasks.txt', 'w')
    for line in data:   #IT TAKES ALL orginal data and rewrites it here
        myfile.write(line)

            
    return '\033[92m' + 'Your task has been successfully changed to complete.' + '\033[00m'

def add_task():

    task_assign = input('To whom you want the task to be assigned to?\n')
    task_title = input('Provide a title of a task:\n')
    description = input('Please a description of the task:\n')

    deadline = input('Type the due date of the task, e.g. dd-mm-yyyy:\n')
    dat_format = deadline.split('-')
    num_date = [int(x) for x in dat_format]
    due_data = date(num_date[2], num_date[1], num_date[0]).strftime('%d %b %Y') 

    is_complete = 'No' #automatically assigned value

    today = date.today()
    today_date = today.strftime('%d %b %Y') # to get the right format

    task_file = open('tasks.txt', 'a')
    task_file.write(f'{task_assign}, {task_title}, {description}, {due_data}, {today_date}, {is_complete}\n')
    task_file.close()
    return '\033[92m' +'Task added successfully.' + '\033[00m'
       
def view_all():
    with open("tasks.txt", "r") as f:
        for line in f.readlines():
            new_line = line.split(', ')
            print('\033[94m'+'─' * 40  +'\n')
            print(('Task: ' +'\t' + new_line[1]).expandtabs(20))
            print(('Assigned to: ' + '\t' + new_line[0]).expandtabs(20))
            print(('Date assigned: ' +'\t' + new_line[4]).expandtabs(20))
            print(('Due date: ' +'\t' + new_line[3]).expandtabs(20))
            print(('Taks Complete? ' +'\t' + new_line[5]).expandtabs(20))
            print(('Task description: ' +'\n' + '  ' + new_line[2]).expandtabs(5))
            print('─' * 40   +'\n'+ '\033[00m')
        return '\nAll tasks displayed below. '

# Function to calculate percentage
def percentage(part, whole):
    return 100 * (float(part) / float(whole))

while (login, password) not in details:
    print("\nIncorrect username or password.", "Please try again.\n", sep='\n') 
    login = input('Please enter your login: \n')
    password = input('Please enter you password: \n')
if (login, password) in details:
    print('\033[92m'+ 'You\'re logged in!' + '\033[00m')
    
while True:
    # the admin user is provided with a new menu option that allows them to display statistics.
    if login == 'admin':

        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
vs - view statistics
e - Exit
: ''').lower()

    else:
    # presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
e - Exit
: ''').lower()


    # user chooses ‘r’ to register a user.
    if menu == 'r':

        print(reg_user())

    # user chooses ‘a’ to add a task.
    elif menu == 'a':
        print(add_task())    
    
    # user chooses ‘va’ to view all tasks.
    elif menu == 'va':
        print(view_all())

    # user chooses ‘vm’ to view the tasks that are assigned to them.    
    elif menu == 'vm':    
        print(view_mine())  

    elif menu == 'vs':
        if login == 'admin':
            print('\nStatistics:\n')

            with open("tasks.txt", "r") as f:
                tasks_num = len(f.readlines())
                print(f'The total number of tasks is: {tasks_num}')

            with open("user.txt", "r") as f:
                users_num = len(f.readlines())
                print(f'The total number of users is: {users_num}\n')
        else:
            print('Sorry you don\'t have the permission to access the statistics.' )
        
    elif menu == 'gr':
        with open("tasks.txt", "r") as f:
            tasks_num = len(f.readlines())
            info_total = f'The total number of tasks is: {tasks_num}\n' 
            
        with open("tasks.txt", "r") as f5:
            tasks = 0
            undone = 0
            overdue_tasks = 0
            today = date.today()
            
            for line in f5.readlines():
                split_line = line.split(', ') 
                duedate = datetime.strptime(split_line[0::][3], '%d %b %Y') 
                
                if duedate < datetime.combine(date.today(), datetime.min.time()) and split_line[0::][-1] == 'No\n' or split_line[0::][-1] == 'No' : 
                    overdue_tasks  += 1

                if split_line[0::][-1] == 'Yes\n' or split_line[0::][-1] == 'Yes':
                    tasks += 1 

                elif split_line[0::][-1] == 'No\n' or split_line[0::][-1] == 'No':
                    undone += 1  
                    
            info_total += f'The total number of finished tasks is: {tasks}\n' 
            info_total += f'The total number of unfinished tasks is: {undone}\n'   
            info_total += f'The total number of overdue tasks is: {overdue_tasks}\n'   
            info_total += 'The percentage of tasks that are incomplete is: {:.2f}%\n'.format(percentage(undone,tasks_num))   
            info_total += 'The percentage of tasks that are overdue is: {:.2f}%\n'.format(percentage(overdue_tasks,tasks_num))

            print('\n' +info_total+'\n') 

            overview = open("task_overview.txt", "w")
            overview.write(info_total)
            overview.close()



        with open("user.txt", "r") as f7:
            # The total number of users registered with task_manager.py.
            users_num = len(f7.readlines())
            info_user = f'The total number of users is: {users_num}\n'
        
        with open("tasks.txt", "r") as f8:
            tasks_num = len(f8.readlines())
            info_user += f'The total number of tasks is: {tasks_num}\n'   

        # Read tasks from the file into a list of lists
        # For this part chatGPT was very useful and our discord channel

        tasks = []
        with open("tasks.txt") as task_file:
            for line in task_file:
                user, task_title, task_description, deadline, date_of_assignment, completed = line.strip().split(", ")
                tasks.append([user, task_title, task_description, deadline, date_of_assignment, completed])

        # The total number of tasks
        total_tasks = len(tasks)

        # Group tasks by user
        tasks_by_user = {}
        for task in tasks:
            user = task[0]
            if user not in tasks_by_user:
                tasks_by_user[user] = []
            tasks_by_user[user].append(task)

        # Write a summary of each user's tasks to the file

        with open("user.txt", "r") as f7:
             # The total number of users registered with task_manager.py.
            users_num = len(f7.readlines())
            info_u = f'The total number of users is: {users_num}\n'
        
        with open("tasks.txt", "r") as f8:
            tasks_num = len(f8.readlines())
            info_u += f'The total number of tasks is: {tasks_num}\n' 


        with open("user_overview.txt", "w") as user_overview_file:
            user_overview_file.write(info_u)
            user_overview_file.write('\n')
            for user, user_tasks in tasks_by_user.items():
                num_tasks = len(user_tasks)
        
                num_completed = len([task for task in user_tasks if task[5] == 'Yes'])
                num_overdue = len([task for task in user_tasks if task[5] not in ['Yes', 'No'] or (task[5] == 'No' and datetime.strptime(task[3], '%d %b %Y') < datetime.combine(date.today(), datetime.min.time()))])
        
                info_user = "User: {}\n".format(user)
                info_user += "  Total number of tasks: {}\n".format(num_tasks)
                info_user += "  Percentage of total tasks: {:.2f}%\n".format(percentage(num_tasks, total_tasks))
                info_user += "  Percentage of completed tasks: {:.2f}%\n".format(percentage(num_completed, num_tasks))
                info_user += "  Percentage of incomplete tasks: {:.2f}%\n".format(percentage(num_tasks - num_completed, num_tasks))
                info_user += "  Percentage of overdue tasks: {:.2f}%\n".format(percentage(num_overdue, num_tasks))
                info_user += "\n"

                print('\n' +info_user+'\n') 

                user_overview_file.write(info_user)

            
                
                
                         
    elif menu == 'e':
        print('You\'re logged out.')
        exit()

    else:
        print('You have made a wrong choice, Please Try again')