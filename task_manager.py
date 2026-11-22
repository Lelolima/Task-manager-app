import json
import os

# File to store tasks
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Warning: could not read {TASKS_FILE} ({exc}); starting with an empty list.")
            return []
        return data if isinstance(data, list) else []
    return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, description):
    """Add a new task."""
    task = {'description': description, 'completed': False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {description}")

def view_tasks(tasks):
    """View all tasks."""
    if not tasks:
        print("No tasks found.")
        return
    
    for index, task in enumerate(tasks, start=1):
        status = "Done" if task['completed'] else "Not Done"
        print(f"{index}. {task['description']} - {status}")

def mark_completed(tasks, task_index):
    """Mark a task as completed."""
    if 1 <= task_index <= len(tasks):
        tasks[task_index - 1]['completed'] = True
        save_tasks(tasks)
        print(f"Task marked as completed: {tasks[task_index - 1]['description']}")
    else:
        print("Invalid task index.")

def delete_task(tasks, task_index):
    """Delete a task."""
    if 1 <= task_index <= len(tasks):
        deleted_task = tasks.pop(task_index - 1)
        save_tasks(tasks)
        print(f"Task deleted: {deleted_task['description']}")
    else:
        print("Invalid task index.")

def read_index(prompt):
    """Read a task number; return None (with a message) if it is not an integer."""
    raw = input(prompt)
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid number.")
        return None

def main():
    tasks = load_tasks()

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
            else:
                add_task(tasks, description)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            task_index = read_index("Enter the task number to mark as completed: ")
            if task_index is not None:
                mark_completed(tasks, task_index)
        elif choice == '4':
            task_index = read_index("Enter the task number to delete: ")
            if task_index is not None:
                delete_task(tasks, task_index)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
