import hashlib

USERS_FILE = "user.txt"

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            users = {}
            for line in file:
                parts = line.strip().split(':')
                username = parts[0]
                password = parts[1]
                tasks = []
                if len(parts) > 2:
                    tasks = parts[2].split(',')
                users[username] = {'password': password, 'tasks': tasks}
            return users
    except FileNotFoundError:
        return {}
    
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        for username, data in users.items():
            tasks_str = ','.join(data['tasks'])
            file.write(f"{username}:{data['password']}:{tasks_str}\n")

def register():
    users = load_users()
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists. Please choose another one.")
        return
    password = hashlib.sha256(input("Enter a password: ").encode()).hexdigest()
    users[username] = {'password': password, 'tasks': []}
    save_users(users)
    print("Registration successful.")

def login():
    users = load_users()
    username = input("Enter your username: ")
    password = hashlib.sha256(input("Enter your password: ").encode()).hexdigest()
    if username in users and users[username]['password'] == password:
        print("Login successful.")
        return username
    else:
        print("Invalid username or password.")
        return None

def list_all_tasks(username):
    users = load_users()
    tasks = users[username]['tasks']
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task}")

def add_task(username):
    users = load_users()
    task = input("Enter a task: ")
    priority = input("Enter priority (high priority/medium priority/low priority): ")
    users[username]['tasks'].append(f"{task} ({priority})")
    save_users(users)
    print("Task added successfully.")

def update_task(username):
    users = load_users()
    tasks = users[username]['tasks']
    list_all_tasks(username)
    task_index = int(input("Enter the task number to update: ")) - 1
    if task_index < len(tasks):
        task = input("Enter the updated task: ")
        priority = input("Enter priority (high priority/medium priority/low priority): ")
        users[username]['tasks'][task_index] = f"{task} ({priority})"
        save_users(users)
        print("Task updated successfully.")
    else:
        print("Invalid task number.")

def delete_task(username):
    users = load_users()
    tasks = users[username]['tasks']
    list_all_tasks(username)
    task_index = int(input("Enter the task number to delete: ")) - 1
    if task_index < len(tasks):
        del users[username]['tasks'][task_index]
        save_users(users)
        print("Task deleted successfully.")
    else:
        print("Invalid task number.")

def main():
    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register()
        elif choice == '2':
            username = login()
            if username:
                while True:
                    print("\nLogged in as:", username)
                    print("1. List all tasks")
                    print("2. Add a task")
                    print("3. Update a task")
                    print("4. Delete a task")
                    print("5. Logout")
                    inner_choice = input("Enter your choice: ")
                    if inner_choice == '1':
                        list_all_tasks(username)
                    elif inner_choice == '2':
                        add_task(username)
                    elif inner_choice == '3':
                        update_task(username)
                    elif inner_choice == '4':
                        delete_task(username)
                    elif inner_choice == '5':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()


