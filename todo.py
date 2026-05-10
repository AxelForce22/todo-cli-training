# Todo App
# A beginner-friendly terminal to-do list that saves tasks to a JSON file.

import json
import os

# The file where tasks are saved
TASKS_FILE = "tasks.json"


def load_tasks():
    # If the file doesn't exist yet, return an empty list
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    # Write the current task list to the JSON file
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet. Add one!")
        return
    print("\nYour tasks:")
    for i, task in enumerate(tasks, start=1):
        # Show [x] if done, [ ] if not done
        status = "[x]" if task["done"] else "[ ]"
        print(f"  {i}. {status} {task['name']}")


def add_task(tasks):
    name = input("Enter the task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return
    tasks.append({"name": name, "done": False})
    save_tasks(tasks)
    print(f"Task '{name}' added.")


def complete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return
    number = get_task_number(tasks, "Enter the task number to mark as done: ")
    if number is None:
        return
    tasks[number]["done"] = True
    save_tasks(tasks)
    print(f"Task '{tasks[number]['name']}' marked as done.")


def delete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return
    number = get_task_number(tasks, "Enter the task number to delete: ")
    if number is None:
        return
    removed = tasks.pop(number)
    save_tasks(tasks)
    print(f"Task '{removed['name']}' deleted.")


def get_task_number(tasks, prompt):
    # Ask the user to pick a task by number and validate the input
    while True:
        user_input = input(prompt).strip()
        try:
            number = int(user_input) - 1  # Convert to zero-based index
            if 0 <= number < len(tasks):
                return number
            else:
                print(f"Please enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("That's not a valid number. Please try again.")


def main():
    print("Welcome to the Todo App!")

    # Load tasks once at the start
    tasks = load_tasks()

    while True:
        print("\nWhat would you like to do?")
        print("  1. Add task")
        print("  2. List tasks")
        print("  3. Mark task as done")
        print("  4. Delete task")
        print("  5. Quit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


# Run the app when this file is executed directly
if __name__ == "__main__":
    main()
